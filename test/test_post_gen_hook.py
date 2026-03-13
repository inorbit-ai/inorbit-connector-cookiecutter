# SPDX-FileCopyrightText: 2026 InOrbit, Inc.
#
# SPDX-License-Identifier: MIT

"""
Tests for the post-generation hook.
"""

from __future__ import annotations

import pytest

# Import hook functions directly for unit testing
from hooks.post_gen_project import (
    find_available_backup_dir,
    move_directory_contents,
    move_item,
)


class TestFindAvailableBackupDir:
    """Test the find_available_backup_dir function."""

    def test_returns_repo_backup_when_not_exists(self, temp_dir):
        """Test that repo.backup is returned when it doesn't exist."""
        result = find_available_backup_dir(temp_dir)
        assert result == temp_dir / "repo.backup"
        assert not result.exists()

    def test_returns_numbered_backup_when_exists(self, temp_dir):
        """Test numbered backup dirs returned when repo.backup exists."""
        # Create repo.backup
        (temp_dir / "repo.backup").mkdir()

        result = find_available_backup_dir(temp_dir)
        assert result == temp_dir / "repo.backup.1"
        assert not result.exists()

    def test_returns_next_available_number(self, temp_dir):
        """Test that the next available number is used."""
        (temp_dir / "repo.backup").mkdir()
        (temp_dir / "repo.backup.1").mkdir()
        (temp_dir / "repo.backup.2").mkdir()

        result = find_available_backup_dir(temp_dir)
        assert result == temp_dir / "repo.backup.3"
        assert not result.exists()


class TestMoveItem:
    """Test the move_item function."""

    def test_moves_file(self, temp_dir):
        """Test moving a file."""
        src_file = temp_dir / "source.txt"
        src_file.write_text("content")
        dst_file = temp_dir / "dest.txt"

        move_item(src_file, dst_file)

        assert dst_file.exists()
        assert dst_file.read_text() == "content"
        assert not src_file.exists()

    def test_moves_directory(self, temp_dir):
        """Test moving a directory."""
        src_dir = temp_dir / "source_dir"
        src_dir.mkdir()
        (src_dir / "file.txt").write_text("content")
        dst_dir = temp_dir / "dest_dir"

        move_item(src_dir, dst_dir)

        assert dst_dir.exists()
        assert (dst_dir / "file.txt").exists()
        assert (dst_dir / "file.txt").read_text() == "content"
        assert not src_dir.exists()

    def test_merges_existing_directory(self, temp_dir):
        """Test that moving to an existing directory merges contents."""
        src_dir = temp_dir / "source_dir"
        src_dir.mkdir()
        (src_dir / "new_file.txt").write_text("new")

        dst_dir = temp_dir / "dest_dir"
        dst_dir.mkdir()
        (dst_dir / "existing_file.txt").write_text("existing")

        move_item(src_dir, dst_dir)

        assert dst_dir.exists()
        assert (dst_dir / "new_file.txt").exists()
        assert (dst_dir / "existing_file.txt").exists()
        assert not src_dir.exists()


class TestMoveDirectoryContents:
    """Test the move_directory_contents function."""

    def test_moves_all_contents(self, temp_dir):
        """Test that all contents are moved."""
        src = temp_dir / "source"
        src.mkdir()
        (src / "file1.txt").write_text("file1")
        (src / "file2.txt").write_text("file2")
        (src / "subdir").mkdir()
        (src / "subdir" / "nested.txt").write_text("nested")

        dst = temp_dir / "dest"
        dst.mkdir()

        move_directory_contents(src, dst)

        assert (dst / "file1.txt").exists()
        assert (dst / "file2.txt").exists()
        assert (dst / "subdir").exists()
        assert (dst / "subdir" / "nested.txt").exists()
        assert not (src / "file1.txt").exists()

    def test_lifts_nested_directory(self, temp_dir):
        """Test that nested directory with same name is lifted."""
        src = temp_dir / "test_connector"
        src.mkdir()
        (src / "file1.txt").write_text("file1")

        # Create nested directory with same name
        nested = src / "test_connector"
        nested.mkdir()
        (nested / "file2.txt").write_text("file2")
        (nested / "subdir").mkdir()
        (nested / "subdir" / "nested.txt").write_text("nested")

        dst = temp_dir / "dest"
        dst.mkdir()

        move_directory_contents(src, dst)

        # Nested contents should be lifted to src level
        assert (src / "file2.txt").exists()
        assert (src / "subdir").exists()
        assert (src / "subdir" / "nested.txt").exists()
        assert not nested.exists()  # Nested dir should be removed

        # Original contents should be moved to dst
        assert (dst / "file1.txt").exists()

    def test_raises_error_if_source_not_directory(self, temp_dir):
        """Test that ValueError is raised if source is not a directory."""
        src_file = temp_dir / "not_a_dir.txt"
        src_file.write_text("content")
        dst = temp_dir / "dest"
        dst.mkdir()

        with pytest.raises(ValueError, match="is not a directory"):
            move_directory_contents(src_file, dst)

    def test_creates_destination_if_not_exists(self, temp_dir):
        """Test that destination is created if it doesn't exist."""
        src = temp_dir / "source"
        src.mkdir()
        (src / "file.txt").write_text("content")

        dst = temp_dir / "dest"

        move_directory_contents(src, dst)

        assert dst.exists()
        assert (dst / "file.txt").exists()

    def test_backs_up_conflicting_files(self, temp_dir):
        """Test that existing files in dst are backed up when overwritten."""
        src = temp_dir / "source"
        src.mkdir()
        (src / "README.md").write_text("new readme")
        (src / "config").mkdir()
        (src / "config" / "example.yaml").write_text("new config")

        dst = temp_dir / "dest"
        dst.mkdir()
        (dst / "README.md").write_text("old readme")
        (dst / "config").mkdir()
        (dst / "config" / "example.yaml").write_text("old config")

        move_directory_contents(src, dst)

        # New content should be in place
        assert (dst / "README.md").read_text() == "new readme"
        assert (dst / "config" / "example.yaml").read_text() == "new config"

        # Old content should be backed up
        backup_dir = dst / "repo.backup"
        assert backup_dir.exists()
        assert (backup_dir / "README.md").read_text() == "old readme"
        assert (backup_dir / "config" / "example.yaml").read_text() == "old config"

    def test_leaves_non_conflicting_items_untouched(self, temp_dir):
        """Test that items in dst not present in src are left alone."""
        src = temp_dir / "source"
        src.mkdir()
        (src / "README.md").write_text("new readme")

        dst = temp_dir / "dest"
        dst.mkdir()
        (dst / "README.md").write_text("old readme")
        (dst / ".claude").mkdir()
        (dst / ".claude" / "skills").mkdir()
        (dst / ".claude" / "skills" / "connector.md").write_text("skill")
        (dst / ".vscode").mkdir()
        (dst / ".vscode" / "settings.json").write_text("{}")

        move_directory_contents(src, dst)

        # Non-conflicting items should be untouched
        assert (dst / ".claude" / "skills" / "connector.md").read_text() == "skill"
        assert (dst / ".vscode" / "settings.json").read_text() == "{}"

        # They should NOT appear in backup
        backup_dir = dst / "repo.backup"
        assert not (backup_dir / ".claude").exists()
        assert not (backup_dir / ".vscode").exists()

    def test_preserves_dot_prefixed_items(self, temp_dir):
        """Test that dot-prefixed items are never backed up or overwritten."""
        src = temp_dir / "source"
        src.mkdir()
        (src / "file.txt").write_text("content")
        # Generated output also has a .claude dir (conflict scenario)
        (src / ".claude").mkdir()
        (src / ".claude" / "generated.md").write_text("generated")
        (src / ".github").mkdir()
        (src / ".github" / "workflows").mkdir()

        dst = temp_dir / "dest"
        dst.mkdir()
        (dst / ".git").mkdir()
        (dst / ".git" / "HEAD").write_text("ref: refs/heads/main")
        (dst / ".claude").mkdir()
        (dst / ".claude" / "skills").mkdir()
        (dst / ".claude" / "skills" / "dev.md").write_text("# AI skill")
        (dst / ".github").mkdir()
        (dst / ".github" / "CODEOWNERS").write_text("* @team")

        move_directory_contents(src, dst)

        # .git preserved
        assert (dst / ".git" / "HEAD").read_text() == "ref: refs/heads/main"
        # .claude preserved (not replaced by generated .claude)
        assert (dst / ".claude" / "skills" / "dev.md").read_text() == "# AI skill"
        # .github preserved
        assert (dst / ".github" / "CODEOWNERS").read_text() == "* @team"
        # Regular file still moved
        assert (dst / "file.txt").read_text() == "content"
        # Nothing dot-prefixed in backup
        backup = dst / "repo.backup"
        if backup.exists():
            assert not (backup / ".git").exists()
            assert not (backup / ".claude").exists()
            assert not (backup / ".github").exists()

    def test_preserves_dot_prefixed_items_during_lift(self, temp_dir):
        """Test dot-prefixed preservation in nested-directory lift doesn't crash."""
        src = temp_dir / "myconnector"
        src.mkdir()
        (src / "README.md").write_text("top-level readme")
        (src / ".github").mkdir()
        (src / ".github" / "workflows").mkdir()
        (src / ".github" / "workflows" / "ci.yml").write_text("ci: generated")

        # Nested directory with same name (triggers the lift logic)
        nested = src / "myconnector"
        nested.mkdir()
        (nested / "connector.py").write_text("# connector")
        (nested / ".github").mkdir()
        (nested / ".github" / "workflows").mkdir()
        (nested / ".github" / "workflows" / "ci.yml").write_text("ci: nested")

        dst = temp_dir / "dest"
        dst.mkdir()
        (dst / ".github").mkdir()
        (dst / ".github" / "CODEOWNERS").write_text("* @team")

        move_directory_contents(src, dst)

        # dst's .github should be preserved (not overwritten by src's .github)
        assert (dst / ".github" / "CODEOWNERS").read_text() == "* @team"
        # src's .github was preserved (not moved to dst), so it stays in src
        assert (src / ".github" / "workflows" / "ci.yml").read_text() == "ci: generated"
        # Lifted connector.py should be in src
        assert (src / "connector.py").read_text() == "# connector"
        # nested dir may not be fully removed if .github was left behind
        # but the function should NOT crash

    def test_no_backup_dir_when_no_conflicts(self, temp_dir):
        """Test that no backup directory is created when there are no conflicts."""
        src = temp_dir / "source"
        src.mkdir()
        (src / "new_file.txt").write_text("new")

        dst = temp_dir / "dest"
        dst.mkdir()
        (dst / "existing_file.txt").write_text("existing")

        move_directory_contents(src, dst)

        assert not (dst / "repo.backup").exists()
        # Both files should coexist
        assert (dst / "new_file.txt").read_text() == "new"
        assert (dst / "existing_file.txt").read_text() == "existing"

    def test_backup_numbering_with_existing_backups(self, temp_dir):
        """Test that backup uses next available number."""
        src = temp_dir / "source"
        src.mkdir()
        (src / "file.txt").write_text("new")

        dst = temp_dir / "dest"
        dst.mkdir()
        (dst / "file.txt").write_text("old")
        (dst / "repo.backup").mkdir()
        (dst / "repo.backup.1").mkdir()

        move_directory_contents(src, dst)

        assert (dst / "repo.backup.2" / "file.txt").read_text() == "old"


class TestPostGenHookIntegration:
    """Integration tests for the post-gen hook as a script."""

    def test_hook_runs_when_use_current_directory_is_y(
        self, temp_dir, cookiecutter_template_dir
    ):
        """Test full hook behavior: move with backup, preserving unrelated items."""
        # Create a structure simulating cookiecutter output
        generated_dir = temp_dir / "wall_e_fleet_connector"
        generated_dir.mkdir()
        (generated_dir / "README.md").write_text("# Generated Project")
        (generated_dir / "pyproject.toml").write_text("[project]")

        # Create nested structure (inner package dir)
        nested = generated_dir / "wall_e_fleet_connector"
        nested.mkdir()
        (nested / "src").mkdir()
        (nested / "src" / "connector.py").write_text("# Connector code")

        # Create parent directory with existing files (simulating template repo)
        parent = temp_dir / "parent"
        parent.mkdir()
        (parent / "README.md").write_text("# Old README")
        (parent / "LICENSE").write_text("MIT")
        (parent / ".claude").mkdir()
        (parent / ".claude" / "skills").mkdir()
        (parent / ".claude" / "skills" / "dev.md").write_text("# AI skill")

        move_directory_contents(generated_dir, parent)

        # Generated files should be in place
        assert (parent / "README.md").read_text() == "# Generated Project"
        assert (parent / "pyproject.toml").read_text() == "[project]"
        # Nested contents should be lifted
        assert (generated_dir / "src" / "connector.py").exists()

        # Conflicting README should be backed up
        assert (parent / "repo.backup" / "README.md").read_text() == "# Old README"

        # Non-conflicting LICENSE should be untouched (not backed up)
        assert (parent / "LICENSE").read_text() == "MIT"
        assert not (parent / "repo.backup" / "LICENSE").exists()

        # .claude should be completely untouched
        assert (parent / ".claude" / "skills" / "dev.md").read_text() == "# AI skill"
        assert not (parent / "repo.backup" / ".claude").exists()
