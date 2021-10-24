locals {
  project_name     = "{{ cookiecutter.project_name }}"
  project_slug     = "{{ cookiecutter.project_slug }}"
  service_slug     = "{{ cookiecutter.service_slug }}"
  environment_slug = { development = "dev", staging = "stage", production = "prod" }[lower(var.environment)]

  namespace = "${local.project_slug}-${local.environment_slug}"

  service_labels = {
    component   = local.service_slug
    environment = var.environment
    project     = local.project_name
    terraform   = "true"
    url         = var.project_url
  }

  digitalocean_k8s_cluster_name      = coalesce(var.digitalocean_k8s_cluster_name, "${local.project_slug}-k8s-cluster")
  digitalocean_database_cluster_name = coalesce(var.digitalocean_database_cluster_name, "${local.project_slug}-database-cluster")

  project_domain = regex("https?://([^/]*)", var.project_url)

  database_host     = data.digitalocean_database_cluster.main.private_host
  database_name     = "${local.project_slug}-${local.environment_slug}-database"
  database_password = digitalocean_database_user.main.password
  database_port     = data.digitalocean_database_cluster.main.port
  database_user     = "${local.project_slug}-${local.environment_slug}-database-user"
  database_url      = "postgres://${local.database_user}:${local.database_password}@${local.database_host}:${local.database_port}/${local.database_name}"

  s3_endpoint_url = "https://${var.digitalocean_spaces_bucket_region}.digitaloceanspaces.com"
}

terraform {
  backend "local" {
  }

  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "2.6.0"
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
  name = local.digitalocean_k8s_cluster_name
}

data "digitalocean_spaces_bucket" "media" {
  count = var.media_storage == "s3" ? 1 : 0

  name   = var.digitalocean_spaces_bucket_name
  region = var.digitalocean_spaces_bucket_region
}

data "digitalocean_database_cluster" "main" {
  name = local.digitalocean_database_cluster_name
}

/* Database */

resource "digitalocean_database_user" "main" {
  cluster_id = data.digitalocean_database_cluster.main.id
  name       = local.database_user
}

resource "digitalocean_database_db" "main" {
  cluster_id = data.digitalocean_database_cluster.main.id
  name       = local.database_name
}

/* Passwords */

resource "random_password" "django_secret_key" {
  length = 50
}

/* Secrets */

resource "kubernetes_secret" "env" {

  metadata {
    name      = "${local.service_slug}-env"
    namespace = local.namespace
  }

  data = merge(
    {
      CACHE_URL         = coalesce(var.cache_url, "locmem://")
      DATABASE_URL      = local.database_url
      DJANGO_SECRET_KEY = random_password.django_secret_key.result
      EMAIL_URL         = coalesce(var.email_url, "console://")
    },
    var.media_storage == "s3" ? {
      AWS_ACCESS_KEY_ID     = var.digitalocean_spaces_access_id
      AWS_SECRET_ACCESS_KEY = var.digitalocean_spaces_secret_key
    } : {},
    var.sentry_dsn != "" ? {
      SENTRY_DSN = var.sentry_dsn
    } : {},
  )
}

/* Config Map */

resource "kubernetes_config_map" "env" {
  metadata {
    name      = "${local.service_slug}-env"
    namespace = local.namespace
  }

  data = merge(
    {
      DJANGO_ADMINS                = coalesce(var.django_admins, "admin,admin@${local.project_slug}.com")
      DJANGO_ALLOWED_HOSTS         = coalesce(var.django_allowed_hosts, "127.0.0.1,localhost,${local.project_domain}")
      DJANGO_CONFIGURATION         = coalesce(var.django_configuration, "Production")
      DJANGO_DEFAULT_FROM_EMAIL    = coalesce(var.django_default_from_email, "info@${local.project_slug}.com")
      DJANGO_SERVER_EMAIL          = coalesce(var.django_server_email, "no-reply@${local.project_slug}.com")
      DJANGO_SESSION_COOKIE_DOMAIN = local.project_domain
      WEB_CONCURRENCY              = "1"
    },
    var.media_storage == "s3" ? {
      DJANGO_AWS_LOCATION            = local.environment_slug
      DJANGO_AWS_STORAGE_BUCKET_NAME = var.digitalocean_spaces_bucket_name
      DJANGO_AWS_S3_ENDPOINT_URL     = local.s3_endpoint_url
      DJANGO_AWS_S3_FILE_OVERWRITE   = var.digitalocean_spaces_file_overwrite
    } : {}
  )
}

/* Deployment */

resource "kubernetes_deployment" "main" {

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
            container_port = var.service_container_port
          }

          env_from {
            secret_ref {
              name = kubernetes_secret.env.metadata[0].name
            }
          }

          env_from {
            config_map_ref {
              name = kubernetes_config_map.env.metadata[0].name
            }
          }
        }
      }
    }
  }
}

/* Cluster IP Service */

resource "kubernetes_service" "cluster_ip" {

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
      port        = var.service_container_port
      target_port = var.service_container_port
    }

  }
}
