"""Shared constants for docsible CLI and core modules."""

DOCSIBLE_START_TAG = "<!-- DOCSIBLE START -->"
DOCSIBLE_END_TAG = "<!-- DOCSIBLE END -->"

DEFAULT_PLAYBOOK_PATH = "tests/test.yml"
DEFAULT_OUTPUT_FILE = "README.md"
DEFAULT_REPOSITORY_BRANCH = "main"

GALAXY_FILE_NAMES = ("galaxy.yml", "galaxy.yaml")

TIMESTAMP_FORMAT = "%Y%m%d%H%M%S"
DATE_FORMAT = "%Y/%m/%d"

GIT_COMMAND_TIMEOUT_SECONDS = 5
REPOSITORY_TYPE_BY_HOST = {
    "github": "github",
    "gitlab": "gitlab",
    "gitea": "gitea",
    "bitbucket.org": "bitbucket",
}
DEFAULT_REPOSITORY_TYPE = "default"

DOCSIBLE_DEFAULT_METADATA = {
    "description": None,
    "requester": None,
    "users": None,
    "dt_dev": None,
    "dt_prod": None,
    "dt_update": None,
    "version": None,
    "time_saving": None,
    "category": None,
    "subCategory": None,
    "aap_hub": None,
    "critical": None,
    "automation_kind": None,
}