#!/usr/bin/env python3

from page_loader.engine import parser, engine


def main():
    args = parser.parse_args()
    engine(args)


if __name__ == '__main__':
    main()
