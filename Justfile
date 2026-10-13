#!/usr/bin/env just --justfile

# Lint python source code
lint:
    python -m flake8 yaclog/

# Format python source code and other support files
format:
    python -m black yaclog/
    python -m yaclog format
    just --fmt

# Build distribution
build:
    python -m build