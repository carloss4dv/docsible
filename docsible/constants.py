"""Shared constants for docsible CLI and core modules."""

DOCSIBLE_START_TAG = "<!-- DOCSIBLE START -->"
DOCSIBLE_END_TAG = "<!-- DOCSIBLE END -->"

DEFAULT_PLAYBOOK_PATH = "tests/test.yml"
DEFAULT_OUTPUT_FILE = "README.md"
DEFAULT_REPOSITORY_BRANCH = "main"
REPOSITORY_URL_DETECT_MODE = "detect"
MARKDOWN_EXTENSION = ".md"

GALAXY_FILE_NAMES = ("galaxy.yml", "galaxy.yaml")
YAML_FILE_EXTENSIONS = (".yml", ".yaml")
YAML_MAIN_SUBDIR = "main"

COLLECTION_ROLES_DIR = "roles"

ROLE_META_DIR = "meta"
ROLE_DEFAULTS_DIR = "defaults"
ROLE_VARS_DIR = "vars"
ROLE_TASKS_DIR = "tasks"

DOCSIBLE_METADATA_FILE = ".docsible"
META_MAIN_FILE_NAMES = ("main.yml", "main.yaml")
ARGUMENT_SPECS_FILE_NAMES = ("argument_specs.yml", "argument_specs.yaml")

ANSIBLE_PLAY_TASKS_KEY = "tasks"
ANSIBLE_PLAY_ROLES_KEY = "roles"

TASK_INFO_KEY_FILE = "file"
TASK_INFO_KEY_TASKS = "tasks"
TASK_INFO_KEY_MERMAID = "mermaid"
TASK_INFO_KEY_COMMENTS = "comments"
TASK_INFO_KEY_LINES = "lines"

ANSIBLE_TASK_BLOCK_KEY = "block"
ANSIBLE_TASK_RESCUE_KEY = "rescue"
ANSIBLE_TASK_WHEN_KEY = "when"
ANSIBLE_TASK_NAME_KEY = "name"
ANSIBLE_PLAY_HOSTS_KEY = "hosts"
ANSIBLE_ROLE_NAME_KEY = "role"
ANSIBLE_INCLUDE_FILE_KEY = "file"
ANSIBLE_INCLUDE_DIR_KEY = "dir"
ANSIBLE_INCLUDE_ROLE_NAME_KEY = "name"

MERMAID_START_NODE = "Start"
MERMAID_END_NODE = "End"
MERMAID_FLOWCHART_HEADER = "flowchart TD"
MERMAID_HOSTS_NODE_PREFIX = "hosts["
MERMAID_HOSTS_NODE_SUFFIX = "]"
MERMAID_UNDEFINED_HOST = "UndefinedHost"
MERMAID_UNNAMED_TASK_PREFIX = "Unnamed_task_"
MERMAID_UNNAMED_ROLE_PREFIX = "Unnamed_role_"
MERMAID_WHEN_LABEL = "When:"
MERMAID_WHEN_JOIN = " AND "
MERMAID_END_OF_BLOCK_LABEL = "End of Block"
MERMAID_END_OF_RESCUE_LABEL = "End of Rescue Block"

MERMAID_CLASSDEF_BLOCK = "classDef block stroke:#3498db,stroke-width:2px;"
MERMAID_CLASSDEF_TASK = "classDef task stroke:#4b76bb,stroke-width:2px;"
MERMAID_CLASSDEF_INCLUDE_TASKS = "classDef includeTasks stroke:#16a085,stroke-width:2px;"
MERMAID_CLASSDEF_IMPORT_TASKS = "classDef importTasks stroke:#34495e,stroke-width:2px;"
MERMAID_CLASSDEF_INCLUDE_ROLE = "classDef includeRole stroke:#2980b9,stroke-width:2px;"
MERMAID_CLASSDEF_IMPORT_ROLE = "classDef importRole stroke:#699ba7,stroke-width:2px;"
MERMAID_CLASSDEF_INCLUDE_VARS = "classDef includeVars stroke:#8e44ad,stroke-width:2px;"
MERMAID_CLASSDEF_RESCUE = "classDef rescue stroke:#665352,stroke-width:2px;"

MERMAID_CLASSDEF_LINES = (
    MERMAID_CLASSDEF_BLOCK,
    MERMAID_CLASSDEF_TASK,
    MERMAID_CLASSDEF_INCLUDE_TASKS,
    MERMAID_CLASSDEF_IMPORT_TASKS,
    MERMAID_CLASSDEF_INCLUDE_ROLE,
    MERMAID_CLASSDEF_IMPORT_ROLE,
    MERMAID_CLASSDEF_INCLUDE_VARS,
    MERMAID_CLASSDEF_RESCUE,
)

TASK_TYPE_DEFAULT = "task"
TASK_DEFAULT_NAME = "Unnamed"
TASK_UNKNOWN_MODULE = "unknown"
TASK_ACTION_KEY = "action"
TASK_NAME_KEY = "name"
TASK_WHEN_KEY = "when"
TASK_WITH_PREFIX = "with_"
TASK_BLOCK_TYPES = ("block", "rescue", "always")
TASK_MODULE_INDICATOR_KEYS = (
    "include_tasks",
    "import_tasks",
    "import_playbook",
    "include_role",
    "import_role",
)

KNOWN_TASK_PARAMS = {
    "action", "any_errors_fatal", "args", "async", "become", "become_exe",
    "become_flags", "become_method", "become_user", "changed_when", "check_mode",
    "collections", "connection", "debugger", "delay", "delegate_facts", "delegate_to",
    "diff", "environment", "failed_when", "ignore_errors", "ignore_unreachable",
    "local_action", "loop", "loop_control", "module_defaults", "name", "no_log",
    "notify", "poll", "port", "register", "remote_user", "retries", "run_once",
    "tags", "throttle", "timeout", "until", "vars", "when", "with_", "block",
    "rescue", "always", "include", "include_tasks", "include_role",
    "import_playbook", "import_tasks", "import_role", "hosts", "gather_facts",
    "roles", "tasks", "handlers", "post_tasks", "pre_tasks", "strategy",
    "max_fail_percentage", "serial", "gather_subset", "gather_timeout",
    "vars_files", "vars_prompt", "force_handlers", "skip_tags", "pause",
    "prompt", "wait_for", "wait_for_connection", "meta", "fact_path",
    "host_vars", "group_vars", "role"
}

TIMESTAMP_FORMAT = "%Y%m%d%H%M%S"
DATE_FORMAT = "%Y/%m/%d"

GIT_COMMAND_TIMEOUT_SECONDS = 5
GIT_EXECUTABLE = "git"
GIT_CONTEXT_FLAG = "-C"
GIT_CMD_REPO_CHECK = ("rev-parse", "--is-inside-work-tree")
GIT_CMD_REMOTE_URL = ("config", "--get", "remote.origin.url")
GIT_CMD_CURRENT_BRANCH = ("rev-parse", "--abbrev-ref", "HEAD")
GIT_TRUE_VALUE = "true"

URL_SCP_PATTERN = r"^git@([^:]+):(.*)$"
URL_SSH_PREFIX = "ssh://git@"
URL_PATH_SEPARATOR = "/"
URL_CREDENTIAL_SEPARATOR = "@"
URL_SCHEME_SSH = "ssh"
URL_SCHEME_GIT = "git"
URL_SCHEME_HTTPS = "https"
URL_GIT_SUFFIX = ".git"
URL_EMPTY = ""

REPO_INFO_KEY_REPOSITORY = "repository"
REPO_INFO_KEY_BRANCH = "branch"
REPO_INFO_KEY_REPOSITORY_TYPE = "repository_type"

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