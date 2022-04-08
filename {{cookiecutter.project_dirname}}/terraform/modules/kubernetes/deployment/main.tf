locals {
  service_slug = "{{ cookiecutter.service_slug }}"

  service_labels = {
    component   = local.service_slug
    environment = var.environment
    project     = var.project_slug
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

  dynamic_secret_envs = split(",", "{% if cookiecutter.use_redis == 'True' %}database-url,cache-url{% else %}database-url{% endif %}")

  use_s3 = length(regexall("s3", var.media_storage)) > 0
}

terraform {
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "2.9.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.1"
    }
  }
}

/* Passwords */

resource "random_password" "django_secret_key" {
  length = 50
}

/* Secrets */

resource "kubernetes_secret_v1" "main" {

  metadata {
    name      = "${local.service_slug}-env-vars"
    namespace = var.namespace
  }

  data = { for k, v in merge(
    var.extra_secret_values,
    {
      DJANGO_SECRET_KEY = random_password.django_secret_key.result
      EMAIL_URL         = var.email_url
      SENTRY_DSN        = var.sentry_dsn
    },
    local.use_s3 ? {
      AWS_ACCESS_KEY_ID     = var.s3_access_id
      AWS_SECRET_ACCESS_KEY = var.s3_secret_key
    } : {}
  ) : k => v if v != "" }
}

/* Config Map */

resource "kubernetes_config_map_v1" "main" {
  metadata {
    name      = "${local.service_slug}-env-vars"
    namespace = var.namespace
  }

  data = { for k, v in merge(
    var.extra_config_values,
    {
      DJANGO_ADMINS                = var.django_admins
      DJANGO_ALLOWED_HOSTS         = local.django_allowed_hosts
      DJANGO_CONFIGURATION         = "Remote"
      DJANGO_DEFAULT_FROM_EMAIL    = var.django_default_from_email
      DJANGO_SERVER_EMAIL          = var.django_server_email
      DJANGO_SESSION_COOKIE_DOMAIN = local.project_host
      INTERNAL_SERVICE_PORT        = local.service_container_port
      SENTRY_ENVIRONMENT           = var.environment
      WEB_CONCURRENCY              = var.web_concurrency
    },
    local.use_s3 ? {
      AWS_S3_REGION_NAME             = var.s3_region
      DJANGO_AWS_LOCATION            = "${var.environment_slug}/media"
      DJANGO_AWS_S3_ENDPOINT_URL     = var.media_storage == "digitalocean-s3" ? "https://${var.s3_region}.${var.s3_host}" : ""
      DJANGO_AWS_S3_FILE_OVERWRITE   = var.s3_file_overwrite
      DJANGO_AWS_STORAGE_BUCKET_NAME = var.s3_bucket_name
    } : {}
  ) : k => v if v != "" }
}

/* Deployment */

resource "kubernetes_deployment_v1" "main" {
  metadata {
    name      = local.service_slug
    namespace = var.namespace
    annotations = {
      "reloader.stakater.com/auto" = "true"
    }
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
              name = kubernetes_config_map_v1.main.metadata[0].name
            }
          }
          env_from {
            secret_ref {
              name = kubernetes_secret_v1.main.metadata[0].name
            }
          }
          dynamic "env_from" {
            for_each = toset(local.dynamic_secret_envs)
            content {
              secret_ref {
                name = env_from.key
              }
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
    namespace = var.namespace
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
