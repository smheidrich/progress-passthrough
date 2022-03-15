#!/bin/bash
# generate setup.py to allow editable installs

# see https://github.com/python-poetry/poetry/issues/761#issuecomment-689491920
poetry build
tar -xvf dist/*.tar.gz --wildcards --no-anchored '*/setup.py' --strip=1
