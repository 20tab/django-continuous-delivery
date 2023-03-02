locals {
  service_labels = {
    component   = var.service_slug
    environment = var.environment
    project     = var.project_slug
    terraform   = "true"
  }

  project_host = regexall("https?://([^/]+)", var.project_url)[0][0]

  django_allowed_hosts = join(
    ",",
    setunion(
      split(",", coalesce(var.django_additional_allowed_hosts, "127.0.0.1,localhost")),
      [local.project_host, var.service_slug]
    )
  )

  use_s3 = length(regexall("s3", var.media_storage)) > 0
}

terraform {
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.12"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.3"
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
    name      = "${var.service_slug}-env-vars"
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
    name      = "${var.service_slug}-env-vars"
    namespace = var.namespace
  }

  data = { for k, v in merge(
    var.extra_config_values,
    {
      DJANGO_ADMINS                      = var.django_admins
      DJANGO_ALLOWED_HOSTS               = local.django_allowed_hosts
      DJANGO_CONFIGURATION               = "Remote"
      DJANGO_CSRF_TRUSTED_ORIGINS        = var.project_url
      DJANGO_DEFAULT_FROM_EMAIL          = var.django_default_from_email
      DJANGO_DISABLE_SERVER_SIDE_CURSORS = var.django_disable_server_side_cursors
      DJANGO_SERVER_EMAIL                = var.django_server_email
      DJANGO_SESSION_COOKIE_DOMAIN       = local.project_host
      INTERNAL_SERVICE_PORT              = var.service_container_port
      SENTRY_ENVIRONMENT                 = var.environment
      WEB_CONCURRENCY                    = var.web_concurrency
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
    name      = var.service_slug
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
        dynamic "volume" {
          for_each = toset(var.media_persistent_volume_claim_name != "" ? [1] : [])

          content {
            name = "media"
            persistent_volume_claim {
              claim_name = var.media_persistent_volume_claim_name
            }
          }
        }
        image_pull_secrets {
          name = "regcred"
        }
        container {
          image = var.service_container_image
          name  = var.service_slug
          resources {
            limits = {
              cpu    = var.service_limits_cpu
              memory = var.service_limits_memory
            }
            requests = {
              cpu    = var.service_requests_cpu
              memory = var.service_requests_memory
            }
          }
          port {
            container_port = var.service_container_port
          }
          dynamic "volume_mount" {
            for_each = toset(var.media_persistent_volume_claim_name != "" ? [1] : [])

            content {
              name       = "media"
              mount_path = var.media_mount_path
            }
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
            for_each = toset(var.additional_secrets)
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
    name      = var.service_slug
    namespace = var.namespace
  }
  spec {
    type = "ClusterIP"
    selector = {
      component = var.service_slug
    }
    port {
      port        = var.service_container_port
      target_port = var.service_container_port
    }
  }
}
