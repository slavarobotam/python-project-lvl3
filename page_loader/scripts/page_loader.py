#!/usr/bin/env python3

import sys
from page_loader.cli import parse_args
from page_loader.engine import engine


def main():
    storage_dir, url = parse_args(sys.argv[1:])  # argument needed for tests
    engine(storage_dir, url)


if __name__ == '__main__':
    main()
