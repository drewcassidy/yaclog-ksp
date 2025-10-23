# yaclog-ksp

[![CI Status](https://git.offworldcolonies.nexus/drewcassidy/yaclog-ksp/badges/workflows/build.yml/badge.svg?branch=main&label=build)](https://git.offworldcolonies.nexus/drewcassidy/yaclog-ksp/actions)
[![PyPI version](https://img.shields.io/pypi/v/yaclog-ksp)](https://pypi.org/project/yaclog-ksp/)

A command line tool based on [yaclog] for converting markdown changelogs to [KerbalChangelog] config files.

![a yak who is a log](https://git.offworldcolonies.nexus/drewcassidy/yaclog/raw/branch/main/logo.png)

*Logo by Erin Cassidy*

## Installation

Install and update with [pip](https://pip.pypa.io/en/stable/getting-started/):

```shell
$ pip install -U yaclog-ksp
```

Or with [uv](https://docs.astral.sh/uv/getting-started/):

```shell
$ uv tool install yaclog-ksp
```

## Usage

```
Usage: yaclog-ksp [OPTIONS]

  Converts markdown changelogs to KSP changelog configs.

Options:
  --path FILE        Location of the changelog file.  [default: CHANGELOG.md]
  -o, --output FILE  Output file to write to. Uses
                     'GameData/{name}/Versioning/{name}ChangeLog.cfg' by
                     default.

  -n, --name TEXT    The name of the mod. Derived from the current directory
                     by default.

  --version          Show the version and exit.
  --help             Show this message and exit.
```

for example, running `yaclog-ksp --path MyLog.md -n "My KSP Mod"`
would output to `GameData/MyKSPMod/Versioning/MyKSPModChangeLog.cfg`

Input files are in markdown, and use a certain syntax to be readable by the tool. Metadata is included in a table at the
top of the file (which row you make the header doesnt matter). Each version is an subheading with the version, an
optional date, and the KSP version as a tag on the end in brackets

#### Example Changelog:

```markdown
# Changelog

This is the changelog for my cool mod!

| modName | MyCoolMod     |
| ------- | ------------- |
| license | CC-By-SA      |
| website | Example.com   |
| author  | A cool person |

## 1.0.0 - 2020-04-16 [KSP 1.11]

First full release

### Fixed

- Nyan Cat now has correct music

### Added

- Multiplayer

## 0.9.1 [KSP 1.10.1]

Supported versions: 0.2.0 beta to 1.10.x

### Changed

A very complicated thing that I can't easily explain in bullet points, 
but this paragraph works pretty well to get the point across!

- Another thing that has multiple specific items
    - this bullet point
    * and this other one
    + oh and another one!

### Removed

- Herobrine

```

[yaclog]: https://git.offworldcolonies.nexus/drewcassidy/yaclog
[KerbalChangelog]: https://github.com/HebaruSan/KerbalChangelog