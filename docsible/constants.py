"""Shared constants for docsible CLI and core modules."""

DOCSIBLE_START_TAG = "<!-- DOCSIBLE START -->"
DOCSIBLE_END_TAG = "<!-- DOCSIBLE END -->"

DEFAULT_PLAYBOOK_PATH = "tests/test.yml"
DEFAULT_OUTPUT_FILE = "README.md"
DEFAULT_REPOSITORY_BRANCH = "main"
REPOSITORY_URL_DETECT_MODE = "detect"

GALAXY_FILE_NAMES = ("galaxy.yml", "galaxy.yaml")
YAML_FILE_EXTENSIONS = (".yml", ".yaml")

COLLECTION_ROLES_DIR = "roles"

ROLE_META_DIR = "meta"
ROLE_DEFAULTS_DIR = "defaults"
ROLE_VARS_DIR = "vars"
ROLE_TASKS_DIR = "tasks"

DOCSIBLE_METADATA_FILE = ".docsible"
META_MAIN_FILE_NAMES = ("main.yml", "main.yaml")
ARGUMENT_SPECS_FILE_NAMES = ("argument_specs.yml", "argument_specs.yaml")

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