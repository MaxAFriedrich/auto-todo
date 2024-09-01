import os
from pathlib import Path

from .parser import Tasks


def priority_float_to_char(value: float) -> str:
    # Define the lookup table
    lookup_table = {
        0.9: 'B',
        0.7: 'C',
        0.5: 'D',
        0.2: 'E',
        0.1: 'F',
        0.0: 'G'  # This will handle values less than 0.1
    }

    # Iterate through the lookup table in descending order
    for threshold in sorted(lookup_table.keys(), reverse=True):
        if value >= threshold:
            return lookup_table[threshold]

    return 'G'  # Default case for values less than 0.1


def urgency_to_float(urgency: str) -> float:
    lookup_table = {
        '@u1': 1,
        '@u2': 0.8,
        '@u3': 0.4,
        '@u4': 0.2,
    }
    return lookup_table.get(urgency, 0)


def importance_to_float(importance: str) -> float:
    lookup_table = {
        '@i1': 0.9,
        '@i2': 0.7,
        '@i3': 0.3,
        '@i4': 0.1,
    }
    return lookup_table.get(importance, 0)


def assign_priority(task):
    if task.priority == 'A':
        return task

    urgency = None
    importance = None

    for context in task.contexts:
        if context.startswith('@u'):
            urgency = urgency_to_float(context)
        elif context.startswith('@i'):
            importance = importance_to_float(context)

    if urgency and importance:
        priority_float = urgency * importance
        task.priority = priority_float_to_char(priority_float)
    return task


def clean_file(tasks: Tasks):
    # remove creation and completion dates
    for task in tasks.tasks:
        task.created_date = None
        task.finished_date = None
        task.raw_todo = None
    return tasks


def commit_file(file):
    os.system(f"git add {file}")
    os.system(f"git commit -m 'Updated {file} by sort_it.py'")


def sort_list(file: Path):
    # Load tasks from file
    tasks = Tasks(path=file)
    print(tasks, file, file.read_text())
    tasks.load()

    tasks = clean_file(tasks)

    # Assign priority based on urgency and importance
    for task in tasks.tasks:
        assign_priority(task)

    # Sort tasks by priority
    sorted_tasks = (
        tasks
        .order_by('priority')
        .order_by('projects')
        .order_by('finished')
    )

    # Save sorted tasks back to file
    sorted_tasks.save(file)
