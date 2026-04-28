{% set env = cookiecutter.resources.envs|selectattr("slug", "equalto", "prod")|first %}certificates = {
  primary = {
    letsencrypt_email = "tech@20tab.com"
    hosts             = ["{{ env.host }}"]
  }
}
cluster_slug              = "{{ cookiecutter.project_slug }}-{{ env.cluster_slug }}"
environment               = "{{ env.name }}"
namespace                 = "{{ cookiecutter.project_slug }}-{{ env.slug }}"
project_slug              = "{{ cookiecutter.project_slug }}"
routing = {
  "{{ env.host }}" = { deployment = "{{ cookiecutter.service_slug }}" }
}
shared_config_values_yaml = "{{ env.name }}/shared-config.yaml"
