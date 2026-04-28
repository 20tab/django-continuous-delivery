locals {
  organization = var.create_organization ? tfe_organization.main[0] : data.tfe_organization.main[0]
  project      = var.create_project ? tfe_project.main[0] : data.tfe_project.main[0]

  workspaces = [
    for env in var.environments : {
      name        = "${var.project_slug}_${var.service_slug}_${env}"
      description = "${var.project_name} ${var.service_slug} service, ${env} environment."
      tags = [
        "project:${var.project_slug}",
        "layer:service",
        "service:${var.service_slug}",
        "environment:${env}",
      ]
    }
  ]
}

terraform {
  backend "local" {
  }

  required_providers {
    tfe = {
      source  = "hashicorp/tfe"
      version = "~> 0.70"
    }
  }
}

provider "tfe" {
  hostname = var.hostname
  token    = var.terraform_cloud_token
}

/* Organization */

data "tfe_organization" "main" {
  count = var.create_organization ? 0 : 1

  name = var.organization_name
}

resource "tfe_organization" "main" {
  count = var.create_organization ? 1 : 0

  name  = var.organization_name
  email = var.admin_email
}

/* Project */

data "tfe_project" "main" {
  count = var.create_project ? 0 : 1

  name         = var.project_slug
  organization = local.organization.name
}

resource "tfe_project" "main" {
  count = var.create_project ? 1 : 0

  organization = local.organization.name
  name         = var.project_slug
  description  = "${var.project_name} project workspaces."
}

resource "tfe_project_settings" "main" {
  project_id             = local.project.id
  default_execution_mode = "local"
}

/* Workspaces */

resource "tfe_workspace" "main" {
  for_each = { for i in local.workspaces : i.name => i }

  name         = each.value.name
  description  = each.value.description
  organization = local.organization.name
  project_id   = local.project.id
  tag_names    = each.value.tags
}
