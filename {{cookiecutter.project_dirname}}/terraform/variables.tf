variable "digitalocean_token" {
  description = "The DigitalOcean access token."
  type        = string
  sensitive   = true
}

variable "digitalocean_cluster_name" {
  description = "The DigitalOcean cluster name."
  type        = string
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
