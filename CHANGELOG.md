# Changelog

All notable changes to this project will be documented in this file.

## 1.0.0 - 2021-05-07

### Changed

- Updated API for yaclog to 1.0.0
- Renamed '--input' option to '--path' for consistency with yaclog, and added an environment variable for its value


## 0.2.0 - 2021-05-06

### Changed

- Generator now adds a comment to files stating they were automatically created by this tool.
- Tweaks and fixes to project metadata in setup.cfg.
- Marked version compatibility with yaclog.


## 0.1.1 - 2021-04-16

yaclog-ksp is [now available on PyPi!](https://pypi.org/project/yaclog-ksp/)

### Changed

- Generator will now use change values instead of nodes when possible for more concise output files.


## 0.1.0 - 2021-04-16

First release

### Added

- `yaclog-ksp` command line tool for converting markdown changelogs to KerbalChangelog configs.