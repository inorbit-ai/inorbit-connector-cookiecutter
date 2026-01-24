# SPDX-FileCopyrightText: 2026 InOrbit, Inc.
#
# SPDX-License-Identifier: MIT

"""Tests for Makefile version bumping functionality in generated projects."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


def _setup_project(project_path: Path, generated_project_dir: Path) -> None:
    """Copy project to git repo and make initial commit."""
    shutil.copytree(generated_project_dir, project_path)
    subprocess.run(
        ["git", "add", "."],
        cwd=project_path,
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "commit", "-m", "Initial commit"],
        cwd=project_path,
        check=True,
        capture_output=True,
    )


def _run_bump(project_path: Path, part: str = "patch", **kwargs):
    """Run make bump command."""
    cmd = ["make", f"bump-{part}"]
    for key, value in kwargs.items():
        cmd.append(f"{key}={value}")
    return subprocess.run(
        cmd, cwd=project_path, capture_output=True, text=True
    )


class TestMakefileVersionBump:
    """Test Makefile version bumping commands."""

    def test_bump_patch(self, generated_project_dir, git_repo):
        """Test that make bump-patch increments patch version."""
        project_path = git_repo / generated_project_dir.name
        _setup_project(project_path, generated_project_dir)

        pyproject = project_path / "pyproject.toml"
        assert 'version = "0.1.0"' in pyproject.read_text()

        result = _run_bump(project_path, "patch")
        result.check_returncode()

        assert 'version = "0.1.1"' in pyproject.read_text()

        # Verify git commit
        log = subprocess.run(
            ["git", "log", "-1", "--pretty=format:%s"],
            cwd=project_path,
            capture_output=True,
            text=True,
            check=True,
        )
        expected = "Bump wall-e-fleet-connector version: 0.1.0 → 0.1.1"
        assert expected in log.stdout

        # Verify tag
        tags = subprocess.run(
            ["git", "tag", "-l"],
            cwd=project_path,
            capture_output=True,
            text=True,
            check=True,
        )
        assert "wall-e-fleet-connector-v0.1.1" in tags.stdout

    def test_bump_minor(self, generated_project_dir, git_repo):
        """Test that make bump-minor increments minor version."""
        project_path = git_repo / generated_project_dir.name
        _setup_project(project_path, generated_project_dir)

        result = _run_bump(project_path, "minor")
        result.check_returncode()

        pyproject = project_path / "pyproject.toml"
        assert 'version = "0.2.0"' in pyproject.read_text()

    def test_bump_major(self, generated_project_dir, git_repo):
        """Test that make bump-major increments major version."""
        project_path = git_repo / generated_project_dir.name
        _setup_project(project_path, generated_project_dir)

        result = _run_bump(project_path, "major")
        result.check_returncode()

        pyproject = project_path / "pyproject.toml"
        assert 'version = "1.0.0"' in pyproject.read_text()

    def test_bump_dry_run(self, generated_project_dir, git_repo):
        """Test that make bump DRY=1 does not make changes."""
        project_path = git_repo / generated_project_dir.name
        _setup_project(project_path, generated_project_dir)

        pyproject = project_path / "pyproject.toml"
        initial_content = pyproject.read_text()

        result = _run_bump(project_path, "patch", DRY=1)
        result.check_returncode()

        assert pyproject.read_text() == initial_content

        # Verify no new commit
        log = subprocess.run(
            ["git", "log", "--oneline"],
            cwd=project_path,
            capture_output=True,
            text=True,
            check=True,
        )
        assert log.stdout.count("\n") == 1  # Only initial commit

        # Verify no tag
        tags = subprocess.run(
            ["git", "tag", "-l"],
            cwd=project_path,
            capture_output=True,
            text=True,
            check=True,
        )
        assert tags.stdout.strip() == ""

    def test_bump_requires_clean_working_tree(
        self, generated_project_dir, git_repo
    ):
        """Test that bump fails with dirty working tree."""
        project_path = git_repo / generated_project_dir.name
        _setup_project(project_path, generated_project_dir)

        # Create uncommitted change
        (project_path / "README.md").write_text("Modified content")

        result = _run_bump(project_path, "patch")

        assert result.returncode != 0
        output = result.stdout + result.stderr
        assert "Working tree must be clean" in output

    def test_bump_allows_dirty_with_flag(
        self, generated_project_dir, git_repo
    ):
        """Test that bump works with DIRTY=1 flag."""
        project_path = git_repo / generated_project_dir.name
        _setup_project(project_path, generated_project_dir)

        # Create uncommitted change
        (project_path / "README.md").write_text("Modified content")

        result = _run_bump(project_path, "patch", DIRTY=1)
        result.check_returncode()

        pyproject = project_path / "pyproject.toml"
        assert 'version = "0.1.1"' in pyproject.read_text()

    def test_bump_updates_uv_lock(self, generated_project_dir, git_repo):
        """Test that uv.lock is updated and committed."""
        project_path = git_repo / generated_project_dir.name
        _setup_project(project_path, generated_project_dir)

        result = _run_bump(project_path, "patch")
        result.check_returncode()

        # Verify lock file change is in the commit
        diff = subprocess.run(
            ["git", "diff", "HEAD~1", "HEAD", "--", "uv.lock"],
            cwd=project_path,
            capture_output=True,
            text=True,
            check=True,
        )
        assert len(diff.stdout) > 0

    def test_bump_tag_format(self, generated_project_dir, git_repo):
        """Test that tags follow the expected format."""
        project_path = git_repo / generated_project_dir.name
        _setup_project(project_path, generated_project_dir)

        result = _run_bump(project_path, "patch")
        result.check_returncode()

        tags = subprocess.run(
            ["git", "tag", "-l", "-n1"],
            cwd=project_path,
            capture_output=True,
            text=True,
            check=True,
        )
        assert "wall-e-fleet-connector-v0.1.1" in tags.stdout
        expected = "Bump wall-e-fleet-connector version: 0.1.0 → 0.1.1"
        assert expected in tags.stdout
