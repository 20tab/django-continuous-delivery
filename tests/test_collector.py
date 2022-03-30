"""Project bootstrap tests."""

from contextlib import contextmanager
from io import StringIO
from unittest import TestCase, mock

from bootstrap.collector import (
    clean_gitlab_group_data,
    clean_media_storage,
    clean_project_dirname,
    clean_project_slug,
    clean_service_dir,
    clean_service_slug,
    clean_use_redis,
)


@contextmanager
def input(*cmds):
    """Mock the input."""
    visible_cmds = "\n".join([c for c in cmds if isinstance(c, str)])
    hidden_cmds = [c.get("hidden") for c in cmds if isinstance(c, dict)]
    with mock.patch("sys.stdin", StringIO(f"{visible_cmds}\n")), mock.patch(
        "getpass.getpass", side_effect=hidden_cmds
    ):
        yield


class TestBootstrapCollector(TestCase):
    """Test the bootstrap collector."""

    maxDiff = None

    def test_clean_gitlab_group_data(self):
        """Test cleaning the GitLab group data."""
        with input("Y"):
            self.assertEqual(
                clean_gitlab_group_data(
                    "my-project", "my-gitlab-group", "mYV4l1DT0k3N"
                ),
                ("my-gitlab-group", "mYV4l1DT0k3N"),
            )
        with input("Y", "my-gitlab-group", "Y"):
            self.assertEqual(
                clean_gitlab_group_data("my-project", None, "mYV4l1DT0k3N"),
                ("my-gitlab-group", "mYV4l1DT0k3N"),
            )
        with input("Y", "my-gitlab-group", "Y", {"hidden": "mYV4l1DT0k3N"}):
            self.assertEqual(
                clean_gitlab_group_data("my-project", None, None),
                ("my-gitlab-group", "mYV4l1DT0k3N"),
            )
        self.assertEqual(
            clean_gitlab_group_data("my-project", "", ""),
            ("", ""),
        )

    def test_clean_media_storage(self):
        """Test cleaning the media storage."""
        with input("local"):
            self.assertEqual(clean_media_storage(""), "local")

    def test_clean_project_dirname(self):
        """Test cleaning the project directory."""
        self.assertEqual(
            clean_project_dirname("tests", "my_project", "backend"), "tests"
        )
        with input("backend"):
            self.assertEqual(
                clean_project_dirname(None, "my_project", "backend"), "backend"
            )

    def test_clean_project_slug(self):
        """Test cleaning the project slug."""
        with input("My Project"):
            self.assertEqual(clean_project_slug("My Project", None), "my-project")
        project_slug = "my-new-project"
        self.assertEqual(
            clean_project_slug("My Project", "my-new-project"), project_slug
        )

    @mock.patch("pathlib.Path.is_absolute", return_value=True)
    def test_clean_service_dir(self, m):
        """Test cleaning the service directory."""
        self.assertTrue(
            clean_service_dir("tests", "my_project").endswith("/tests/my_project")
        )
        with mock.patch("shutil.rmtree", return_value=None), mock.patch(
            "pathlib.Path.is_dir", return_value=True
        ), input("Y"):
            self.assertTrue(
                clean_service_dir("tests", "my_project").endswith("/tests/my_project")
            )

    def test_clean_service_slug(self):
        """Test cleaning the back end service slug."""
        with input(""):
            self.assertEqual(clean_service_slug(""), "backend")
        with input("my backend"):
            self.assertEqual(clean_service_slug(""), "mybackend")

    def test_clean_use_redis(self):
        """Test cleaning the Sentry organization."""
        self.assertEqual(clean_use_redis("Y"), "Y")