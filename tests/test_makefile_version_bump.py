# SPDX-FileCopyrightText: 2026 InOrbit, Inc.
#
# SPDX-License-Identifier: MIT

"""
Tests for Makefile version bumping functionality in generated projects.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest


class TestMakefileVersionBump:
    """Test Makefile version bumping commands."""

    def test_bump_patch(self, generated_project_dir, git_repo):
        """Test that make bump-patch increments patch version."""
        # Copy generated project to git repo
        project_name = generated_project_dir.name
        project_path = git_repo / project_name
        shutil.copytree(generated_project_dir, project_path)

        # Initialize git and make initial commit
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

        # Read initial version
        pyproject_path = project_path / "pyproject.toml"
        initial_content = pyproject_path.read_text()
        assert 'version = "0.1.0"' in initial_content

        # Run bump-patch
        result = subprocess.run(
            ["make", "bump-patch"],
            cwd=project_path,
            capture_output=True,
            text=True,
            check=True,
        )

        # Verify version was bumped
        new_content = pyproject_path.read_text()
        assert 'version = "0.1.1"' in new_content

        # Verify git commit was created
        commit_result = subprocess.run(
            ["git", "log", "-1", "--pretty=format:%s"],
            cwd=project_path,
            capture_output=True,
            text=True,
            check=True,
        )
        assert "Bump wall-e-fleet-connector version: 0.1.0 → 0.1.1" in commit_result.stdout

        # Verify tag was created
        tag_result = subprocess.run(
            ["git", "tag", "-l"],
            cwd=project_path,
            capture_output=True,
            text=True,
            check=True,
        )
        assert "wall-e-fleet-connector-v0.1.1" in tag_result.stdout

    def test_bump_minor(self, generated_project_dir, git_repo):
        """Test that make bump-minor increments minor version."""
        project_name = generated_project_dir.name
        project_path = git_repo / project_name
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

        result = subprocess.run(
            ["make", "bump-minor"],
            cwd=project_path,
            capture_output=True,
            text=True,
            check=True,
        )

        pyproject_path = project_path / "pyproject.toml"
        new_content = pyproject_path.read_text()
        assert 'version = "0.2.0"' in new_content

    def test_bump_major(self, generated_project_dir, git_repo):
        """Test that make bump-major increments major version."""
        project_name = generated_project_dir.name
        project_path = git_repo / project_name
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

        result = subprocess.run(
            ["make", "bump-major"],
            cwd=project_path,
            capture_output=True,
            text=True,
            check=True,
        )

        pyproject_path = project_path / "pyproject.toml"
        new_content = pyproject_path.read_text()
        assert 'version = "1.0.0"' in new_content

    def test_bump_dry_run(self, generated_project_dir, git_repo):
        """Test that make bump DRY=1 does not make changes."""
        project_name = generated_project_dir.name
        project_path = git_repo / project_name
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

        pyproject_path = project_path / "pyproject.toml"
        initial_content = pyproject_path.read_text()

        # Run dry-run
        result = subprocess.run(
            ["make", "bump", "PART=patch", "DRY=1"],
            cwd=project_path,
            capture_output=True,
            text=True,
            check=True,
        )

        # Verify version was not changed
        new_content = pyproject_path.read_text()
        assert new_content == initial_content

        # Verify no commit was created
        commit_result = subprocess.run(
            ["git", "log", "--oneline"],
            cwd=project_path,
            capture_output=True,
            text=True,
            check=True,
        )
        assert commit_result.stdout.count("\n") == 1  # Only initial commit

        # Verify no tag was created
        tag_result = subprocess.run(
            ["git", "tag", "-l"],
            cwd=project_path,
            capture_output=True,
            text=True,
            check=True,
        )
        assert tag_result.stdout.strip() == ""

    def test_bump_requires_clean_working_tree(self, generated_project_dir, git_repo):
        """Test that bump fails with dirty working tree."""
        project_name = generated_project_dir.name
        project_path = git_repo / project_name
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

        # Create uncommitted change
        readme_path = project_path / "README.md"
        readme_path.write_text("Modified content")

        # Try to bump - should fail
        result = subprocess.run(
            ["make", "bump-patch"],
            cwd=project_path,
            capture_output=True,
            text=True,
        )

        assert result.returncode != 0
        assert "Working tree must be clean" in result.stderr

    def test_bump_allows_dirty_with_flag(self, generated_project_dir, git_repo):
        """Test that bump works with DIRTY=1 flag even with dirty working tree."""
        project_name = generated_project_dir.name
        project_path = git_repo / project_name
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

        # Create uncommitted change
        readme_path = project_path / "README.md"
        readme_path.write_text("Modified content")

        # Bump with DIRTY=1 - should succeed
        result = subprocess.run(
            ["make", "bump-patch", "DIRTY=1"],
            cwd=project_path,
            capture_output=True,
            text=True,
            check=True,
        )

        pyproject_path = project_path / "pyproject.toml"
        new_content = pyproject_path.read_text()
        assert 'version = "0.1.1"' in new_content

    def test_bump_updates_uv_lock(self, generated_project_dir, git_repo):
        """Test that uv.lock is updated and committed."""
        project_name = generated_project_dir.name
        project_path = git_repo / project_name
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

        lock_path = project_path / "uv.lock"
        initial_lock_content = lock_path.read_text()

        # Run bump
        subprocess.run(
            ["make", "bump-patch"],
            cwd=project_path,
            capture_output=True,
            text=True,
            check=True,
        )

        # Verify lock file was updated (should have different content)
        new_lock_content = lock_path.read_text()
        # The lock file should be different due to version change
        # We'll check that it's in the commit
        diff_result = subprocess.run(
            ["git", "diff", "HEAD~1", "HEAD", "--", "uv.lock"],
            cwd=project_path,
            capture_output=True,
            text=True,
            check=True,
        )
        # Should show changes to uv.lock
        assert len(diff_result.stdout) > 0

    def test_bump_tag_format(self, generated_project_dir, git_repo):
        """Test that tags follow the expected format."""
        project_name = generated_project_dir.name
        project_path = git_repo / project_name
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

        subprocess.run(
            ["make", "bump-patch"],
            cwd=project_path,
            capture_output=True,
            text=True,
            check=True,
        )

        # Verify tag format: {project_slug}-v{version}
        tag_result = subprocess.run(
            ["git", "tag", "-l", "-n1"],
            cwd=project_path,
            capture_output=True,
            text=True,
            check=True,
        )
        assert "wall-e-fleet-connector-v0.1.1" in tag_result.stdout
        assert "Bump wall-e-fleet-connector version: 0.1.0 → 0.1.1" in tag_result.stdout
