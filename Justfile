#!/usr/bin/env just --justfile

source_dirs := "yaclog_ksp/"

# Lint python source code
lint:
    pyflakes {{ source_dirs }}
    black --check {{ source_dirs }}

# Format python source code and other support files
format:
    black {{ source_dirs }}
    yaclog format
    just --fmt --unstable

# Build distribution
build:
    python -m build
