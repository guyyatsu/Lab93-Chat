#!/bin/bash

# Project binary directory.
ProjectBin=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Create virtual environment in the project directory.
cd $ProjectBin/../.. && python3 -m venv $ProjectBin/..

# Move to virtual environment & install requirements.
cd $ProjectBin/../.. && pip install -r requirements.txt