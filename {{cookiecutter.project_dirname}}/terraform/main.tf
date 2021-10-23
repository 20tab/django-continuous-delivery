locals {
  project_name     = "{{ cookiecutter.project_name }}"
  project_slug     = "{{ cookiecutter.project_slug }}"
  environment_slug = { development = "dev", staging = "stage", production = "prod" }[lower(var.environment)]

  service_name = "${local.project_name} ${var.environment} {{ cookiecutter.service_name }}"
  service_slug = "${local.project_slug}-${local.environment_slug}-{{ cookiecutter.service_slug }}"
  service_labels = {
    component   = local.service_slug
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

data "digitalocean_spaces_bucket" "main" {
  name   = var.digitalocean_spaces_bucket_name
  region = var.digitalocean_spaces_bucket_region
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
    name      = "${local.service_slug}-deployment"
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
          name  = local.service_slug

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
            name  = "DJANGO_ADMINS"
            value = var.django_admins
          }

          env {
            name  = "DJANGO_ALLOWED_HOSTS"
            value = var.django_allowed_hosts
          }

          env {
            name  = "DJANGO_CONFIGURATION"
            value = var.django_configuration
          }
          # {% if cookiecutter.media_storage == "s3" %}
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
            name  = "DJANGO_AWS_LOCATION"
            value = "${local.environment_slug}/media"
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
            name  = "DJANGO_AWS_STORAGE_BUCKET_NAME"
            value = var.digitalocean_spaces_bucket_name
          }
          # {% endif %}
          env {
            name  = "DJANGO_DEBUG"
            value = var.django_debug
          }

          env {
            name  = "DJANGO_DEFAULT_FROM_EMAIL"
            value = var.django_default_from_email
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
            name  = "DJANGO_SERVER_EMAIL"
            value = var.django_server_email
          }

          env {
            name  = "DJANGO_SESSION_COOKIE_DOMAIN"
            value = var.project_domain
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
            name  = "WEB_CONCURRENCY"
            value = "1"
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "backend_cluster_ip" {

  metadata {
    name      = "${local.service_slug}-cluster-ip-service"
    namespace = "${local.project_slug}-development"
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
