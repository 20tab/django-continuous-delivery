{% if "environment" in cookiecutter.tfvars %}{% for item in cookiecutter.tfvars.environment|sort %}{{ item }}
{% endfor %}{% endif %}# django_admins=""
# django_additional_allowed_hosts=""
# django_configuration="Remote"
# django_default_from_email=""
# django_server_email=""
# s3_file_overwrite="False"
# service_container_port="{{ cookiecutter.internal_service_port }}"
# service_replicas=1
# web_concurrency=""
