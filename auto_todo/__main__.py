import argparse
from enum import Enum
from pathlib import Path

from auto_todo.config import Config


class Action(Enum):
    SORT = 'sort'
    WEB = 'web'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', help='The action to perform')
    args = parser.parse_args()
    match Action(args.action):
        case Action.SORT:
            from .sort_it import sort_list
            sort_list(Path(Config().main_list))
        case Action.WEB:
            from .web import run_server
            run_server()
        case _:
            print('Invalid action')


if __name__ == '__main__':
    main()
