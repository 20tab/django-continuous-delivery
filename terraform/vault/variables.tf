variable "project_slug" {
  description = "The project slug."
  type        = string
}

variable "secrets" {
  description = "The service secrets."
  type        = map(map(string))
  default     = {}
}
