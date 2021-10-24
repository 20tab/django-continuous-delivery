variable "cache_url" {
  description = "The cache connection url."
  type        = string
  default     = ""
  sensitive   = true
}

variable "digitalocean_k8s_cluster_name" {
  description = "The DigitalOcean cluster name."
  type        = string
  default     = ""
}

variable "digitalocean_database_cluster_name" {
  description = "The DigitalOcean database cluster name."
  type        = string
  default     = ""
}

variable "digitalocean_spaces_access_id" {
  description = "The DigitalOcean Spaces Access Key ID."
  type        = string
  default     = ""
  sensitive   = true
}

variable "digitalocean_spaces_bucket_name" {
  description = "The DigitalOcean Spaces bucket name."
  type        = string
  default     = "{{ cookiecutter.project_slug }}"
}

variable "digitalocean_spaces_bucket_region" {
  description = "The DigitalOcean Spaces bucket region."
  type        = string
  default     = "fra1"
}

variable "digitalocean_spaces_file_overwrite" {
  description = "The DigitalOcean Spaces file overwriting setting."
  type        = string
  default     = "False"
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

variable "django_admins" {
  type        = string
  description = "The value of the DJANGO_ADMINS environment variable."
  default     = ""
}

variable "django_allowed_hosts" {
  type        = string
  description = "The value of the DJANGO_ALLOWED_HOSTS environment variable."
  default     = ""
}

variable "django_configuration" {
  type        = string
  description = "The value of the DJANGO_CONFIGURATION environment variable."
  default     = ""
}

variable "django_default_from_email" {
  type        = string
  description = "The value of the DJANGO_DEFAULT_FROM_EMAIL environment variable."
  default     = ""
}

variable "django_server_email" {
  type        = string
  description = "The value of the DJANGO_SERVER_EMAIL environment variable."
  default     = ""
}

variable "email_url" {
  type        = string
  description = "The email server connection url."
  default     = ""
  sensitive   = true
}

variable "environment" {
  type        = string
  description = "The name of the deploy environment, e.g. \"Production\"."
}

variable "media_storage" {
  description = "The media storage solution."
  type        = string
  default     = "{{ cookiecutter.media_storage }}"
}

variable "project_url" {
  description = "The project url."
  type        = string
}

variable "sentry_dsn" {
  description = "The Sentry project DSN."
  type        = string
  default     = ""
  sensitive   = true
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
