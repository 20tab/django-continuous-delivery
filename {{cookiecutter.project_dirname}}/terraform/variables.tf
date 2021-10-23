variable "digitalocean_cluster_name" {
  description = "The DigitalOcean cluster name."
  type        = string
}
# {% if cookiecutter.media_storage == "s3" %}
variable "digitalocean_spaces_bucket_name" {
  description = "The DigitalOcean spaces bucket name."
  type        = string
  default     = "{{ cookiecutter.project_slug }}"
}

variable "digitalocean_spaces_bucket_region" {
  description = "The DigitalOcean spaces bucket region."
  type        = string
}
# {% endif %}
variable "digitalocean_token" {
  description = "The DigitalOcean access token."
  type        = string
  sensitive   = true
}
variable "django_admins" {
  type        = string
  description = "The value of the DJANGO_ADMINS environment variable."
  default     = "20tab,errors@20tab.com"
}

variable "django_allowed_hosts" {
  type        = string
  description = "The value of the DJANGO_ALLOWED_HOSTS environment variable."
  default     = "127.0.0.1,localhost"
}

variable "django_configuration" {
  type        = string
  description = "The value of the DJANGO_CONFIGURATION environment variable."
  default     = "Production"
}

variable "django_debug" {
  type        = string
  description = "The value of the DJANGO_DEBUG environment variable."
  default     = "False"
}

variable "django_default_from_email" {
  type        = string
  description = "The value of the DJANGO_DEFAULT_FROM_EMAIL environment variable."
}

variable "django_server_email" {
  type        = string
  description = "The value of the DJANGO_SERVER_EMAIL environment variable."
  default     = "info@20tab.com"
}

variable "environment" {
  type        = string
  description = "The name of the deploy environment, e.g. \"Production\"."
}

variable "project_description" {
  description = "The project description."
  type        = string
  default     = ""
}

variable "project_domain" {
  description = "The project domain."
  type        = string
}

variable "service_container_image" {
  description = "The service container image."
  type        = string
}

variable "service_container_port" {
  description = "The service container port."
  type        = number
  default     = 8000
}

variable "service_replicas" {
  description = "The desired numbers of replicas to deploy."
  type        = number
  default     = 1
}
