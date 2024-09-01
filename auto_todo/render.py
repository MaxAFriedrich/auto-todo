from auto_todo.custom import get_main_list, CustomTasks


# Render a markdown file of tables to the same location as main_list
# one table for each asignee, and one for no asignees

def has_none(tasks: CustomTasks, assignee):
    for task in tasks.tasks:
        if assignee in task.assignees:
            return False
    return True


def render_table_unassigned(tasks: CustomTasks) -> str:
    markdown = '# Unassigned\n\n'

    markdown += '| Task | Priority | Urgency | Importance | Projects | Due |\n'
    markdown += '|------|----------|---------|------------|----------|-----|\n'
    for task in tasks.tasks:
        if len(task.assignees) == 0:
            markdown += (
                f'| {task.striped_todo} | {task.priority} | {task.urgency} | '
                f'{task.importance} | {", ".join(task.projects)} | '
                f'{task.due_date} |\n')

    markdown += '\n'
    return markdown


def render_table(tasks: CustomTasks, assignee) -> str:
    pretty_assignee = assignee[2:].title()

    markdown = f'# {pretty_assignee}\n\n'

    if has_none(tasks, assignee):
        return markdown + "No tasks\n"
    markdown += '| Task | Priority | Urgency | Importance | Projects | Due |\n'
    markdown += '|------|----------|---------|------------|----------|-----|\n'
    for task in tasks.tasks:
        if assignee in task.assignees:
            markdown += (
                f'| {task.striped_todo} | {task.priority} | {task.urgency} | '
                f'{task.importance} | {", ".join(task.projects)} | '
                f'{task.due_date} |\n')

    markdown += '\n'
    return markdown


def render():
    main_list = get_main_list()
    assignees = set()
    for task in main_list.tasks:
        assignees.update(task.assignees)

    markdown = ("**WARNING: This file is auto-generated. Do not edit "
                "manually.**\n\n")
    for assignee in assignees:
        markdown += render_table(main_list, assignee)

    markdown += render_table_unassigned(main_list)

    with open(main_list.path.with_suffix('.md'), 'w') as f:
        f.write(markdown)
