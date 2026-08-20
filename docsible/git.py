from __future__ import annotations
import re
import subprocess
from pathlib import Path
from typing import Dict
from urllib.parse import urlparse, urlunparse
from docsible.constants import (
    DEFAULT_REPOSITORY_TYPE,
    GIT_COMMAND_TIMEOUT_SECONDS,
    GIT_CMD_CURRENT_BRANCH,
    GIT_CMD_REMOTE_URL,
    GIT_CMD_REPO_CHECK,
    GIT_CONTEXT_FLAG,
    GIT_EXECUTABLE,
    GIT_TRUE_VALUE,
    REPO_INFO_KEY_BRANCH,
    REPO_INFO_KEY_REPOSITORY,
    REPO_INFO_KEY_REPOSITORY_TYPE,
    REPOSITORY_TYPE_BY_HOST,
    URL_CREDENTIAL_SEPARATOR,
    URL_EMPTY,
    URL_GIT_SUFFIX,
    URL_PATH_SEPARATOR,
    URL_SCP_PATTERN,
    URL_SCHEME_GIT,
    URL_SCHEME_HTTPS,
    URL_SCHEME_SSH,
    URL_SSH_PREFIX,
)


class GitInfoError(Exception):
    pass


class GitCommandError(GitInfoError):
    def __init__(self, message: str, stderr: str | None = None):
        super().__init__(message)
        self.stderr = stderr


class GitTimeoutError(GitInfoError):
    pass


class NotGitRepositoryError(GitInfoError):
    pass


def clean_and_standardize_url(url: str) -> str:
    processed_url = url

    scp_like_match = re.match(URL_SCP_PATTERN, processed_url)
    if scp_like_match:
        hostname = scp_like_match.group(1)
        path = scp_like_match.group(2)
        processed_url = f"{URL_SSH_PREFIX}{hostname}{URL_PATH_SEPARATOR}{path}"

    try:
        parsed = urlparse(processed_url)
        netloc = parsed.netloc
        path = parsed.path
        force_https = False

        if URL_CREDENTIAL_SEPARATOR in netloc:
            force_https = True
            netloc_parts = netloc.rsplit(URL_CREDENTIAL_SEPARATOR, 1)
            if len(netloc_parts) == 2:
                netloc = netloc_parts[1]
            else:
                return URL_EMPTY

        if parsed.scheme in (URL_SCHEME_SSH, URL_SCHEME_GIT):
            force_https = True

        final_scheme = URL_SCHEME_HTTPS if force_https and netloc else parsed.scheme

        path = parsed.path.rstrip(URL_PATH_SEPARATOR)
        if path.endswith(URL_GIT_SUFFIX):
            path = path[:-4]

        return urlunparse((
            final_scheme,
            netloc,
            path,
            "",
            "",
            ""
        ))
    except (ValueError, IndexError):
        return URL_EMPTY


def get_repo_info(path: str | Path) -> Dict[str, str]:
    dir_path = str(path)
    timeout = GIT_COMMAND_TIMEOUT_SECONDS

    try:
        is_repo_check = subprocess.run(
            [GIT_EXECUTABLE, GIT_CONTEXT_FLAG, dir_path, *GIT_CMD_REPO_CHECK],
            capture_output=True, text=True, check=True, timeout=timeout
        )
        if is_repo_check.stdout.strip() != GIT_TRUE_VALUE:
            raise NotGitRepositoryError(f"Path is not inside a Git work tree: {dir_path}")

        raw_url = subprocess.run(
            [GIT_EXECUTABLE, GIT_CONTEXT_FLAG, dir_path, *GIT_CMD_REMOTE_URL],
            capture_output=True, text=True, check=True, timeout=timeout
        ).stdout.strip()

        branch = subprocess.run(
            [GIT_EXECUTABLE, GIT_CONTEXT_FLAG, dir_path, *GIT_CMD_CURRENT_BRANCH],
            capture_output=True, text=True, check=True, timeout=timeout
        ).stdout.strip()

    except subprocess.TimeoutExpired as e:
        raise GitTimeoutError(f"Git command timed out for path: {dir_path}") from e
    except subprocess.CalledProcessError as e:
        raise GitCommandError(
            f"A Git command failed for path: {dir_path}",
            stderr=e.stderr.strip()
        ) from e

    repository_url = clean_and_standardize_url(raw_url)
    hostname = urlparse(repository_url).hostname or URL_EMPTY

    repo_type = DEFAULT_REPOSITORY_TYPE
    for host_marker, detected_repo_type in REPOSITORY_TYPE_BY_HOST.items():
        if host_marker in hostname:
            repo_type = detected_repo_type
            break

    return {
        REPO_INFO_KEY_REPOSITORY: repository_url,
        REPO_INFO_KEY_BRANCH: branch,
        REPO_INFO_KEY_REPOSITORY_TYPE: repo_type,
    }
