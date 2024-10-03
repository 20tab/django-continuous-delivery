variable "cache_url" {
  type        = string
  description = "A Django cache URL override."
  default     = ""
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

variable "kubernetes_cluster_ca_certificate" {
  description = "The base64 encoded Kubernetes CA certificate."
  type        = string
  sensitive   = true
}

variable "kubernetes_host" {
  description = "The Kubernetes host."
  type        = string
}

variable "kubernetes_token" {
  description = "A Kubernetes admin token."
  type        = string
  sensitive   = true
}

variable "media_persistent_volume_capacity" {
  description = "The media persistent volume capacity (e.g. 1Gi)."
  type        = string
  default     = "10Gi"
}

variable "media_persistent_volume_claim_capacity" {
  description = "The media persistent volume claim capacity (e.g. 1Gi)."
  type        = string
  default     = ""
}

variable "media_persistent_volume_host_path" {
  description = "The media persistent volume host path."
  type        = string
  default     = ""
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
