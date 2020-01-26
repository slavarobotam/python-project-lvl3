#!/usr/bin/env python3

import sys
from page_loader.cli import run_cli
from page_loader.engine import run_engine
import requests


def main():
    try:
        # sys.argv added for testability
        args = run_cli(sys.argv[1:])
        run_engine(args)

    except (PermissionError, FileNotFoundError):
        sys.exit(1)
    except (requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            requests.exceptions.RequestException):
        sys.exit(1)
    except Exception:
        sys.exit(1)


if __name__ == '__main__':
    main()
