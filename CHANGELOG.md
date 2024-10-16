# Changelog

All notable changes to this project will be documented in this file.

## Version 1.1.0 - 2024-10-16

### Changed

- Relicensed code under Apache-2.0 license
- Dropped support for python 3.8


## Version 1.0.4 - 2024-09-09

### Fixed

- Fixed action failint to run


## Version 1.0.3 - 2024-08-27

### Changed

- Adjusted dependencies. Click <8 is no longer supported
- When stdout is not a tty, only the output file path is printed

### Added

- Added Github Action


## Version 1.0.2 - 2021-05-12

### Changed

- Updated to support Click version 8


## Version 1.0.0 - 2021-05-07

### Changed

- Updated API for yaclog to 1.0.0
- Renamed '--input' option to '--path' for consistency with yaclog, and added an environment variable for its value


## Version 0.2.0 - 2021-05-06

### Changed

- Generator now adds a comment to files stating they were automatically created by this tool.
- Tweaks and fixes to project metadata in setup.cfg.
- Marked version compatibility with yaclog.


## Version 0.1.1 - 2021-04-16

yaclog-ksp is [now available on PyPi!](https://pypi.org/project/yaclog-ksp/)

### Changed

- Generator will now use change values instead of nodes when possible for more concise output files.


## Version 0.1.0 - 2021-04-16

First release

### Added

- `yaclog-ksp` command line tool for converting markdown changelogs to KerbalChangelog configs.