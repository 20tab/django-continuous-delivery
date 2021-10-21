locals {
  project_name = "{{cookiecutter.project_name}}"
  project_slug = "{{cookiecutter.project_slug}}"
  environment_slug = { development = "dev", staging = "stage", production = "prod" }[lower(var.environment)]

  service_name = "${local.project_name} ${var.environment} {{cookiecutter.service_name}}"
  service_slug = "${local.project_slug}-${local.environment_slug}-{{cookiecutter.service_slug}}"
  service_labels = {
    component   = var.service_slug
    domain      = var.project_domain
    environment = var.environment
    project     = local.project_name
    terraform   = "true"
  }
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
      version = "2.6.0"
    }
  }
}

provider "digitalocean" {
  token = var.digitalocean_token
}

data "digitalocean_kubernetes_cluster" "main" {
  name = var.digitalocean_cluster_name
}

provider "kubernetes" {
  host  = data.digitalocean_kubernetes_cluster.main.endpoint
  token = data.digitalocean_kubernetes_cluster.main.kube_config[0].token
  cluster_ca_certificate = base64decode(
    data.digitalocean_kubernetes_cluster.main.kube_config[0].cluster_ca_certificate
  )
}

resource "kubernetes_deployment" "backend" {

  metadata {
    name      = "${var.service_slug}-deployment"
    namespace = "${local.project_slug}-development"
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
          name  = var.service_slug

          port {
            container_port = var.service_container_port
          }

          env {
            name = "CACHE_URL"

            value_from {

              secret_key_ref {
                key  = "CACHE_URL"
                name = "secrets"
              }
            }
          }

          env {
            name = "DATABASE_URL"

            value_from {

              secret_key_ref {
                key  = "DATABASE_URL"
                name = "secrets"
              }
            }
          }

          env {
            name = "DJANGO_ADMINS"

            value_from {

              secret_key_ref {
                key  = "DJANGO_ADMINS"
                name = "secrets"
              }
            }
          }

          env {
            name = "DJANGO_ALLOWED_HOSTS"

            value_from {

              secret_key_ref {
                key  = "DJANGO_ALLOWED_HOSTS"
                name = "secrets"
              }
            }
          }

          env {
            name = "DJANGO_CONFIGURATION"

            value_from {

              secret_key_ref {
                key  = "DJANGO_CONFIGURATION"
                name = "secrets"
              }
            }
          }
          {% if cookiecutter.use_media == "Yes" %}
          env {
            name = "DJANGO_AWS_ACCESS_KEY_ID"

            value_from {

              secret_key_ref {
                key  = "AWS_ACCESS_KEY_ID"
                name = "secrets"
              }
            }
          }

          env {
            name = "DJANGO_AWS_LOCATION"
            value= "$(DJANGO_CONFIGURATION)/media"
          }

          env {
            name = "DJANGO_AWS_S3_HOST"

            value_from {

              secret_key_ref {
                key  = "AWS_S3_HOST"
                name = "secrets"
              }
            }
          }

          env {
            name = "DJANGO_AWS_SECRET_ACCESS_KEY"

            value_from {

              secret_key_ref {
                key  = "AWS_SECRET_ACCESS_KEY"
                name = "secrets"
              }
            }
          }

          env {
            name = "DJANGO_AWS_STORAGE_BUCKET_NAME"

            value_from {

              secret_key_ref {
                key  = "AWS_STORAGE_BUCKET_NAME"
                name = "secrets"
              }
            }
          }
          {% endif %}
          env {
            name = "DJANGO_DEBUG"

            value_from {

              secret_key_ref {
                key  = "DJANGO_DEBUG"
                name = "secrets"
              }
            }
          }

          env {
            name = "DJANGO_DEFAULT_FROM_EMAIL"

            value_from {

              secret_key_ref {
                key  = "DJANGO_DEFAULT_FROM_EMAIL"
                name = "secrets"
              }
            }
          }

          env {
            name = "DJANGO_SECRET_KEY"

            value_from {

              secret_key_ref {
                key  = "DJANGO_SECRET_KEY"
                name = "secrets"
              }
            }
          }

          env {
            name = "DJANGO_SERVER_EMAIL"

            value_from {

              secret_key_ref {
                key  = "DJANGO_SERVER_EMAIL"
                name = "secrets"
              }
            }
          }

          env {
            name = "DJANGO_SESSION_COOKIE_DOMAIN"

            value_from {

              secret_key_ref {
                key  = "DJANGO_SESSION_COOKIE_DOMAIN"
                name = "secrets"
              }
            }
          }

          env {
            name = "EMAIL_URL"

            value_from {

              secret_key_ref {
                key  = "EMAIL_URL"
                name = "secrets"
              }
            }
          }

          env {
            name = "SENTRY_DSN"

            value_from {

              secret_key_ref {
                key  = "SENTRY_DSN"
                name = "secrets"
              }
            }
          }

          env {
            name = "WEB_CONCURRENCY"
            value= "1"
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "backend_cluster_ip" {

  metadata {
    name      = "${var.service_slug}-cluster-ip-service"
    namespace = "${local.project_slug}-development"
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
