terraform {
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.27"
    }
  }
}

/* Cron Job */

resource "kubernetes_cron_job_v1" "main" {
  metadata {
    name      = var.name
    namespace = var.namespace
  }

  spec {
    schedule = var.schedule
    job_template {
      metadata {}
      spec {
        template {
          metadata {}
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
              name    = "main"
              image   = var.container_image
              command = var.container_command
              dynamic "volume_mount" {
                for_each = toset(var.media_persistent_volume_claim_name != "" ? [1] : [])

                content {
                  name       = "media"
                  mount_path = var.media_mount_path
                }
              }
              dynamic "env_from" {
                for_each = toset(var.config_maps)

                content {
                  config_map_ref {
                    name = env_from.key
                  }
                }
              }
              dynamic "env_from" {
                for_each = toset(var.secrets)

                content {
                  secret_ref {
                    name = env_from.key
                  }
                }
              }
            }
            restart_policy = "OnFailure"
          }
        }
      }
    }
  }
}
