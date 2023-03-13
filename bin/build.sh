#!/bin/bash

ProjectBin=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Activate te development environment.
source $ProjectBin/activate

cd $ProjectBin/..

python3 $ProjectBin/IncrementVersion.py $ProjectBin/..pyproject.toml
python3 -m build




# Obsolete; fuck jupyter. See Issue #9.
# Left for posterity.
function CompileJupyter() {

    # Compile notebook to python source.
    jupyter nbconvert --to python \
	                  --output-dir="$ProjectBin/../src/Lab93_chat" \
		              --output="ChatSystem"

    # Compile new readme file.
    jupyter nbconvert --to markdown \
	                  --output-dir="$ProjectBin/.." \
		              --output="readme"
}