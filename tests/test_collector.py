"""Bootstrap collector tests."""

import os
from pathlib import Path
from shutil import rmtree
from unittest import TestCase, mock

from bootstrap.collector import Collector

from tests.utils import mock_input


class TestBootstrapCollector(TestCase):
    """Test the bootstrap collector."""

    maxDiff = None

    def setUp(self):
        """Setup the test data."""
        self.output_dir = Path("./tests/test_files")
        rmtree(self.output_dir, ignore_errors=True)
        return super().setUp()

    def tearDown(self):
        """Cleanup after each test."""
        rmtree(self.output_dir, ignore_errors=True)
        return super().tearDown()

    def test_collect(self):
        """Test collect options."""
        collector = Collector(
            project_name="project_name",
        )
        collector.set_project_dirname = mock.MagicMock()
        collector.set_project_slug = mock.MagicMock()
        collector.set_service_slug = mock.MagicMock()
        collector.set_project_urls = mock.MagicMock()
        collector.set_project_dirname = mock.MagicMock()
        collector.set_service_dir = mock.MagicMock()
        collector.set_use_redis = mock.MagicMock()
        collector.set_terraform = mock.MagicMock()
        collector.set_vault = mock.MagicMock()
        collector.set_deployment_type = mock.MagicMock()
        collector.set_environments_distribution = mock.MagicMock()
        collector.set_project_urls = mock.MagicMock()
        collector.set_sentry = mock.MagicMock()
        collector.set_gitlab = mock.MagicMock()
        collector.set_media_storage = mock.MagicMock()
        collector.collect()
        collector.set_project_slug.assert_called_once()
        collector.set_project_dirname.assert_called_once()
        collector.set_service_dir.assert_called_once()
        collector.set_use_redis.assert_called_once()
        collector.set_terraform.assert_called_once()
        collector.set_vault.assert_called_once()
        collector.set_deployment_type.assert_called_once()
        collector.set_environments_distribution.assert_called_once()
        collector.set_project_urls.assert_called_once()
        collector.set_sentry.assert_called_once()
        collector.set_gitlab.assert_called_once()
        collector.set_media_storage.assert_called_once()

    def test_environments_distribution_for_other_k8s_deployment(self):
        """Test collecting the environments distribution for other-k8s deployment."""
        collector = Collector(project_name="project_name", deployment_type="other-k8s")
        self.assertIsNone(collector.environments_distribution)
        with mock.patch("bootstrap.collector.click.prompt") as mocked_prompt:
            collector.set_environments_distribution()
        self.assertEqual(collector.environments_distribution, "1")
        mocked_prompt.assert_not_called()

    def test_environments_distribution_from_default(self):
        """Test collecting the environments distribution from its default value."""
        collector = Collector(
            project_name="project_name",
        )
        self.assertIsNone(collector.environments_distribution)
        with mock_input(""):
            collector.set_environments_distribution()
        self.assertEqual(collector.environments_distribution, "1")

    def test_environments_distribution_from_input(self):
        """Test collecting the environments distribution from user input."""
        collector = Collector(
            project_name="project_name",
        )
        self.assertIsNone(collector.environments_distribution)
        with mock_input("one", "yet-another-bad-value", "3"):
            collector.set_environments_distribution()
        self.assertEqual(collector.environments_distribution, "3")

    def test_environments_distribution_from_options(self):
        """Test collecting the environments distribution from the collected options."""
        collector = Collector(
            project_name="project_name", environments_distribution="2"
        )
        self.assertEqual(collector.environments_distribution, "2")
        with mock.patch("bootstrap.collector.click.prompt") as mocked_prompt:
            collector.set_environments_distribution()
        self.assertEqual(collector.environments_distribution, "2")
        mocked_prompt.assert_not_called()

    def test_deployment_type_from_default(self):
        """Test collecting the deployment type from its default value."""
        collector = Collector(
            project_name="project_name",
        )
        self.assertIsNone(collector.deployment_type)
        with mock_input(""):
            collector.set_deployment_type()
        self.assertEqual(collector.deployment_type, "digitalocean-k8s")

    def test_deployment_type_from_input(self):
        """Test collecting the deployment type from user input."""
        collector = Collector(
            project_name="project_name",
        )
        self.assertIsNone(collector.deployment_type)
        with mock_input("bad-deployment-type", "yet-another-bad-value", "other-k8s"):
            collector.set_deployment_type()
        self.assertEqual(collector.deployment_type, "other-k8s")

    def test_deployment_type_from_options(self):
        """Test collecting the deployment type from the collected options."""
        collector = Collector(project_name="project_name", deployment_type="other-k8s")
        self.assertEqual(collector.deployment_type, "other-k8s")
        with mock.patch("bootstrap.collector.click.prompt") as mocked_prompt:
            collector.set_deployment_type()
        self.assertEqual(collector.deployment_type, "other-k8s")
        mocked_prompt.assert_not_called()

    def test_gitlab_no(self):
        """Test not setting Gitlab."""
        collector = Collector(project_name="project_name", gitlab_url="")
        with mock_input("n"):
            collector.set_gitlab()
        self.assertEqual(collector.gitlab_url, "")

    def test_gitlab_default(self):
        """Test setting Gitlab options from default."""
        collector = Collector(
            project_name="project_name", project_slug="gitlab-project"
        )
        self.assertIsNone(collector.gitlab_url)
        self.assertIsNone(collector.gitlab_token)
        self.assertIsNone(collector.gitlab_namespace_path)
        with mock_input("y", "", {"hidden": "G1tl4b_Tok3n!"}, "namespacepath"):
            collector.set_gitlab()
        self.assertEqual(collector.gitlab_url, "https://gitlab.com")
        self.assertEqual(collector.gitlab_token, "G1tl4b_Tok3n!")
        self.assertEqual(collector.gitlab_namespace_path, "namespacepath")

    def test_gitlab_input(self):
        """Test setting Gitlab options from input."""
        collector = Collector(
            project_name="project_name",
        )
        self.assertIsNone(collector.gitlab_url)
        self.assertIsNone(collector.gitlab_token)
        self.assertIsNone(collector.gitlab_namespace_path)
        with mock_input(
            "y",
            "https://gitlab.custom-domain.com",
            {"hidden": "input-G1tl4b_Tok3n!"},
            "inputnamespacepath",
        ):
            collector.set_gitlab()
        self.assertEqual(collector.gitlab_url, "https://gitlab.custom-domain.com")
        self.assertEqual(collector.gitlab_token, "input-G1tl4b_Tok3n!")
        self.assertEqual(collector.gitlab_namespace_path, "inputnamespacepath")

    def test_gitlab_options(self):
        """Test setting Gitlab options from options."""
        collector = Collector(
            project_name="project_name",
            gitlab_url="https://gitlab.custom-domain.com",
            gitlab_token="input-G1tl4b_Tok3n!",
            gitlab_namespace_path="inputnamespacepath",
        )
        self.assertEqual(collector.gitlab_url, "https://gitlab.custom-domain.com")
        self.assertEqual(collector.gitlab_token, "input-G1tl4b_Tok3n!")
        self.assertEqual(collector.gitlab_namespace_path, "inputnamespacepath")
        collector.set_gitlab()
        self.assertEqual(collector.gitlab_url, "https://gitlab.custom-domain.com")
        self.assertEqual(collector.gitlab_token, "input-G1tl4b_Tok3n!")
        self.assertEqual(collector.gitlab_namespace_path, "inputnamespacepath")

    def test_project_dirname(self):
        """Test collecting the project dirname."""
        collector = Collector(project_slug="project-slug", service_slug="service-slug")
        self.assertIsNone(collector.project_dirname)
        with mock_input("service-slug"):
            collector.set_project_dirname()
        self.assertEqual(collector.project_dirname, "service-slug")

    def test_project_urls_from_default(self):
        """Test collecting the domain and urls options from default."""
        collector = Collector(project_name="project_name", project_slug="test-project")
        self.assertIsNone(collector.project_url_dev)
        self.assertIsNone(collector.project_url_stage)
        self.assertIsNone(collector.project_url_prod)
        with mock_input("", "", ""):
            collector.set_project_urls()
        self.assertEqual(collector.project_url_dev, "https://dev.test-project.com")
        self.assertEqual(collector.project_url_stage, "https://stage.test-project.com")
        self.assertEqual(collector.project_url_prod, "https://www.test-project.com")

    def test_project_urls_from_input(self):
        """Test collecting the domain and urls options from input."""
        collector = Collector(project_name="project_name", project_slug="test-project")
        self.assertIsNone(collector.project_url_dev)
        self.assertIsNone(collector.project_url_stage)
        self.assertIsNone(collector.project_url_prod)
        with mock_input(
            "bad domain.com",
            "https://dev-from-input.domain.com",
            "dev from input",
            "https://dev-from-input.domain.com",
            "prod-from-input             ",
            "https://prod-from-input.domain.com",
        ):
            collector.set_project_urls()
        self.assertEqual(collector.project_url_dev, "https://dev-from-input.domain.com")
        self.assertEqual(
            collector.project_url_stage, "https://dev-from-input.domain.com"
        )
        self.assertEqual(
            collector.project_url_prod, "https://prod-from-input.domain.com"
        )

    def test_project_urls_from_options(self):
        """Test collecting the domain and urls options from input."""
        collector = Collector(
            project_url_dev="https://dev.domain.com",
            project_url_stage="https://stage.domain.com",
            project_url_prod="https://www.domain.com",
        )
        self.assertEqual(collector.project_url_dev, "https://dev.domain.com")
        self.assertEqual(collector.project_url_stage, "https://stage.domain.com")
        self.assertEqual(collector.project_url_prod, "https://www.domain.com")
        with mock.patch("bootstrap.collector.click.prompt") as mocked_prompt:
            collector.set_project_urls()
        self.assertEqual(collector.project_url_dev, "https://dev.domain.com")
        self.assertEqual(collector.project_url_stage, "https://stage.domain.com")
        self.assertEqual(collector.project_url_prod, "https://www.domain.com")
        mocked_prompt.assert_not_called()

    def test_project_slug_from_default(self):
        """Test collecting the project slug from its default value."""
        collector = Collector(project_name="My Project")
        self.assertIsNone(collector.project_slug)
        with mock_input(""):
            collector.set_project_slug()
        self.assertEqual(collector.project_slug, "my-project")

    def test_project_slug_from_input(self):
        """Test collecting the project slug from user input."""
        collector = Collector(project_name="Test Project")
        self.assertIsNone(collector.project_slug)
        with mock_input("My New Project Slug"):
            collector.set_project_slug()
        self.assertEqual(collector.project_slug, "my-new-project-slug")

    def test_project_slug_from_options(self):
        """Test collecting the project slug from the collected options."""
        collector = Collector(
            project_name="My Project",
            project_slug="my-new-project",
        )
        self.assertEqual(collector.project_slug, "my-new-project")
        with mock.patch("bootstrap.collector.click.prompt") as mocked_prompt:
            collector.set_project_slug()
        self.assertEqual(collector.project_slug, "my-new-project")
        mocked_prompt.assert_not_called()

    def test_redis_from_input(self):
        """Test setting the `use_redis` flag from user input."""
        collector = Collector(
            project_name="project_name",
        )
        self.assertIsNone(collector.use_redis)
        with mock_input("y"):
            collector.set_use_redis()
        self.assertTrue(collector.use_redis)

    def test_redis_from_options(self):
        """Test setting the `use_redis` flag from user input."""
        collector = Collector(project_name="project_name", use_redis=False)
        self.assertFalse(collector.use_redis)
        with mock.patch("bootstrap.collector.click.confirm") as mocked_confirm:
            collector.set_use_redis()
        self.assertFalse(collector.use_redis)
        mocked_confirm.assert_not_called()

    def test_launch_runner(self):
        """Test launching the runner."""
        collector = Collector(
            project_name="project_name",
        )
        runner = mock.MagicMock()
        collector.get_runner = mock.MagicMock(return_value=runner)
        collector.launch_runner()
        runner.run.assert_called_once()

    def test_get_runner(self):
        """Test getting the runner."""
        collector = Collector(
            deployment_type="digitalocean-k8s",
            environments_distribution="1",
            internal_service_port=8000,
            media_storage="local",
            project_dirname="project_dirname",
            project_name="Test Project",
            project_slug="test-project",
            project_url_dev="https://dev.test.com",
            project_url_prod="https://www.test.com",
            project_url_stage="https://stage.test.com",
            service_slug="django",
            terraform_backend="terraform-cloud",
            use_redis=False,
        )
        collector._service_dir = Path(".")
        runner = collector.get_runner()

        self.assertEqual(runner.deployment_type, "digitalocean-k8s")
        self.assertEqual(runner.environments_distribution, "1")
        self.assertEqual(runner.internal_service_port, 8000)
        self.assertEqual(runner.media_storage, "local")
        self.assertEqual(runner.project_dirname, "project_dirname")
        self.assertEqual(runner.project_name, "Test Project")
        self.assertEqual(runner.project_slug, "test-project")
        self.assertEqual(runner.project_url_dev, "https://dev.test.com")
        self.assertEqual(runner.project_url_prod, "https://www.test.com")
        self.assertEqual(runner.project_url_stage, "https://stage.test.com")
        self.assertEqual(runner.service_slug, "django")
        self.assertEqual(runner.terraform_backend, "terraform-cloud")
        self.assertEqual(runner.use_redis, False)

    def test_sentry_no(self):
        """Test not setting Sentry."""
        collector = Collector(
            project_name="project_name",
        )
        self.assertIsNone(collector.sentry_org)
        with mock_input("n"):
            collector.set_sentry()
        self.assertIsNone(collector.sentry_org)

    def test_sentry_default(self):
        """Test setting Sentry options from default."""
        collector = Collector(project_name="project_name")
        self.assertIsNone(collector.sentry_org)
        self.assertIsNone(collector.sentry_url)
        with mock_input(
            "y",
            "sentry-input-organization",
            "",
            "https://backend.sentry.dsn",
        ):
            collector.set_sentry()
        self.assertEqual(collector.sentry_org, "sentry-input-organization")
        self.assertEqual(collector.sentry_url, "https://sentry.io")
        self.assertEqual(collector.sentry_dsn, "https://backend.sentry.dsn")

    def test_sentry_options(self):
        """Test setting Sentry options from options."""
        collector = Collector(
            project_name="project_name",
            sentry_org="sentry-options-organization",
            sentry_url="https://other-sentry-url.com",
            sentry_dsn="https://backend.sentry.dsn",
        )
        self.assertEqual(collector.sentry_org, "sentry-options-organization")
        self.assertEqual(collector.sentry_url, "https://other-sentry-url.com")
        collector.set_sentry()
        self.assertEqual(collector.sentry_org, "sentry-options-organization")
        self.assertEqual(collector.sentry_url, "https://other-sentry-url.com")

    def test_storage_input(self):
        """Test setting storage options from input."""
        collector = Collector(
            project_name="project_name",
        )
        with mock_input("aws-s3"):
            collector.set_media_storage()
        self.assertEqual(collector.media_storage, "aws-s3")

    def test_storage_input_local(self):
        """Test setting storage options from input."""
        collector = Collector(
            project_name="project_name",
        )
        with mock_input("local"):
            collector.set_media_storage()
        self.assertEqual(collector.media_storage, "local")

    def test_storage_options(self):
        """Test setting storage options from options."""
        collector = Collector(project_name="project_name", media_storage="aws-s3")
        self.assertEqual(collector.media_storage, "aws-s3")
        with mock_input("2"):
            collector.set_media_storage()
        self.assertEqual(collector.media_storage, "aws-s3")

    def test_service_slug_default(self):
        """Test setting the service slug from default."""
        collector = Collector(
            project_name="project_name",
        )
        self.assertIsNone(collector.service_slug)
        with mock_input(""):
            collector.set_service_slug()
        self.assertEqual(collector.service_slug, "backend")

    def test_service_slug_input(self):
        """Test setting the service slug from input."""
        collector = Collector(
            project_name="project_name",
        )
        self.assertIsNone(collector.service_slug)
        with mock_input("input-slug"):
            collector.set_service_slug()
        self.assertEqual(collector.service_slug, "input-slug")

    def test_service_slug_options(self):
        """Test setting the service slug from options."""
        collector = Collector(
            project_name="project_name", service_slug="service-slug-options"
        )
        self.assertEqual(collector.service_slug, "service-slug-options")
        with mock_input("asdadsa"):
            collector.set_service_slug()
        self.assertEqual(collector.service_slug, "service-slug-options")

    def test_service_dir_new(self):
        """Test service dir with a new folder."""
        collector = Collector(
            project_name="project_name",
            output_dir=str(self.output_dir.resolve()),
            project_dirname="test_project",
        )
        service_dir = self.output_dir / "test_project"
        collector.set_service_dir()
        self.assertFalse(os.path.exists(service_dir))
        self.assertEqual(collector._service_dir, service_dir.resolve())

    def test_service_dir_already_exists(self):
        """Test service dir with a new folder."""
        collector = Collector(
            project_name="project_name",
            output_dir=str(self.output_dir.resolve()),
            project_dirname="test_project",
        )
        service_dir = self.output_dir / "test_project"
        os.makedirs(service_dir, exist_ok=True)
        with mock_input("y"):
            collector.set_service_dir()
        self.assertFalse(os.path.exists(service_dir))
        self.assertEqual(collector._service_dir, service_dir.resolve())

    def test_terraform_backend_from_default(self):
        """Test setting the Terraform backend from its default value."""
        collector = Collector(
            project_name="project_name",
        )
        self.assertIsNone(collector.terraform_backend)
        collector.set_terraform_cloud = mock.MagicMock()
        with mock_input(""):
            collector.set_terraform()
        self.assertEqual(collector.terraform_backend, "terraform-cloud")
        collector.set_terraform_cloud.assert_called_once()

    def test_terraform_backend_from_input(self):
        """Test setting the Terraform backend from user input."""
        collector = Collector(
            project_name="project_name",
        )
        self.assertIsNone(collector.terraform_backend)
        collector.set_terraform_cloud = mock.MagicMock()
        with mock_input("bad-tf-backend", "another-bad-tf-backend", "gitlab"):
            collector.set_terraform()
        self.assertEqual(collector.terraform_backend, "gitlab")
        collector.set_terraform_cloud.assert_not_called()

    def test_terraform_backend_from_options(self):
        """Test setting the Terraform backend from the collected options."""
        collector = Collector(
            project_name="project_name", terraform_backend="terraform-cloud"
        )
        self.assertEqual(collector.terraform_backend, "terraform-cloud")
        collector.set_terraform_cloud = mock.MagicMock()
        with mock.patch("bootstrap.collector.click") as mocked_click:
            collector.set_terraform()
        self.assertEqual(collector.terraform_backend, "terraform-cloud")
        mocked_click.prompt.assert_not_called()
        collector.set_terraform_cloud.assert_called_once()

    def test_terraform_cloud_from_input(self):
        """Test setting up Terraform Cloud from user input."""
        collector = Collector(
            project_name="project_name", terraform_backend="terraform-cloud"
        )
        self.assertIsNone(collector.terraform_cloud_hostname)
        self.assertIsNone(collector.terraform_cloud_token)
        self.assertIsNone(collector.terraform_cloud_organization)
        self.assertIsNone(collector.terraform_cloud_organization_create)
        self.assertIsNone(collector.terraform_cloud_admin_email)
        with mock_input(
            "",
            {"hidden": "mytfcT0k3N"},
            "myTFCOrg",
            "y",
            "bad-email",
            "admin@test.com",
        ):
            collector.set_terraform_cloud()
        self.assertEqual(collector.terraform_cloud_hostname, "app.terraform.io")
        self.assertEqual(collector.terraform_cloud_token, "mytfcT0k3N")
        self.assertEqual(collector.terraform_cloud_organization, "myTFCOrg")
        self.assertTrue(collector.terraform_cloud_organization_create)
        self.assertEqual(collector.terraform_cloud_admin_email, "admin@test.com")

    def test_terraform_cloud_from_options(self):
        """Test setting up Terraform Cloud from the collected options."""
        collector = Collector(
            project_name="project_name",
            terraform_backend="terraform-cloud",
            terraform_cloud_hostname="app.terraform.io",
            terraform_cloud_token="mytfcT0k3N",
            terraform_cloud_organization="myTFCOrg",
            terraform_cloud_organization_create=True,
            terraform_cloud_admin_email="admin@test.com",
        )
        self.assertEqual(collector.terraform_cloud_hostname, "app.terraform.io")
        self.assertEqual(collector.terraform_cloud_token, "mytfcT0k3N")
        self.assertEqual(collector.terraform_cloud_organization, "myTFCOrg")
        self.assertTrue(collector.terraform_cloud_organization_create)
        self.assertEqual(collector.terraform_cloud_admin_email, "admin@test.com")
        with mock.patch("bootstrap.collector.click") as mocked_click:
            collector.set_terraform_cloud()
        self.assertEqual(collector.terraform_cloud_hostname, "app.terraform.io")
        self.assertEqual(collector.terraform_cloud_token, "mytfcT0k3N")
        self.assertEqual(collector.terraform_cloud_organization, "myTFCOrg")
        self.assertTrue(collector.terraform_cloud_organization_create)
        self.assertEqual(collector.terraform_cloud_admin_email, "admin@test.com")
        mocked_click.prompt.assert_not_called()

    def test_terraform_cloud_from_input_and_options(self):
        """Test setting up Terraform Cloud from options and user input."""
        collector = Collector(
            project_name="project_name",
            terraform_backend="terraform-cloud",
            terraform_cloud_token="mytfcT0k3N",
        )
        self.assertIsNone(collector.terraform_cloud_hostname)
        self.assertEqual(collector.terraform_cloud_token, "mytfcT0k3N")
        self.assertIsNone(collector.terraform_cloud_organization)
        self.assertIsNone(collector.terraform_cloud_organization_create)
        self.assertIsNone(collector.terraform_cloud_admin_email)
        with mock_input("tfc.my-company.com", "myTFCOrg", "n"):
            collector.set_terraform_cloud()
        self.assertEqual(collector.terraform_cloud_hostname, "tfc.my-company.com")
        self.assertEqual(collector.terraform_cloud_token, "mytfcT0k3N")
        self.assertEqual(collector.terraform_cloud_organization, "myTFCOrg")
        self.assertFalse(collector.terraform_cloud_organization_create)
        self.assertEqual(collector.terraform_cloud_admin_email, "")

    def test_vault_no(self):
        """Test not setting vault."""
        collector = Collector(
            project_name="project_name",
        )
        self.assertIsNone(collector.vault_token)
        self.assertIsNone(collector.vault_url)
        with mock_input("n"):
            collector.set_vault()
        self.assertIsNone(collector.vault_token)

    def test_vault_from_input(self):
        """Test setting up Vault from user input."""
        collector = Collector(
            project_name="project_name",
        )
        self.assertIsNone(collector.vault_token)
        self.assertIsNone(collector.vault_url)
        with mock_input(
            {"hidden": "v4UlTtok3N"},
            "https://vault.test.com",
        ), mock.patch(
            "bootstrap.collector.click.confirm", return_value=True
        ) as mocked_confirm:
            collector.set_vault()
        self.assertEqual(collector.vault_token, "v4UlTtok3N")
        self.assertEqual(collector.vault_url, "https://vault.test.com")
        self.assertEqual(len(mocked_confirm.mock_calls), 2)

    def test_vault_from_options(self):
        """Test setting up Vault from the collected options."""
        collector = Collector(
            project_name="project_name",
            vault_token="v4UlTtok3N",
            vault_url="https://vault.test.com",
        )
        self.assertEqual(collector.vault_token, "v4UlTtok3N")
        self.assertEqual(collector.vault_url, "https://vault.test.com")
        with mock.patch(
            "bootstrap.collector.click.confirm", return_value=True
        ) as mocked_confirm:
            collector.set_vault()
        self.assertEqual(collector.vault_token, "v4UlTtok3N")
        self.assertEqual(collector.vault_url, "https://vault.test.com")
        self.assertEqual(len(mocked_confirm.mock_calls), 1)

    def test_vault_from_input_and_options(self):
        """Test setting up Vault from options and user input."""
        collector = Collector(
            project_name="project_name", vault_url="https://vault.test.com"
        )
        self.assertIsNone(collector.vault_token)
        self.assertEqual(collector.vault_url, "https://vault.test.com")
        with mock_input({"hidden": "v4UlTtok3N"}), mock.patch(
            "bootstrap.collector.click.confirm", return_value=True
        ) as mocked_confirm:
            collector.set_vault()
        self.assertEqual(collector.vault_token, "v4UlTtok3N")
        self.assertEqual(collector.vault_url, "https://vault.test.com")
        self.assertEqual(len(mocked_confirm.mock_calls), 1)
