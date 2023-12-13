#!/bin/bash

set -eo pipefail

cd /home/${USER}/git/legiontd/ltd-tool-mysql
python3 main.py

cd /home/${USER}/git/proleak.github.io/

git add .
git commit -m "Update $(date +%F)"
git push