import shutil
import subprocess
import sys
from pathlib import Path

"""
Post-generation hook to move the generated connector to the current directory.
"""

# Dot-prefixed items (e.g. .git, .claude, .github, .gitignore, .env) in the destination
# are never backed up or overwritten. This preserves repository metadata, AI skills,
# CI configuration, and other dot-files that the user may have customized.


def run_uv_lock(project_dir: Path) -> None:
    """
    Run uv lock in the project directory if uv is available.
    If uv is not available, print a message and continue.
    """
    uv_path = shutil.which("uv")
    if uv_path is None:
        print("uv not found in PATH, skipping uv lock")
        return

    print("Running uv lock...")
    try:
        subprocess.run(
            [uv_path, "lock"],
            cwd=project_dir,
            check=True,
            capture_output=True,
            text=True,
        )
        print("uv lock completed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Warning: uv lock failed: {e}")
        print("Continuing with file operations...")


def find_available_backup_dir(dst: Path) -> Path:
    """
    Find the first available backup directory name by trying repo.backup,
    repo.backup.1, repo.backup.2, etc.
    """
    backup_base = dst / "repo.backup"
    if not backup_base.exists():
        return backup_base

    counter = 1
    while True:
        backup_dir = dst / f"repo.backup.{counter}"
        if not backup_dir.exists():
            return backup_dir
        counter += 1


def move_item(src_item: Path, dst_item: Path):
    """Move a single file or directory from src to dst."""
    if src_item.is_dir():
        if dst_item.exists():
            shutil.copytree(
                src_item,
                dst_item,
                dirs_exist_ok=True,
                copy_function=shutil.copy2,
            )
        else:
            shutil.copytree(src_item, dst_item, copy_function=shutil.copy2)
        shutil.rmtree(src_item)
    else:
        shutil.copy2(src_item, dst_item)
        src_item.unlink()


def move_directory_contents(src: Path, dst: Path):
    """Move contents from src directory to dst directory.

    Handles nested directories with the same name as src by lifting their
    contents up one level.

    Any existing items in dst that would be overwritten are backed up to
    a repo.backup/ directory first. Items not present in the generated output
    are left untouched. Dot-prefixed items (.git, .claude, .github, etc.)
    that already exist in dst are never backed up or overwritten.
    """
    if not src.is_dir():
        raise ValueError(f"Source path {src} is not a directory")

    if not dst.exists():
        dst.mkdir(parents=True, exist_ok=True)

    backup_dir = None

    def _backup(target: Path):
        """Back up an existing item before it gets overwritten."""
        nonlocal backup_dir
        if backup_dir is None:
            backup_dir = find_available_backup_dir(dst)
            backup_dir.mkdir(parents=True)
            print(f"Backing up existing files to {backup_dir}")
        print(f"  Backing up {target.name}")
        move_item(target, backup_dir / target.name)

    def _move(item: Path, target_dir: Path):
        """Move an item, backing up any existing conflict first.

        Dot-prefixed items (.git, .claude, .github, etc.) that already exist in
        the target directory are preserved — they are never backed up or overwritten.
        """
        target = target_dir / item.name
        if target.exists() and target.name.startswith("."):
            print(f"Preserving {target.name}")
            return
        if target.exists():
            _backup(target)
        print(f"Moving {item.name} to {target_dir}")
        move_item(item, target)

    inner_dir = src / src.name

    for item in src.iterdir():
        if item.name == src.name and item.is_dir():
            continue
        _move(item, dst)

    if inner_dir.exists() and inner_dir.is_dir():
        print(f"Lifting contents of {inner_dir.name}/ up into {src.name}/")
        for item in inner_dir.iterdir():
            _move(item, src)
        inner_dir.rmdir()


if __name__ == "__main__":
    if "{{ cookiecutter.use_current_directory }}".lower() == "y":
        try:
            src = Path.cwd()
            dst = src.parent

            run_uv_lock(src)
            move_directory_contents(src, dst)
        except Exception as e:
            print(f"Error moving directory contents: {e}")
            sys.exit(1)
