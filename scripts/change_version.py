#!/usr/bin/env python3
"""
This script updates the version across multiple files:
 - docsible/cli.py (the function get_version() returns the version)
 - setup.py (e.g., version='0.7.10')
 - pyproject.toml (e.g., version = "0.7.10")

It supports two actions:
  - "bump": increments the patch version (e.g. 0.7.10 -> 0.7.11)
  - "revert": decrements the patch version (e.g. 0.7.10 -> 0.7.9)
  
Usage:
    python scripts/change_version.py bump
    python scripts/change_version.py revert
"""

import re
import sys
import logging
import argparse
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


SEMVER_PATTERN = r"^(\d+)\.(\d+)\.(\d+)$"

CLI_FILE = Path("docsible") / "cli.py"
SETUP_FILE = Path("setup.py")
PYPROJECT_FILE = Path("pyproject.toml")

CLI_VERSION_PATTERN = r'(def\s+get_version\(\):\s+return\s+["\'])(\d+\.\d+\.\d+)(["\'])'
SETUP_VERSION_PATTERN = r'(version\s*=\s*["\'])(\d+\.\d+\.\d+)(["\'])'
PYPROJECT_VERSION_PATTERN = r'(version\s*=\s*["\'])(\d+\.\d+\.\d+)(["\'])'

VERSION_REPLACEMENT = r'\g<1>{}\g<3>'

ERROR_INVALID_VERSION = "Invalid version format: {}"
ERROR_PATCH_UNDERFLOW = "Cannot revert version: patch version is already 0."
ERROR_FILE_MISSING = "File {} does not exist."
ERROR_VERSION_NOT_FOUND = "Version string not found in {}"
ERROR_CLI_READ = "Error reading {}: {}"
ERROR_CLI_VERSION_NOT_FOUND = "Could not find version string in docsible/cli.py"

LOG_CURRENT_VERSION = "Current version in cli.py: {}"
LOG_BUMP_VERSION = "Bumping version to: {}"
LOG_REVERT_VERSION = "Reverting version to: {}"
LOG_FILE_UPDATED = "Updated {}"
LOG_VERSION_COMPLETE = "Version update complete. New version: {}"


def change_version(version_str: str, bump: bool = True) -> str:
    """
    Change the patch version number.

    Args:
        version_str (str): A semantic version string in the format 'major.minor.patch'
        bump (bool): If True, increment the patch version; if False, decrement it.

    Returns:
        str: The updated version string.

    Raises:
        ValueError: If the version format is invalid.
    """
    match = re.match(SEMVER_PATTERN, version_str)
    if not match:
        raise ValueError(ERROR_INVALID_VERSION.format(version_str))
    major, minor, patch = map(int, match.groups())
    if bump:
        patch += 1
    else:
        if patch == 0:
            logging.error(ERROR_PATCH_UNDERFLOW)
            sys.exit(1)
        patch -= 1
    return f"{major}.{minor}.{patch}"


def update_file(file_path: Path, pattern: str, replacement_format: str, new_version: str):
    """
    Updates a file by replacing the version string with the new version.

    Args:
        file_path (str): The path to the file.
        pattern (str): A regex pattern to find the version string.
        replacement_format (str): A format string using explicit group references.
        new_version (str): The new version string to inject.
    """
    if not file_path.exists():
        logging.error(ERROR_FILE_MISSING.format(file_path))
        sys.exit(1)
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    if not re.search(pattern, content):
        logging.error(ERROR_VERSION_NOT_FOUND.format(file_path))
        sys.exit(1)
    new_content = re.sub(
        pattern, replacement_format.format(new_version), content)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    logging.info(LOG_FILE_UPDATED.format(file_path))


def main():
    parser = argparse.ArgumentParser(
        description="Bump or revert version across multiple files."
    )
    parser.add_argument(
        "action",
        choices=["bump", "revert"],
        help="Action to perform: 'bump' to increment or 'revert' to decrement the patch version.",
    )
    args = parser.parse_args()

    # Read the current version from cli.py.
    try:
        with open(CLI_FILE, "r", encoding="utf-8") as f:
            cli_content = f.read()
    except Exception as e:
        logging.error(ERROR_CLI_READ.format(CLI_FILE, e))
        sys.exit(1)

    cli_match = re.search(CLI_VERSION_PATTERN, cli_content)
    if not cli_match:
        logging.error(ERROR_CLI_VERSION_NOT_FOUND)
        sys.exit(1)
    current_version = cli_match.group(2)
    logging.info(LOG_CURRENT_VERSION.format(current_version))

    # Decide the new version based on the requested action.
    if args.action == "bump":
        new_version = change_version(current_version, bump=True)
        logging.info(LOG_BUMP_VERSION.format(new_version))
    else:
        new_version = change_version(current_version, bump=False)
        logging.info(LOG_REVERT_VERSION.format(new_version))

    # Update all files with the new version.
    update_file(CLI_FILE, CLI_VERSION_PATTERN, VERSION_REPLACEMENT, new_version)
    update_file(SETUP_FILE, SETUP_VERSION_PATTERN, VERSION_REPLACEMENT, new_version)
    update_file(PYPROJECT_FILE, PYPROJECT_VERSION_PATTERN, VERSION_REPLACEMENT, new_version)

    logging.info(LOG_VERSION_COMPLETE.format(new_version))


if __name__ == "__main__":
    main()
