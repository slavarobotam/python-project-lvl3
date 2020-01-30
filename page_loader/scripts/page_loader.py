#!/usr/bin/env python3

import sys

from page_loader.cli import parse_args
from page_loader.engine import run_engine
from page_loader.logging import run_logging


def main():
    args = parse_args(sys.argv[1:])
    run_logging(args.level, args.filepath)
    if not run_engine(args):
        sys.exit(1)


if __name__ == '__main__':
    main()
