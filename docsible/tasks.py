"""Module with function for manage block and rescue code"""

from docsible.constants import (
    KNOWN_TASK_PARAMS,
    TASK_ACTION_KEY,
    TASK_BLOCK_TYPES,
    TASK_DEFAULT_NAME,
    TASK_MODULE_INDICATOR_KEYS,
    TASK_NAME_KEY,
    TASK_TYPE_DEFAULT,
    TASK_UNKNOWN_MODULE,
    TASK_WHEN_KEY,
    TASK_WITH_PREFIX,
)


def escape_pipes(text):
    """Function to escape pipes in string or list"""
    if isinstance(text, str):
        return text.replace("|", r"¦")
    if isinstance(text, list):
        return [escape_pipes(item) for item in text]
    return text  # Return the text as is if it's not a string or list.


def process_special_task_keys(task, task_type=TASK_TYPE_DEFAULT):
    """Function to process tasks, including block and rescue constructs."""
    tasks = []

    for block_type in TASK_BLOCK_TYPES:
        if block_type in task:
            task_name = task.get(TASK_NAME_KEY, f'{TASK_DEFAULT_NAME}_{block_type}')
            task_module = block_type
            task_when = escape_pipes(task.get(TASK_WHEN_KEY, None))
            tasks.append({
                'name': escape_pipes(task_name),
                'module': task_module,
                'type': block_type,
                'when': task_when
            })
            for sub_task in task[block_type]:
                processed_tasks = process_special_task_keys(
                    sub_task, block_type)
                tasks.extend(processed_tasks)
            return tasks  # Exit after processing block, rescue, or always

    # Handle regular tasks
    task_name = task.get(TASK_NAME_KEY, TASK_DEFAULT_NAME)
    task_when = escape_pipes(task.get(TASK_WHEN_KEY, None))

    # Determine module name based on known task indicators or default to 'unknown'
    task_module = TASK_UNKNOWN_MODULE  # Default module if not found
    if TASK_ACTION_KEY in task:
        action = task[TASK_ACTION_KEY]
        if isinstance(action, dict):
            # Module name from action dict
            task_module = list(action.keys())[0]
        else:
            task_module = action  # Module name as action string
    else:
        # Specific modules without 'action' key
        for key in TASK_MODULE_INDICATOR_KEYS:
            if key in task:
                task_module = key
                break

    # Ensure only relevant modules are shown and not general parameters like 'name' or 'when'
    if task_module == TASK_UNKNOWN_MODULE:
        module_keys = [key for key in task.keys()
                       if key not in KNOWN_TASK_PARAMS and not key.startswith(TASK_WITH_PREFIX)]
        task_module = module_keys[0] if module_keys else TASK_UNKNOWN_MODULE

    tasks.append({
        'name': escape_pipes(task_name),
        'module': task_module if task_module != TASK_UNKNOWN_MODULE else '',  # Blank if unknown
        'type': task_type,
        'when': task_when
    })
    return tasks
