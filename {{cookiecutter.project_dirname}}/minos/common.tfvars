deployments = {
  {{ cookiecutter.service_slug }} = {
    port = "{{ cookiecutter.internal_service_port }}"
  }
}
postgres_enabled          = {{ cookiecutter.use_postgres }}
postgres_create_database  = {{ cookiecutter.postgres_create_database }}
service_slug              = "{{ cookiecutter.service_slug }}"
shared_secret_values_json = "shared-secrets.tftpl.json"
