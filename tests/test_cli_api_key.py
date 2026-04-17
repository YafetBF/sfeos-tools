"""Tests for CLI API key authentication support."""

import os
from unittest.mock import patch

from click.testing import CliRunner

from sfeos_tools.cli import cli
from sfeos_tools.cli_options import set_es_env_vars


class TestSetEsEnvVars:
    """Tests for set_es_env_vars function."""

    def test_set_es_env_vars_all_parameters(self):
        """Test setting all environment variables."""
        # Clear any existing env vars
        for key in [
            "ES_HOST",
            "ES_PORT",
            "ES_USE_SSL",
            "ES_USER",
            "ES_PASS",
            "ES_API_KEY",
        ]:
            os.environ.pop(key, None)

        set_es_env_vars(
            host="example.com",
            port=9200,
            use_ssl=True,
            user="testuser",
            password="testpass",
            api_key="test-api-key-123",
        )

        assert os.environ.get("ES_HOST") == "example.com"
        assert os.environ.get("ES_PORT") == "9200"
        assert os.environ.get("ES_USE_SSL") == "true"
        assert os.environ.get("ES_USER") == "testuser"
        assert os.environ.get("ES_PASS") == "testpass"
        assert os.environ.get("ES_API_KEY") == "test-api-key-123"

        # Cleanup
        for key in [
            "ES_HOST",
            "ES_PORT",
            "ES_USE_SSL",
            "ES_USER",
            "ES_PASS",
            "ES_API_KEY",
        ]:
            os.environ.pop(key, None)

    def test_set_es_env_vars_api_key_only(self):
        """Test setting only API key."""
        for key in [
            "ES_HOST",
            "ES_PORT",
            "ES_USE_SSL",
            "ES_USER",
            "ES_PASS",
            "ES_API_KEY",
        ]:
            os.environ.pop(key, None)

        set_es_env_vars(api_key="my-api-key")

        assert os.environ.get("ES_API_KEY") == "my-api-key"
        assert "ES_HOST" not in os.environ
        assert "ES_USER" not in os.environ

        # Cleanup
        os.environ.pop("ES_API_KEY", None)

    def test_set_es_env_vars_use_ssl_false(self):
        """Test setting use_ssl to False."""
        os.environ.pop("ES_USE_SSL", None)

        set_es_env_vars(use_ssl=False)

        assert os.environ.get("ES_USE_SSL") == "false"

        # Cleanup
        os.environ.pop("ES_USE_SSL", None)

    def test_set_es_env_vars_use_ssl_true(self):
        """Test setting use_ssl to True."""
        os.environ.pop("ES_USE_SSL", None)

        set_es_env_vars(use_ssl=True)

        assert os.environ.get("ES_USE_SSL") == "true"

        # Cleanup
        os.environ.pop("ES_USE_SSL", None)

    def test_set_es_env_vars_port_conversion(self):
        """Test that port is converted to string."""
        os.environ.pop("ES_PORT", None)

        set_es_env_vars(port=9202)

        assert os.environ.get("ES_PORT") == "9202"
        assert isinstance(os.environ.get("ES_PORT"), str)

        # Cleanup
        os.environ.pop("ES_PORT", None)


class TestAddBboxShapeCliApiKey:
    """Tests for add-bbox-shape CLI command with API key."""

    def test_add_bbox_shape_with_api_key(self):
        """Test add-bbox-shape command accepts --api-key option."""
        runner = CliRunner()

        with patch("sfeos_tools.cli.asyncio.run") as mock_run, patch(
            "sfeos_tools.cli.set_es_env_vars"
        ) as mock_set_vars:
            mock_run.return_value = None

            runner.invoke(
                cli,
                [
                    "add-bbox-shape",
                    "--backend",
                    "elasticsearch",
                    "--api-key",
                    "test-key-123",
                ],
            )

            # Verify the command was called with the API key
            mock_set_vars.assert_called_once()
            call_kwargs = mock_set_vars.call_args[1]
            assert call_kwargs["api_key"] == "test-key-123"

    def test_add_bbox_shape_sets_api_key_env_var(self):
        """Test that add-bbox-shape sets ES_API_KEY environment variable."""
        runner = CliRunner()

        with patch("sfeos_tools.cli.asyncio.run") as mock_run:
            mock_run.return_value = None

            runner.invoke(
                cli,
                [
                    "add-bbox-shape",
                    "--backend",
                    "elasticsearch",
                    "--api-key",
                    "my-secret-key",
                ],
            )

            # The env var should be set by set_es_env_vars
            assert os.environ.get("ES_API_KEY") == "my-secret-key"

            # Cleanup
            os.environ.pop("ES_API_KEY", None)

    def test_add_bbox_shape_with_multiple_options(self):
        """Test add-bbox-shape with host, port, and api-key."""
        runner = CliRunner()

        with patch("sfeos_tools.cli.asyncio.run") as mock_run, patch(
            "sfeos_tools.cli.set_es_env_vars"
        ) as mock_set_vars:
            mock_run.return_value = None

            runner.invoke(
                cli,
                [
                    "add-bbox-shape",
                    "--backend",
                    "elasticsearch",
                    "--host",
                    "db.example.com",
                    "--port",
                    "9200",
                    "--api-key",
                    "test-key",
                ],
            )

            mock_set_vars.assert_called_once()
            call_kwargs = mock_set_vars.call_args[1]
            assert call_kwargs["host"] == "db.example.com"
            assert call_kwargs["port"] == 9200
            assert call_kwargs["api_key"] == "test-key"


class TestReindexCliApiKey:
    """Tests for reindex CLI command with API key."""

    def test_reindex_with_api_key(self):
        """Test reindex command accepts --api-key option."""
        runner = CliRunner()

        with patch("sfeos_tools.cli.asyncio.run") as mock_run, patch(
            "sfeos_tools.cli.set_es_env_vars"
        ) as mock_set_vars:
            mock_run.return_value = None

            runner.invoke(
                cli,
                [
                    "reindex",
                    "--backend",
                    "elasticsearch",
                    "--api-key",
                    "reindex-key-456",
                    "--yes",
                ],
            )

            # Verify the command was called with the API key
            mock_set_vars.assert_called_once()
            call_kwargs = mock_set_vars.call_args[1]
            assert call_kwargs["api_key"] == "reindex-key-456"

    def test_reindex_sets_api_key_env_var(self):
        """Test that reindex sets ES_API_KEY environment variable."""
        runner = CliRunner()

        with patch("sfeos_tools.cli.asyncio.run") as mock_run:
            mock_run.return_value = None

            runner.invoke(
                cli,
                [
                    "reindex",
                    "--backend",
                    "opensearch",
                    "--api-key",
                    "opensearch-api-key",
                    "--yes",
                ],
            )

            # The env var should be set by set_es_env_vars
            assert os.environ.get("ES_API_KEY") == "opensearch-api-key"

            # Cleanup
            os.environ.pop("ES_API_KEY", None)

    def test_reindex_with_all_auth_options(self):
        """Test reindex with host, port, user, password, and api-key."""
        runner = CliRunner()

        with patch("sfeos_tools.cli.asyncio.run") as mock_run, patch(
            "sfeos_tools.cli.set_es_env_vars"
        ) as mock_set_vars:
            mock_run.return_value = None

            runner.invoke(
                cli,
                [
                    "reindex",
                    "--backend",
                    "elasticsearch",
                    "--host",
                    "prod.example.com",
                    "--port",
                    "9202",
                    "--api-key",
                    "prod-api-key",
                    "--yes",
                ],
            )

            mock_set_vars.assert_called_once()
            call_kwargs = mock_set_vars.call_args[1]
            assert call_kwargs["host"] == "prod.example.com"
            assert call_kwargs["port"] == 9202
            assert call_kwargs["api_key"] == "prod-api-key"


class TestIngestCatalogCliApiKey:
    """Tests for ingest-catalog CLI command with API key."""

    def test_ingest_catalog_with_api_key(self):
        """Test ingest-catalog command accepts --api-key option."""
        runner = CliRunner()

        # Create a temporary XML file for testing
        import tempfile

        with tempfile.NamedTemporaryFile(mode="w", suffix=".rdf", delete=False) as f:
            f.write('<?xml version="1.0"?><rdf:RDF></rdf:RDF>')
            temp_file = f.name

        try:
            with patch("sfeos_tools.cli.ingest_from_xml") as mock_ingest:
                runner.invoke(
                    cli,
                    [
                        "ingest-catalog",
                        "--xml-file",
                        temp_file,
                        "--api-key",
                        "catalog-api-key",
                    ],
                )

                # Verify the command was called with the API key
                mock_ingest.assert_called_once()
                call_kwargs = mock_ingest.call_args[1]
                assert call_kwargs["api_key"] == "catalog-api-key"
        finally:
            os.unlink(temp_file)

    def test_ingest_catalog_api_key_passed_to_function(self):
        """Test that ingest-catalog passes API key to ingest_from_xml."""
        runner = CliRunner()

        import tempfile

        with tempfile.NamedTemporaryFile(mode="w", suffix=".rdf", delete=False) as f:
            f.write('<?xml version="1.0"?><rdf:RDF></rdf:RDF>')
            temp_file = f.name

        try:
            with patch("sfeos_tools.cli.ingest_from_xml") as mock_ingest:
                runner.invoke(
                    cli,
                    [
                        "ingest-catalog",
                        "--xml-file",
                        temp_file,
                        "--stac-url",
                        "http://localhost:8080",
                        "--api-key",
                        "my-catalog-key",
                    ],
                )

                # Verify ingest_from_xml was called with correct parameters
                mock_ingest.assert_called_once()
                args, kwargs = mock_ingest.call_args
                assert args[0] == temp_file
                assert args[1] == "http://localhost:8080"
                assert kwargs.get("api_key") == "my-catalog-key"
        finally:
            os.unlink(temp_file)

    def test_ingest_catalog_rejects_both_auth_methods(self):
        """Test that ingest-catalog rejects both user/password and api-key together."""
        runner = CliRunner()

        import tempfile

        with tempfile.NamedTemporaryFile(mode="w", suffix=".rdf", delete=False) as f:
            f.write('<?xml version="1.0"?><rdf:RDF></rdf:RDF>')
            temp_file = f.name

        try:
            result = runner.invoke(
                cli,
                [
                    "ingest-catalog",
                    "--xml-file",
                    temp_file,
                    "--user",
                    "testuser",
                    "--password",
                    "testpass",
                    "--api-key",
                    "test-key",
                ],
            )

            # Verify the command failed with proper error message
            assert result.exit_code != 0
            assert "Authentication error" in result.output
            assert "user/password OR an api_key" in result.output
        finally:
            os.unlink(temp_file)

    def test_ingest_catalog_rejects_user_without_password(self):
        """Test that ingest-catalog rejects user without password."""
        runner = CliRunner()

        import tempfile

        with tempfile.NamedTemporaryFile(mode="w", suffix=".rdf", delete=False) as f:
            f.write('<?xml version="1.0"?><rdf:RDF></rdf:RDF>')
            temp_file = f.name

        try:
            result = runner.invoke(
                cli,
                [
                    "ingest-catalog",
                    "--xml-file",
                    temp_file,
                    "--user",
                    "testuser",
                ],
            )

            # Verify the command failed with proper error message
            assert result.exit_code != 0
            assert "Authentication error" in result.output
            assert "Both user AND password must be provided together" in result.output
        finally:
            os.unlink(temp_file)

    def test_ingest_catalog_rejects_password_without_user(self):
        """Test that ingest-catalog rejects password without user."""
        runner = CliRunner()

        import tempfile

        with tempfile.NamedTemporaryFile(mode="w", suffix=".rdf", delete=False) as f:
            f.write('<?xml version="1.0"?><rdf:RDF></rdf:RDF>')
            temp_file = f.name

        try:
            result = runner.invoke(
                cli,
                [
                    "ingest-catalog",
                    "--xml-file",
                    temp_file,
                    "--password",
                    "testpass",
                ],
            )

            # Verify the command failed with proper error message
            assert result.exit_code != 0
            assert "Authentication error" in result.output
            assert "Both user AND password must be provided together" in result.output
        finally:
            os.unlink(temp_file)
