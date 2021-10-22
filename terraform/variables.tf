variable "gitlab_group_slug" {
  description = "The slug of the Gitlab group."
  type        = string
}

variable "gitlab_token" {
  description = "The Gitlab token."
  type        = string
  sensitive   = true
}

variable "service_dir" {
  description = "The service directory."
  type        = string
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
