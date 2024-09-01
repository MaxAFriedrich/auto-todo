import argparse
from enum import Enum

from auto_todo.config import Config


class Action(Enum):
    SORT = 'sort'
    WEB = 'web'
    RENDER = 'render'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', help='The action to perform')
    args = parser.parse_args()
    match Action(args.action):
        case Action.SORT:
            from .sort_it import sort_list
            sort_list(Config().main_list)
        case Action.WEB:
            from .web import run_server
            run_server()
        case Action.RENDER:
            from .render import render
            render()
        case _:
            print('Invalid action')


if __name__ == '__main__':
    main()
