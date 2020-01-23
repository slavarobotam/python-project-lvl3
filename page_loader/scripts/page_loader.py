#!/usr/bin/env python3

import sys
from page_loader.cli import parse_args
from page_loader.engine import engine


def main():
    args = parse_args(sys.argv[1:])  # sys.argv added for testability
    engine(args)


if __name__ == '__main__':
    main()
