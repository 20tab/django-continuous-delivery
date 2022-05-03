variable "config_maps" {
  description = "The CronJob ConfigMap names."
  type        = list(string)
  default     = []
}

variable "container_command" {
  description = "The CronJob container command."
  type        = list(string)
}

variable "container_image" {
  description = "The CronJob container image."
  type        = string
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

variable "name" {
  type        = string
  description = "The CronJob name."
}

variable "namespace" {
  description = "The Kubernetes namespace."
  type        = string
}

variable "schedule" {
  description = "The CronJob schedule."
  type        = string
}

variable "secrets" {
  description = "The CronJob Secret names."
  type        = list(string)
  default     = []
}
