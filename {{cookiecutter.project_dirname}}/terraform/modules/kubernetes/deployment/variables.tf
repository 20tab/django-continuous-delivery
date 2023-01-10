variable "additional_secrets" {
  type        = list(any)
  description = "Additional Kubernetes Secret names to link to the Deployment."
  default     = []
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

variable "django_default_from_email" {
  type        = string
  description = "The value of the DJANGO_DEFAULT_FROM_EMAIL environment variable."
  default     = ""
}

variable "django_disable_server_side_cursors" {
  type        = string
  description = "The value of the DJANGO_DISABLE_SERVER_SIDE_CURSORS environment variable."
  default     = "False"
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
  description = "The deploy environment name, e.g. \"Production\"."
}

variable "environment_slug" {
  type        = string
  description = "The deploy environment slug, e.g. \"stage\"."
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

variable "media_mount_path" {
  description = "The mount path of the media directory inside the container."
  type        = string
  default     = "/app/media"
}

variable "media_persistent_volume_claim_name" {
  description = "The media persistent volume claim name."
  type        = string
  default     = ""
}

variable "media_storage" {
  description = "The media storage solution."
  type        = string
}

variable "namespace" {
  description = "The Kubernetes namespace."
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
  default     = ""
}

variable "service_limits_cpu" {
  description = "The service limits cpu value."
  type        = string
}

variable "service_limits_memory" {
  description = "The service limits memory value."
  type        = string
}

variable "service_replicas" {
  description = "The desired numbers of replicas to deploy."
  type        = number
  default     = 1
}

variable "service_requests_cpu" {
  description = "The service requests cpu value."
  type        = string
}

variable "service_requests_memory" {
  description = "The service requests memory value."
  type        = string
}

variable "service_slug" {
  description = "The service slug."
  type        = string
}

variable "web_concurrency" {
  description = "The desired number of gunicorn workers."
  type        = string
  default     = ""
}
