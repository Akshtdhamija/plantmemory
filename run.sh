#!/usr/bin/env bash
# One-command launch: set up a local venv, install the one dependency, start the
# hub, and open the dashboard in your browser.
set -e
cd "$(dirname "$0")"

if [ ! -d .venv ]; then
  python3 -m venv .venv
fi
# shellcheck disable=SC1091
. .venv/bin/activate
pip install -q -r requirements.txt
python -m plant_memory hub
