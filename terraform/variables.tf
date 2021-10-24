variable "create_group_variables" {
  description = "True if Gitlab group variables should be created."
  type        = bool
  default     = false
}

variable "digitalocean_spaces_access_id" {
  description = "The DigitalOcean Spaces Access Key ID."
  type        = string
  default     = ""
  sensitive   = true
}

variable "digitalocean_spaces_bucket_region" {
  description = "The DigitalOcean Spaces bucket region."
  type        = string
  default     = "fra1"
}

variable "digitalocean_spaces_secret_key" {
  description = "The DigitalOcean Spaces Secret Key."
  type        = string
  default     = ""
  sensitive   = true
}

variable "digitalocean_token" {
  description = "The DigitalOcean access token."
  type        = string
  sensitive   = true
}

variable "gitlab_group_slug" {
  description = "The slug of the Gitlab group."
  type        = string
}

variable "gitlab_token" {
  description = "The Gitlab token."
  type        = string
  sensitive   = true
}

variable "project_description" {
  description = "The project description."
  type        = string
  default     = ""
}

variable "project_name" {
  description = "The project name."
  type        = string
}

variable "project_slug" {
  description = "The project slug."
  type        = string
}

variable "sentry_dsn" {
  description = "The Sentry project DSN."
  type        = string
  default     = ""
  sensitive   = true
}

variable "service_dir" {
  description = "The service directory."
  type        = string
}

variable "service_slug" {
  description = "The service slug."
  type        = string
}
