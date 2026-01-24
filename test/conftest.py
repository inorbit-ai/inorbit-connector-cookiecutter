# SPDX-FileCopyrightText: 2026 InOrbit, Inc.
#
# SPDX-License-Identifier: MIT

"""Test-wide fixtures for cookiecutter template tests."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def cookiecutter_template_dir():
    """Get the path to the cookiecutter template directory."""
    return Path(__file__).parent.parent


@pytest.fixture
def generated_project_dir(temp_dir, cookiecutter_template_dir):
    """Generate a cookiecutter project and return its path."""
    output_dir = temp_dir / "output"
    output_dir.mkdir()

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "cookiecutter",
            str(cookiecutter_template_dir),
            "--no-input",
            "-o",
            str(output_dir),
            "python_version=3.13",
            "use_current_directory=n",
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    generated_dir = output_dir / "wall_e_fleet_connector"
    assert generated_dir.exists(), (
        f"Generated project not found. "
        f"Output: {result.stdout}\nError: {result.stderr}"
    )

    return generated_dir


@pytest.fixture
def git_repo(temp_dir):
    """Create a git repository in a temporary directory."""
    repo_dir = temp_dir / "git_repo"
    repo_dir.mkdir()

    subprocess.run(
        ["git", "init"],
        cwd=repo_dir,
        check=True,
        capture_output=True,
    )

    subprocess.run(
        ["git", "config", "user.name", "Test User"],
        cwd=repo_dir,
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=repo_dir,
        check=True,
        capture_output=True,
    )

    return repo_dir
