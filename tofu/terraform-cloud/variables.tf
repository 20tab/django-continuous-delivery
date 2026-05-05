variable "admin_email" {
  description = "The Terraform Cloud Organization admin email."
  type        = string
  default     = ""
}

variable "create_organization" {
  description = "Tell if the Terraform Cloud organization should be created."
  type        = bool
  default     = false
}

variable "create_project" {
  description = "Tell if the Terraform Cloud project should be created (false when Talos parent has already created it)."
  type        = bool
  default     = true
}

variable "environments" {
  description = "The list of environment slugs."
  type        = list(string)
  default     = []
}

variable "hostname" {
  description = "The Terraform Cloud hostname."
  type        = string
  default     = "app.terraform.io"
}

variable "organization_name" {
  description = "The Terraform Cloud Organization name."
  type        = string
}

variable "project_name" {
  description = "The project name."
  type        = string
}

variable "project_slug" {
  description = "The project slug."
  type        = string
}

variable "service_slug" {
  description = "The service slug."
  type        = string
}

variable "terraform_cloud_token" {
  description = "The Terraform Cloud token."
  type        = string
  sensitive   = true
  default     = ""
}
