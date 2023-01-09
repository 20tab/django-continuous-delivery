variable "project_slug" {
  description = "The project slug."
  type        = string
}

variable "secrets" {
  description = "The service secrets."
  type        = map(map(string))
  default     = {}
}

variable "vault_address" {
  description = "The Vault address."
  type        = string
}

variable "vault_token" {
  description = "The Vault token."
  type        = string
  sensitive   = true
  default     = ""
}
