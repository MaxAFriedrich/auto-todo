import argparse
from enum import Enum


class Action(Enum):
    SORT = 'sort'
    WEB = 'web'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', help='The action to perform')
    parser.add_argument('file', help='The file to parse')
    args = parser.parse_args()
    match args.action:
        case Action.SORT:
            from .sort_it import sort_list
            sort_list(args.file)
        case Action.WEB:
            from .web import run_server
            run_server(args.file)
        case _:
            print('Invalid action')


if __name__ == '__main__':
    main()
