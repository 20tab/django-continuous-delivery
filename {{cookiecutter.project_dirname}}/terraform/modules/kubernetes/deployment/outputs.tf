output "config_map_name" {
  description = "The name of the Kubernetes ConfigMap associated with the Deployment."
  value       = kubernetes_config_map_v1.main.metadata[0].name
}

output "secret_name" {
  description = "The name of the Kubernetes Secret associated with the Deployment."
  value       = kubernetes_secret_v1.main.metadata[0].name
}
