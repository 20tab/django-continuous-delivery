locals {
  project_name     = "{{ cookiecutter.project_name }}"
  project_slug     = "{{ cookiecutter.project_slug }}"
  environment_slug = { development = "dev", staging = "stage", production = "prod" }[lower(var.environment)]

  namespace = "${local.project_slug}-${local.environment_slug}"

  media_storage = "{{ cookiecutter.media_storage }}"

  extra_config_values = {}
  extra_secret_values = {}
}

terraform {
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
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
  name = var.stack_slug == "main" ? "${local.project_slug}-k8s-cluster" : "${local.project_slug}-${var.stack_slug}-k8s-cluster"
}

/* Deployment */

module "deployment" {
  source = "../modules/kubernetes/deployment"

  environment      = var.environment
  environment_slug = local.environment_slug

  namespace = local.namespace

  project_slug = local.project_slug
  project_url  = var.project_url

  service_container_image = var.service_container_image
  service_container_port  = var.service_container_port
  service_replicas        = var.service_replicas

  media_storage = local.media_storage

  django_admins             = var.django_admins
  django_allowed_hosts      = var.django_allowed_hosts
  django_default_from_email = var.django_default_from_email
  django_server_email       = var.django_server_email
  email_url                 = var.email_url
  s3_access_id              = var.s3_access_id
  s3_bucket_name            = var.s3_bucket_name
  s3_file_overwrite         = var.s3_file_overwrite
  s3_host                   = var.s3_host
  s3_region                 = var.s3_region
  s3_secret_key             = var.s3_secret_key
  sentry_dsn                = var.sentry_dsn
  web_concurrency           = var.web_concurrency

  extra_config_values = local.extra_config_values
  extra_secret_values = local.extra_secret_values
}
