#!/bin/bash

# Binary directory local to the project.
ProjectBin=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Move to the project directory and start a new branch.
cd $ProjectBin/.. && python3 $ProjectBin/BuildFunctions.py --branch

# Open the Vim IDE.  Note that NERDTree is useful here.
vim $ProjectBin/../src/Lab93_Chat/

# Add your patches and push your commits.
python3 $ProjectBin/BuildFunctions.py --enumerate

# Increment the build version in the project file.
python3 $ProjectBin/BuildFunctionspy --increment --file $ProjectBin/..pyproject.toml

# Build and upload the pip package.
python3 -m build && python3 -m twine upload $ProjectBin/../dist/*