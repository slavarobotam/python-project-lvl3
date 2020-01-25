#!/usr/bin/env python3

import sys
from page_loader.cli import parse_args
from page_loader.engine import engine
import requests


def main():
    args = parse_args(sys.argv[1:])  # sys.argv added for testability
    try:
        engine(args)
    except (PermissionError, FileNotFoundError):
        sys.exit(1)
    except requests.exceptions.RequestException:
        sys.exit(1)


if __name__ == '__main__':
    main()
