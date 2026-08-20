import re
from docsible.constants import (
    ANSIBLE_INCLUDE_DIR_KEY,
    ANSIBLE_INCLUDE_FILE_KEY,
    ANSIBLE_INCLUDE_ROLE_NAME_KEY,
    ANSIBLE_PLAY_HOSTS_KEY,
    ANSIBLE_PLAY_ROLES_KEY,
    ANSIBLE_PLAY_TASKS_KEY,
    ANSIBLE_ROLE_NAME_KEY,
    ANSIBLE_TASK_BLOCK_KEY,
    ANSIBLE_TASK_NAME_KEY,
    ANSIBLE_TASK_RESCUE_KEY,
    ANSIBLE_TASK_WHEN_KEY,
    MERMAID_CLASSDEF_LINES,
    MERMAID_END_NODE,
    MERMAID_END_OF_BLOCK_LABEL,
    MERMAID_END_OF_RESCUE_LABEL,
    MERMAID_FLOWCHART_HEADER,
    MERMAID_HOSTS_NODE_PREFIX,
    MERMAID_HOSTS_NODE_SUFFIX,
    MERMAID_START_NODE,
    MERMAID_UNDEFINED_HOST,
    MERMAID_UNNAMED_ROLE_PREFIX,
    MERMAID_UNNAMED_TASK_PREFIX,
    MERMAID_WHEN_JOIN,
    MERMAID_WHEN_LABEL,
    TASK_INFO_KEY_FILE,
    TASK_INFO_KEY_MERMAID,
)


def sanitize_for_mermaid_id(text):
    text = text.replace("|", "_")
    # Allowing a-zA-Z0-9 as well as French accents
    return re.sub(r'[^a-zA-Z0-9À-ÿ]', '_', text)


def break_text(text, max_length=50):
    words = text.split(' ')
    lines = []
    current_line = []
    current_length = 0
    for word in words:
        if current_length + len(word) + len(current_line) > max_length:
            lines.append(' '.join(current_line))
            current_length = 0
            current_line = []
        current_line.append(word)
        current_length += len(word)
    if current_line:
        lines.append(' '.join(current_line))
    return '<br>'.join(lines)


def sanitize_for_title(text):
    # Allowing a-z0-9 as well as French accents, and converting to lower case
    try:
        sanitized_text = re.sub(r'[^a-z0-9À-ÿ]', ' ', text.lower())
        return break_text(sanitized_text)
    except Exception as e:
        return "cannot handle"


def sanitize_for_condition(text, max_length=50):
    sanitized_text = re.sub(r'[^a-z0-9À-ÿ]', ' ', text.lower())
    return break_text(sanitized_text, max_length)


def process_tasks(tasks, last_node, mermaid_data, parent_node=None, level=0, in_rescue_block=False):
    for i, task in enumerate(tasks):
        has_rescue = False
        task_name = task.get(ANSIBLE_TASK_NAME_KEY, f"{MERMAID_UNNAMED_TASK_PREFIX}{i}")
        task_module_include_tasks = task.get(
            "ansible.builtin.include_tasks") or task.get("include_tasks", False)
        task_module_import_tasks = task.get(
            "ansible.builtin.import_tasks") or task.get("import_tasks", False)
        task_module_import_playbook = task.get(
            "ansible.builtin.import_playbook") or task.get("import_playbook", False)
        task_module_include_role = task.get(
            "ansible.builtin.include_role") or task.get("include_role", False)
        task_module_import_role = task.get(
            "ansible.builtin.import_role") or task.get("import_role", False)
        task_module_include_vars = task.get(
            "ansible.builtin.include_vars") or task.get("include_vars", False)
        when_condition = task.get(ANSIBLE_TASK_WHEN_KEY, False)
        block = task.get(ANSIBLE_TASK_BLOCK_KEY, False)
        rescue = task.get(ANSIBLE_TASK_RESCUE_KEY, False)
        task_name = re.sub(r"{{\s*(\w+)\s*}}", r"\1", task_name)
        sanitized_task_name = sanitize_for_mermaid_id(f"{task_name}{i}")
        sanitized_task_title = sanitize_for_title(task_name)
        if when_condition:
            if isinstance(when_condition, list):
                when_condition = MERMAID_WHEN_JOIN.join(when_condition)
            sanitized_when_condition = f"**{sanitize_for_condition(str(when_condition)).strip()}**"
            if MERMAID_WHEN_LABEL not in sanitized_task_title:
                sanitized_task_title += f'<br>{MERMAID_WHEN_LABEL} {sanitized_when_condition}'
        if block:
            block_start_node = sanitized_task_name + f'_block_start_{level}'
            mermaid_data += f'\n  {last_node}-->|Block Start| {block_start_node}[[{sanitized_task_title}]]:::block'
            last_node, mermaid_data = process_tasks(
                block, block_start_node, mermaid_data, block_start_node, level + 1, in_rescue_block=False)
            if rescue:
                has_rescue = True
                rescue_start_node = sanitized_task_name + \
                    f'_rescue_start_{level}'
                mermaid_data += f'\n  {last_node}-->|Rescue Start| {rescue_start_node}[{sanitized_task_title}]:::rescue'
                last_node, mermaid_data = process_tasks(
                    rescue, rescue_start_node, mermaid_data, block_start_node, level + 1, in_rescue_block=True)
                end_label = MERMAID_END_OF_RESCUE_LABEL
                mermaid_data += f'\n  {last_node}-.->|{end_label}| {block_start_node}'
        elif rescue:
            rescue_start_node = sanitized_task_name + f'_rescue_start_{level}'
            mermaid_data += f'\n  {last_node}-->|Rescue Start| {rescue_start_node}[{sanitized_task_title}]:::rescue'
            last_node, mermaid_data = process_tasks(
                rescue, rescue_start_node, mermaid_data, parent_node, level + 1, in_rescue_block=True)
            end_label = MERMAID_END_OF_RESCUE_LABEL
            mermaid_data += f'\n  {last_node}-.->|{end_label}| {parent_node}'
        else:

            if task_module_include_tasks:
                if isinstance(task_module_include_tasks, dict):
                    check_style_included_tasks = task_module_include_tasks.get(
                        ANSIBLE_INCLUDE_FILE_KEY, task_module_include_tasks)
                else:
                    check_style_included_tasks = task_module_include_tasks
                sanitized_include_tasks_name = sanitize_for_mermaid_id(
                    f"{task_name}_{check_style_included_tasks}_{i}")
                sanitized_include_tasks_title = sanitize_for_title(
                    f"{check_style_included_tasks}")
                mermaid_data += f'\n  {last_node}-->|Include task| {sanitized_include_tasks_name}[{sanitized_task_title}<br>include_task: {sanitized_include_tasks_title}]:::includeTasks'
                last_node = sanitized_include_tasks_name

            elif task_module_import_tasks:
                if isinstance(task_module_import_tasks, dict):
                    check_style_imported_tasks = task_module_import_tasks.get(
                        ANSIBLE_INCLUDE_FILE_KEY, task_module_import_tasks)
                else:
                    check_style_imported_tasks = task_module_import_tasks
                sanitized_imported_tasks_name = sanitize_for_mermaid_id(
                    f"{task_name}_{check_style_imported_tasks}_{i}")
                sanitized_imported_tasks_title = sanitize_for_title(
                    f"{check_style_imported_tasks}")
                mermaid_data += f'\n  {last_node}-->|Import task| {sanitized_imported_tasks_name}[/{sanitized_task_title}<br>import_task: {sanitized_imported_tasks_title}/]:::importTasks'
                last_node = sanitized_imported_tasks_name

            elif task_module_import_playbook:
                if isinstance(task_module_import_playbook, dict):
                    check_style_import_playbook = task_module_import_playbook.get(
                        ANSIBLE_INCLUDE_FILE_KEY, task_module_import_playbook)
                else:
                    check_style_import_playbook = task_module_import_playbook
                sanitized_import_playbook_name = sanitize_for_mermaid_id(
                    f"{task_name}_{check_style_import_playbook}_{i}")
                sanitized_import_playbook_title = sanitize_for_title(
                    f"{check_style_import_playbook}")
                mermaid_data += f'\n  {last_node}-->|Import playbook| {sanitized_import_playbook_name}[/{sanitized_task_title}<br>import_playbook: {sanitized_import_playbook_title}/]:::importPlaybook'
                last_node = sanitized_import_playbook_name

            elif task_module_include_role:
                if isinstance(task_module_include_role, dict):
                    check_style_include_role = task_module_include_role.get(
                        ANSIBLE_INCLUDE_ROLE_NAME_KEY, task_module_include_role)
                else:
                    check_style_include_role = task_module_include_role
                sanitized_include_role_name = sanitize_for_mermaid_id(
                    f"{task_name}_{check_style_include_role}_{i}")
                sanitized_include_role_title = sanitize_for_title(
                    check_style_include_role)
                mermaid_data += f'\n  {last_node}-->|Include role| {sanitized_include_role_name}({sanitized_task_title}<br>include_role: {sanitized_include_role_title}):::includeRole'
                last_node = sanitized_include_role_name

            elif task_module_import_role:
                if isinstance(task_module_import_role, dict):
                    check_style_import_role = task_module_import_role.get(
                        ANSIBLE_INCLUDE_ROLE_NAME_KEY, task_module_import_role)
                else:
                    check_style_import_role = task_module_import_role
                sanitized_import_role_name = sanitize_for_mermaid_id(
                    f"{task_name}_{check_style_import_role}_{i}")
                sanitized_import_role_title = sanitize_for_title(
                    check_style_import_role)
                mermaid_data += f'\n  {last_node}-->|Import role| {sanitized_import_role_name}([{sanitized_task_title}<br>import_role: {sanitized_import_role_title}]):::importRole'
                last_node = sanitized_import_role_name

            elif task_module_include_vars:
                if isinstance(task_module_include_vars, dict):
                    check_style_include_vars = task_module_include_vars.get(
                        ANSIBLE_INCLUDE_FILE_KEY, False) or task_module_include_vars.get(ANSIBLE_INCLUDE_DIR_KEY, task_module_include_vars)
                else:
                    check_style_include_vars = task_module_include_vars
                sanitized_include_vars_name = sanitize_for_mermaid_id(
                    f"{task_name}_{check_style_include_vars}_{i}")
                sanitized_include_vars_title = sanitize_for_title(
                    check_style_include_vars)
                mermaid_data += f'\n  {last_node}-->|Include vars| {sanitized_include_vars_name}[{sanitized_task_title}<br>include_vars: {sanitized_include_vars_title}]:::includeVars'
                last_node = sanitized_include_vars_name

            else:
                mermaid_data += f'\n  {last_node}-->|Task| {sanitized_task_name}[{sanitized_task_title}]:::task'
                last_node = sanitized_task_name

    if parent_node and not in_rescue_block and not has_rescue:
        end_label = MERMAID_END_OF_BLOCK_LABEL
        mermaid_data += f'\n  {last_node}-.->|{end_label}| {parent_node}'

    return last_node, mermaid_data


def generate_mermaid_playbook(playbook):
    mermaid_data = MERMAID_FLOWCHART_HEADER
    for play in playbook:
        hosts = play.get(ANSIBLE_PLAY_HOSTS_KEY, MERMAID_UNDEFINED_HOST)
        tasks = play.get(ANSIBLE_PLAY_TASKS_KEY, [])
        roles = play.get(ANSIBLE_PLAY_ROLES_KEY, [])
        if not isinstance(hosts, list):
            hosts = [hosts]
        sanitized_hosts = []
        for host in hosts:
            host = re.sub(r"{{\s*(\w+)\s*}}", r"\1", host)
            host = sanitize_for_mermaid_id(host)
            sanitized_hosts.append(host)
        sanitized_hosts = ", ".join(sanitized_hosts)
        sanitized_hosts = f"{MERMAID_HOSTS_NODE_PREFIX}{sanitized_hosts}{MERMAID_HOSTS_NODE_SUFFIX}"
        last_node = sanitized_hosts
        if roles:
            for i, role in enumerate(roles):
                role_name = role[ANSIBLE_ROLE_NAME_KEY] if isinstance(role, dict) else role
                role_name = role_name if role_name else f"{MERMAID_UNNAMED_ROLE_PREFIX}{i}"
                role_name = re.sub(r"{{\s*(\w+)\s*}}", r"\1", role_name)
                sanitized_role_name = sanitize_for_mermaid_id(role_name)
                sanitized_role_title = sanitize_for_title(role_name)
                mermaid_data += f'\n  {last_node}-->|Role| {sanitized_role_name}[{sanitized_role_title}]'
                last_node = sanitized_role_name
        last_node, mermaid_data = process_tasks(tasks, last_node, mermaid_data)
    return mermaid_data


def generate_mermaid_role_tasks_per_file(tasks_per_file):
    mermaid_codes = {}
    for task_info in tasks_per_file:
        task_file = task_info[TASK_INFO_KEY_FILE]
        tasks = task_info[TASK_INFO_KEY_MERMAID]
        mermaid_data = f"{MERMAID_FLOWCHART_HEADER}\n{MERMAID_START_NODE}\n" + "\n".join(MERMAID_CLASSDEF_LINES) + "\n"
        last_node = MERMAID_START_NODE
        last_node, mermaid_data = process_tasks(tasks, last_node, mermaid_data)
        mermaid_data += f'\n  {last_node}-->{MERMAID_END_NODE}'
        mermaid_codes[task_file] = mermaid_data

    return mermaid_codes
