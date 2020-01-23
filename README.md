# Page_loader
[![Maintainability](https://api.codeclimate.com/v1/badges/6618e09548c56dd08217/maintainability)](https://codeclimate.com/github/slavarobotam/python-project-lvl3/maintainability)  [![Test Coverage](https://api.codeclimate.com/v1/badges/6618e09548c56dd08217/test_coverage)](https://codeclimate.com/github/slavarobotam/python-project-lvl3/test_coverage)  [![Build Status](https://travis-ci.org/slavarobotam/python-project-lvl3.svg?branch=master)](https://travis-ci.org/slavarobotam/python-project-lvl3)


Page_loader is a free and easy-to-use utility for downloading pages.

### Installation:

```sh
$ pip install --user --index-url https://test.pypi.org/simple/ \
    --extra-index-url https://pypi.org/simple/ slavarobotam_page_loader
```

### How to use

If you want to **download a page**, just run:
``` bash
$ page-loader https://example.com/
```
---
You can specify the **storage directory** with `-o`(or `--output`) parameter.
```sh
$ page-loader -o=mydownloads https://example.com/
```
Default storage is your current working directory.

---
**Level of logging** is chosen with `-l`(or `--level`) parameter:
```sh
$ page-loader -l=debug https://example.com/
```
Levels are `info` (for basic information about the process) or `debug` for maximum details.

### Installation and base functionality

[![asciicast](https://asciinema.org/a/293203.svg)](https://asciinema.org/a/293203)

### Logging feature

[![asciicast](https://asciinema.org/a/295009.svg)](https://asciinema.org/a/295009)

### Error handling

[![asciicast](https://asciinema.org/a/295544.svg)](https://asciinema.org/a/295544)

### Progress bar

[![asciicast](https://asciinema.org/a/295571.svg)](https://asciinema.org/a/295571)