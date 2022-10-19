locals {
  user_data = jsondecode(data.http.user_info.response_body)

  git_config_args = "-c user.email=${local.user_data.email} -c user.name=\"${local.user_data.name}\""

  is_main_group_root = data.gitlab_group.main.parent_id == 0

  pages_base_url = local.is_main_group_root ? "https://${data.gitlab_group.main.path}.gitlab.io" : data.gitlab_group.main_parent[0].parent_id == 0 ? "https://${data.gitlab_group.main_parent[0].path}.gitlab.io/${data.gitlab_group.main.path}" : ""
}

terraform {
  backend "local" {
  }

  required_providers {
    gitlab = {
      source  = "gitlabhq/gitlab"
      version = "~> 3.18"
    }
  }
}

/* Providers */

provider "gitlab" {
  token = var.gitlab_token
}

/* User Info */

data "http" "user_info" {
  url = "${var.gitlab_url}/api/v4/user"

  request_headers = {
    Accept        = "application/json"
    Authorization = "Bearer ${var.gitlab_token}"
  }
}

/* Group */

data "gitlab_group" "main" {
  full_path = var.group_path
}

data "gitlab_group" "main_parent" {
  count = local.is_main_group_root ? 0 : 1

  group_id = data.gitlab_group.main.parent_id
}

/* Project */

resource "gitlab_project" "main" {
  name                   = title(var.service_slug)
  path                   = var.service_slug
  description            = "The \"${var.project_name}\" project ${var.service_slug} service."
  namespace_id           = data.gitlab_group.main.id
  initialize_with_readme = false
  shared_runners_enabled = true
}

resource "null_resource" "init_repo" {
  depends_on = [gitlab_branch_protection.develop]

  triggers = {
    service_project_id = gitlab_project.main.id
  }

  provisioner "local-exec" {
    command = join(" && ", [
      "cd ${var.service_dir}",
      format(
        join(" && ", [
          "git init --initial-branch=develop",
          "git remote add origin %s",
          "git add .",
          "git ${local.git_config_args} commit -m 'Initial commit'",
          "git push -u origin develop -o ci.skip",
          "git checkout -b main",
          "git push -u origin main -o ci.skip",
          "git remote set-url origin %s",
          "git checkout develop",
        ]),
        replace(
          gitlab_project.main.http_url_to_repo,
          "/^https://(.*)$/",
          "https://oauth2:${var.gitlab_token}@$1"
        ),
        gitlab_project.main.ssh_url_to_repo,
      )
    ])
  }
}

/* Branch Protections */

resource "gitlab_branch_protection" "develop" {
  project            = gitlab_project.main.id
  branch             = "develop"
  push_access_level  = "maintainer"
  merge_access_level = "developer"
}

resource "gitlab_branch_protection" "main" {
  depends_on = [null_resource.init_repo]

  project            = gitlab_project.main.id
  branch             = "main"
  push_access_level  = "no one"
  merge_access_level = "maintainer"
}

resource "gitlab_tag_protection" "tags" {
  project             = gitlab_project.main.id
  tag                 = "*"
  create_access_level = "maintainer"
}

/* Badges */

resource "gitlab_project_badge" "root_group_coverage" {
  count = local.pages_base_url != "" ? 1 : 0

  project   = gitlab_project.main.id
  link_url  = "${local.pages_base_url}/${gitlab_project.main.path}/htmlcov"
  image_url = "https://gitlab.com/%%{project_path}/badges/%%{default_branch}/coverage.svg"
}

/* Group Variables */

resource "gitlab_group_variable" "vars" {
  for_each = var.group_variables

  group     = data.gitlab_group.main.id
  key       = each.key
  value     = each.value.value
  protected = lookup(each.value, "protected", true)
  masked    = lookup(each.value, "masked", false)
}

/* Project Variables */

resource "gitlab_project_variable" "vars" {
  for_each = var.project_variables

  project           = gitlab_project.main.id
  key               = each.key
  value             = each.value.value
  protected         = lookup(each.value, "protected", true)
  masked            = lookup(each.value, "masked", false)
  environment_scope = lookup(each.value, "environment_scope", "*")
}
