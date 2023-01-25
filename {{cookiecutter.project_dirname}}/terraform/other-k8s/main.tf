locals {
  environment_slug = { development = "dev", staging = "stage", production = "prod" }[lower(var.environment)]

  namespace = "${var.project_slug}-${local.environment_slug}"
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

/* Providers */

provider "kubernetes" {
  host                   = var.kubernetes_host
  token                  = var.kubernetes_token
  cluster_ca_certificate = base64decode(var.kubernetes_cluster_ca_certificate)
}

/* Providers */

provider "kubernetes" {
  host                   = var.kubernetes_host
  token                  = var.kubernetes_token
  cluster_ca_certificate = base64decode(var.kubernetes_cluster_ca_certificate)
}

/* Volumes */

resource "kubernetes_persistent_volume_v1" "media" {
  count = var.media_storage == "local" ? 1 : 0

  metadata {
    name = "${local.namespace}-${var.service_slug}-media"
  }
  spec {
    capacity = {
      storage = var.media_persistent_volume_capacity
    }
    access_modes = ["ReadWriteOnce"]
    persistent_volume_source {
      host_path {
        path = var.media_persistent_volume_host_path
      }
    }
  }
}

resource "kubernetes_persistent_volume_claim_v1" "media" {
  count = var.media_storage == "local" ? 1 : 0

  metadata {
    name      = "${var.service_slug}-media"
    namespace = local.namespace
  }
  spec {
    access_modes = ["ReadWriteOnce"]
    resources {
      requests = {
        storage = coalesce(
          var.media_persistent_volume_claim_capacity,
          var.media_persistent_volume_capacity
        )
      }
    }
    volume_name = kubernetes_persistent_volume_v1.media[0].metadata[0].name
  }
}

/* Deployment */

module "deployment" {
  source = "../modules/kubernetes/deployment"

  environment      = var.environment
  environment_slug = local.environment_slug

  namespace = local.namespace

  project_slug = var.project_slug
  project_url  = var.project_url

  service_container_image = var.service_container_image
  service_container_port  = var.service_container_port
  service_limits_cpu      = var.service_limits_cpu
  service_limits_memory   = var.service_limits_memory
  service_replicas        = var.service_replicas
  service_requests_cpu    = var.service_requests_cpu
  service_requests_memory = var.service_requests_memory
  service_slug            = var.service_slug

  media_storage = var.media_storage

  media_persistent_volume_claim_name = var.media_storage == "local" ? kubernetes_persistent_volume_claim_v1.media[0].metadata[0].name : ""

  django_admins                   = var.django_admins
  django_additional_allowed_hosts = var.django_additional_allowed_hosts
  django_default_from_email       = var.django_default_from_email
  django_server_email             = var.django_server_email
  email_url                       = var.email_url
  s3_access_id                    = var.s3_access_id
  s3_bucket_name                  = var.s3_bucket_name
  s3_file_overwrite               = var.s3_file_overwrite
  s3_host                         = var.s3_host
  s3_region                       = var.s3_region
  s3_secret_key                   = var.s3_secret_key
  sentry_dsn                      = var.sentry_dsn
  web_concurrency                 = var.web_concurrency

  extra_config_values = var.extra_config_values
  extra_secret_values = var.extra_secret_values

  additional_secrets = var.use_redis ? ["database-url", "cache-url"] : ["database-url"]
}
