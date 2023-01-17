"""Bootstrap helpers tests."""
import json
import os
from pathlib import Path
from time import time
from unittest import TestCase, mock


from bootstrap.helpers import (
    format_gitlab_variable,
    format_tfvar,
    slugify_option,
    validate_or_prompt_domain,
    validate_or_prompt_path,
    validate_or_prompt_url,
)
from tests.utils import mock_input


class GitlabVariableTestcase(TestCase):
    """Test the 'format_gitlab_varialbe' function."""

    def test_gitlab_variable_unmasked_unprotected(self):
        """Test the formatting of a gitlab unmasked, unprotected variable."""
        self.assertEqual(
            format_gitlab_variable("value", False, False),
            '{ value = "value", protected = false }',
        )

    def test_gitlab_variable_masked_unprotected(self):
        """Test the formatting of a gitlab masked, unprotected variable."""
        self.assertEqual(
            format_gitlab_variable("value", True, False),
            '{ value = "value", masked = true, protected = false }',
        )

    def test_gitlab_variable_unmasked_protected(self):
        """Test the formatting of a gitlab unmasked, protected variable."""
        self.assertEqual(
            format_gitlab_variable("value", False, True), '{ value = "value" }'
        )

    def test_gitlab_variable_masked_protected(self):
        """Test the formatting of a gitlab masked, unprotected variable."""
        self.assertEqual(
            format_gitlab_variable("value", True, True),
            '{ value = "value", masked = true }',
        )


class FormatTFVarTestCase(TestCase):
    """Test the 'format_tfvar' function."""

    def test_format_list(self):
        """Test the function formats a list properly."""
        self.assertEqual(format_tfvar([1, 2, 3], "list"), '["1", "2", "3"]')

    def test_format_bool(self):
        """Test the function formats a boolean properly."""
        self.assertEqual(format_tfvar(True, "bool"), "true")

    def test_format_number(self):
        """Test the function formats a number properly."""
        self.assertEqual(format_tfvar(6, "num"), "6")

    def test_format_default(self):
        """Test the function formats a boolean properly."""
        self.assertEqual(format_tfvar("something else", "default"), '"something else"')


class OptionSlugifyTestCase(TestCase):
    """Test the 'option_slugify' function."""

    def test_slugify_with_value(self):
        """Test slugifying with a value."""
        self.assertEqual(
            slugify_option(None, None, "Text to slugify"), "text-to-slugify"
        )

    def test_slugify_no_value(self):
        """Test slugifying without a value."""
        self.assertEqual(slugify_option(None, None, None), None)


class ValidatePromptDomain(TestCase):
    """Test the 'validate_or_prompt_domain' function."""

    def test_validate_good(self):
        """Test validation of a good domain."""
        self.assertEqual(
            validate_or_prompt_domain("message", "www.google.com"), "www.google.com"
        )

    def test_validate_bad(self):
        """Test validation of a bad domain."""
        with mock_input("www.test.com"):
            self.assertEqual(
                validate_or_prompt_domain("message", "www. google .com"),
                "www.test.com",
            )

    def test_validate_no_value(self):
        """Test validation without a domain."""
        with mock_input("www google com", "www.google.com"):
            self.assertEqual(
                validate_or_prompt_domain("message", None), "www.google.com"
            )


class ValidatePromptUrl(TestCase):
    """Test the 'validate_or_prompt_url' function."""

    def test_validate_good(self):
        """Test validation of a good URL."""
        self.assertEqual(
            validate_or_prompt_url("message", "https://www.google.com"),
            "https://www.google.com",
        )

    def test_validate_bad(self):
        """Test validation of a bad URL."""
        with mock_input("https://www.google.com"):
            self.assertEqual(
                validate_or_prompt_url("message", "https://www. google .com"),
                "https://www.google.com",
            )

    def test_validate_no_value(self):
        """Test validation with no starting value."""
        with mock_input("www google com", "www.google.com", "https://www.google.com"):
            self.assertEqual(
                validate_or_prompt_url("message", None), "https://www.google.com"
            )


class ValidatePromptPath(TestCase):
    """Test the 'validate_or_prompt_path' function."""

    def test_validate_good(self):
        """Test validation of a good path."""
        self.assertEqual(validate_or_prompt_path("message", "/app"), "/app")

    def test_validate_bad(self):
        """Test validation of a bad path."""
        with mock_input("app"):
            self.assertEqual(validate_or_prompt_path("message", "// app / "), "app")

    def test_validate_no_value(self):
        """Test validation with no starting value."""
        with mock_input("app"):
            self.assertEqual(validate_or_prompt_path("message", None), "app")
