terraform {
  backend "local" {
  }

  required_providers {
    vault = {
      source  = "hashicorp/vault"
      version = "~>3.11.0"
    }
  }
}

provider "vault" {
  address = var.vault_address

  token = var.vault_token

  dynamic "auth_login_oidc" {
    for_each = var.vault_token == "" ? ["default"] : []

    content {
      role = auth_login_oidc.value
    }
  }
}

/* Secrets */

resource "vault_generic_secret" "main" {
  for_each = var.secrets

  path = "${var.project_slug}/${each.key}"

  data_json = jsonencode(each.value)
}
