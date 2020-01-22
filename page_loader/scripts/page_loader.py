#!/usr/bin/env python3

import sys
from page_loader.cli import parse_args
from page_loader.engine import engine


def main():
    # sys.argv added for testability
    args = parse_args(sys.argv[1:])
    engine(args)


if __name__ == '__main__':
    main()
