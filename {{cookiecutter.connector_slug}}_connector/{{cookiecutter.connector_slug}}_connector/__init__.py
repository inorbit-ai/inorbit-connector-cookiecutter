# SPDX-FileCopyrightText: 2026 {{ cookiecutter.author }}
#
# SPDX-License-Identifier: MIT

"""Top-level package for InOrbit {{ cookiecutter.connector_target }} Connector."""

from importlib import metadata

__author__ = """InOrbit Inc."""
__email__ = "{{cookiecutter.email}}"
# Read the installed package version from metadata
try:
    __version__ = metadata.version("{{cookiecutter.project_slug}}")
except metadata.PackageNotFoundError:
    __version__ = "unknown"
