import shutil
from pathlib import Path
import sys

"""
Post-generation hook to move the generated connector to the current directory.
"""


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


def backup_existing_files(dst: Path, src_dir_name: str):
    """
    Backup existing files in destination directory to repo.backup/.
    Uses numbered suffixes (repo.backup.1, repo.backup.2, etc.) if needed.
    Excludes .git/ directory and the generated source directory.
    """
    backup_dir = find_available_backup_dir(dst)
    backup_dir.mkdir(parents=True, exist_ok=True)

    items_to_backup = []
    for item in dst.iterdir():
        if item.name == ".git" or item.name == src_dir_name:
            continue
        if item.name.startswith("repo.backup"):
            continue
        items_to_backup.append(item)

    if not items_to_backup:
        return

    print(f"Backing up existing files to {backup_dir}")
    for item in items_to_backup:
        backup_item = backup_dir / item.name
        print(f"  Backing up {item.name}")

        if item.is_dir():
            shutil.copytree(item, backup_item, copy_function=shutil.copy2)
            shutil.rmtree(item)
        else:
            shutil.copy2(item, backup_item)
            item.unlink()


def move_item(src_item: Path, dst_item: Path):
    """Move a single file or directory from src to dst."""
    if src_item.is_dir():
        if dst_item.exists():
            shutil.copytree(
                src_item,
                dst_item,
                dirs_exist_ok=True,
                copy_function=shutil.copy2
            )
        else:
            shutil.copytree(src_item, dst_item, copy_function=shutil.copy2)
        shutil.rmtree(src_item)
    else:
        shutil.copy2(src_item, dst_item)
        src_item.unlink()


def move_directory_contents(src: Path, dst: Path):
    """
    Move contents from src directory to dst directory, handling nested
    directories with the same name as src.
    """
    if not src.is_dir():
        raise ValueError(f"Source path {src} is not a directory")

    if not dst.exists():
        dst.mkdir(parents=True, exist_ok=True)

    inner_dir = src / src.name

    for item in src.iterdir():
        if item.name == src.name and item.is_dir():
            continue

        print(f"Moving {item.name} to {dst}")
        move_item(item, dst / item.name)

    if inner_dir.exists() and inner_dir.is_dir():
        print(f"Lifting contents of {inner_dir.name}/ up into {src.name}/")
        for item in inner_dir.iterdir():
            print(f"  Moving {item.name} to {src}")
            move_item(item, src / item.name)

        inner_dir.rmdir()


if __name__ == "__main__":
    if "{{ cookiecutter.use_current_directory }}".lower() == "y":
        try:
            src = Path.cwd()
            dst = src.parent

            backup_existing_files(dst, src.name)
            move_directory_contents(src, dst)
        except Exception as e:
            print(f"Error moving directory contents: {e}")
            sys.exit(1)
