locals {
  project_name     = "{{ cookiecutter.project_name }}"
  project_slug     = "{{ cookiecutter.project_slug }}"
  service_slug     = "{{ cookiecutter.service_slug }}"
  environment_slug = { development = "dev", staging = "stage", production = "prod" }[lower(var.environment)]

  namespace = "${local.project_slug}-${local.environment_slug}"

  stacks        = jsondecode(var.stacks)
  stack_slug    = compact([for k, v in local.stacks : lookup(v, local.environment_slug, "") != "" ? k : ""])[0]
  resource_name = local.stack_slug == "main" ? local.project_slug : "${local.project_slug}-${local.stack_slug}"

  service_labels = {
    component   = local.service_slug
    environment = var.environment
    project     = local.project_slug
    terraform   = "true"
  }

  project_host = regexall("https?://([^/]+)", var.project_url)[0][0]

  django_allowed_hosts = join(
    ",",
    setunion(
      split(",", coalesce(var.django_allowed_hosts, "127.0.0.1,localhost")),
      [local.project_host, local.service_slug]
    )
  )

  service_container_port = coalesce(var.service_container_port, "{{ cookiecutter.internal_service_port }}")
}

terraform {
  backend "http" {
  }

  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "2.8.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "3.1.0"
    }
  }
}

/* Providers */

provider "digitalocean" {
  token = var.digitalocean_token
}

provider "kubernetes" {
  host  = data.digitalocean_kubernetes_cluster.main.endpoint
  token = data.digitalocean_kubernetes_cluster.main.kube_config[0].token
  cluster_ca_certificate = base64decode(
    data.digitalocean_kubernetes_cluster.main.kube_config[0].cluster_ca_certificate
  )
}

/* Data Sources */

data "digitalocean_kubernetes_cluster" "main" {
  name = "${local.resource_name}-k8s-cluster"
}

/* Passwords */

resource "random_password" "django_secret_key" {
  length = 50
}

/* Secrets */

resource "kubernetes_secret_v1" "env" {

  metadata {
    name      = "${local.service_slug}-env"
    namespace = local.namespace
  }

  data = { for k, v in merge(
    {
      CACHE_URL         = var.cache_url
      DATABASE_URL      = var.database_url
      DJANGO_SECRET_KEY = random_password.django_secret_key.result
      EMAIL_URL         = var.email_url
      SENTRY_DSN        = var.sentry_dsn
    },
    var.media_storage == "s3" ? {
      AWS_ACCESS_KEY_ID     = var.s3_bucket_access_id
      AWS_SECRET_ACCESS_KEY = var.s3_bucket_secret_key
    } : {}
  ) : k => v if v != "" }
}

/* Config Map */

resource "kubernetes_config_map_v1" "env" {
  metadata {
    name      = "${local.service_slug}-env"
    namespace = local.namespace
  }

  data = { for k, v in merge(
    {
      DJANGO_ADMINS                = var.django_admins
      DJANGO_ALLOWED_HOSTS         = local.django_allowed_hosts
      DJANGO_CONFIGURATION         = var.django_configuration
      DJANGO_DEFAULT_FROM_EMAIL    = var.django_default_from_email
      DJANGO_SERVER_EMAIL          = var.django_server_email
      DJANGO_SESSION_COOKIE_DOMAIN = local.project_host
      INTERNAL_SERVICE_PORT        = local.service_container_port
      WEB_CONCURRENCY              = var.web_concurrency
    },
    var.media_storage == "s3" ? {
      DJANGO_AWS_LOCATION            = local.environment_slug
      DJANGO_AWS_STORAGE_BUCKET_NAME = var.s3_bucket_name
      DJANGO_AWS_S3_ENDPOINT_URL     = var.s3_bucket_endpoint_url
      DJANGO_AWS_S3_FILE_OVERWRITE   = var.s3_bucket_file_overwrite
    } : {}
  ) : k => v if v != "" }
}

/* Deployment */

resource "kubernetes_deployment_v1" "main" {

  metadata {
    name      = local.service_slug
    namespace = local.namespace
  }

  spec {
    replicas = var.service_replicas

    selector {
      match_labels = local.service_labels
    }

    template {

      metadata {
        labels = local.service_labels
      }

      spec {

        image_pull_secrets {
          name = "regcred"
        }

        container {
          image = var.service_container_image
          name  = local.service_slug

          port {
            container_port = local.service_container_port
          }

          env_from {
            config_map_ref {
              name = kubernetes_config_map_v1.env.metadata[0].name
            }
          }

          env_from {
            secret_ref {
              name = kubernetes_secret_v1.env.metadata[0].name
            }
          }
        }
      }
    }
  }
}

/* Cluster IP Service */

resource "kubernetes_service_v1" "cluster_ip" {

  metadata {
    name      = local.service_slug
    namespace = local.namespace
  }

  spec {
    type = "ClusterIP"
    selector = {
      component = local.service_slug
    }

    port {
      port        = local.service_container_port
      target_port = local.service_container_port
    }

  }
}
