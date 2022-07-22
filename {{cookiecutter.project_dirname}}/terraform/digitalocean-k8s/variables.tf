variable "digitalocean_token" {
  description = "The Digital Ocean access token."
  type        = string
  sensitive   = true
}

variable "django_additional_allowed_hosts" {
  type        = string
  description = "Additional entries of the DJANGO_ALLOWED_HOSTS environment variable ('127.0.0.1', 'localhost', the service slug and the project host are included by default)."
  default     = ""
}

variable "django_admins" {
  type        = string
  description = "The value of the DJANGO_ADMINS environment variable."
  default     = ""
}

variable "django_configuration" {
  type        = string
  description = "The value of the DJANGO_CONFIGURATION environment variable."
  default     = "Remote"
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

variable "extra_config_values" {
  type        = map(string)
  description = "Additional config map environment variables."
  default     = {}
}

variable "extra_secret_values" {
  type        = map(string)
  description = "Additional secret environment variables."
  default     = {}
  sensitive   = true
}

variable "media_storage" {
  description = "The media storage solution."
  type        = string
}

variable "project_slug" {
  description = "The project slug."
  type        = string
}

variable "project_url" {
  description = "The project url."
  type        = string
}

variable "s3_access_id" {
  description = "The S3 bucket access key ID."
  type        = string
  default     = ""
  sensitive   = true
}

variable "s3_bucket_name" {
  description = "The S3 bucket name."
  type        = string
  default     = ""
}

variable "s3_file_overwrite" {
  description = "The S3 bucket file overwriting setting."
  type        = string
  default     = "False"
}

variable "s3_host" {
  description = "The S3 bucket host."
  type        = string
  default     = ""
}

variable "s3_region" {
  description = "The S3 bucket region."
  type        = string
  default     = ""
}

variable "s3_secret_key" {
  description = "The S3 bucket secret access key."
  type        = string
  default     = ""
  sensitive   = true
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
  type        = string
  default     = "{{ cookiecutter.internal_service_port }}"
}

variable "service_replicas" {
  description = "The desired numbers of replicas to deploy."
  type        = number
  default     = 1
}

variable "service_slug" {
  description = "The service slug."
  type        = string
}

variable "stack_slug" {
  description = "The slug of the stack where the service is deployed."
  type        = string
}

variable "use_redis" {
  description = "Tell if a Redis service is used."
  type        = bool
  default     = false
}

variable "web_concurrency" {
  description = "The desired number of gunicorn workers."
  type        = string
  default     = ""
}
