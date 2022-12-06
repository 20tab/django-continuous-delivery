terraform {
  required_providers {
    vault = {
      source  = "hashicorp/vault"
      version = "3.7.0"
    }
  }
}

provider "vault" {}

/* Secrets */

resource "vault_generic_secret" "main" {
  for_each = var.secrets

  path = "${var.project_slug}/${each.key}"

  data_json = jsonencode(each.value)
}
