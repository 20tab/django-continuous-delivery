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

  project_domain = regex("https?://([^/]*)", var.project_url)

  database_host     = data.digitalocean_database_cluster.main.private_host
  database_name     = "${local.project_slug}-${local.environment_slug}-database"
  database_password = digitalocean_database_user.main.password
  database_port     = data.digitalocean_database_cluster.main.port
  database_user     = "${local.project_slug}-${local.environment_slug}-database-user"
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
  name = var.digitalocean_cluster_name
}

data "digitalocean_spaces_bucket" "main" {
  name   = var.digitalocean_spaces_bucket_name
  region = var.digitalocean_spaces_bucket_region
}

data "digitalocean_database_cluster" "main" {
  name = "${local.project_slug}-database-cluster"
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

resource "kubernetes_secret" "main" {

  metadata {
    name      = "${local.service_slug}-secrets"
    namespace = local.namespace
  }

  data = {
    CACHE_URL         = var.cache_url
    DATABASE_URL      = "postgres://${local.database_user}:${local.database_password}@${local.database_host}:${local.database_port}/${local.database_name}"
    DJANGO_SECRET_KEY = random_password.django_secret_key
    EMAIL_URL         = var.email_url
    SENTRY_DSN        = var.sentry_dsn
  }
}

/* Config Map */

resource "kubernetes_config_map" "main" {
  metadata {
    name      = "${local.service_slug}-config-map"
    namespace = local.namespace
  }

  data = merge(
    {
      DJANGO_ADMINS                = var.django_admins
      DJANGO_ALLOWED_HOSTS         = var.django_allowed_hosts
      DJANGO_CONFIGURATION         = var.django_configuration
      DJANGO_DEBUG                 = var.django_debug
      DJANGO_DEFAULT_FROM_EMAIL    = var.django_default_from_email
      DJANGO_SERVER_EMAIL          = var.django_server_email
      DJANGO_SESSION_COOKIE_DOMAIN = local.project_domain
      WEB_CONCURRENCY              = "1"
    },
    var.media_storage == "s3" ? {
      DJANGO_AWS_LOCATION            = "${local.environment_slug}/media"
      DJANGO_AWS_STORAGE_BUCKET_NAME = var.digitalocean_spaces_bucket_name
    } : {}
  )
}

/* Deployment */

resource "kubernetes_deployment" "backend" {

  metadata {
    name      = "${local.service_slug}-deployment"
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
              name = kubernetes_secret.main.metadata[0].name
            }
          }

          env_from {
            config_map_ref {
              name = kubernetes_config_map.main.metadata[0].name
            }
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
            name = "DJANGO_AWS_SECRET_ACCESS_KEY"

            value_from {

              secret_key_ref {
                key  = "AWS_SECRET_ACCESS_KEY"
                name = "secrets"
              }
            }
          }
          # {% endif %}
        }
      }
    }
  }
}

/* Cluster IP Service */

resource "kubernetes_service" "backend_cluster_ip" {

  metadata {
    name      = "${local.service_slug}-cluster-ip-service"
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
