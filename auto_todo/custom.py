from dataclasses import dataclass
from pathlib import Path

from auto_todo.parser import Task, Tasks
from auto_todo.web import config


@dataclass
class CustomTask(Task):

    def __init__(self, raw_todo: str, id: int):
        super().__init__(raw_todo=raw_todo, id=id)

    @property
    def urgency(self) -> int:
        # find `@u1`
        for context in self.contexts:
            if context.startswith('@u'):
                return int(context[2:])

    @property
    def importance(self) -> int:
        # find `@i1`
        for context in self.contexts:
            if context.startswith('@i'):
                return int(context[2:])

    @property
    def assignees(self) -> list[str]:
        # find `@a:bob`
        return [context[3:] for context in self.contexts if
                context.startswith('@a:')]

    @property
    def due_date(self) -> str:
        # find `due:2021-12-31`
        for context in self.contexts:
            if context.startswith('due:'):
                return context[4:]


class CustomTasks(Tasks):
    def __init__(self, path: Path):
        super().__init__(path=path)

    def load(self):
        self._trigger_event('load')

        self.tasks = [
            CustomTask(line.strip(), i) for i, line in
            enumerate(self.path.read_text().splitlines())
        ]

        self._trigger_event('loaded')


def get_tasks_from_file(file: Path) -> CustomTasks:
    tasks = CustomTasks(path=file)
    tasks.load()
    return tasks


def get_main_list() -> CustomTasks:
    return get_tasks_from_file(config.main_list)
