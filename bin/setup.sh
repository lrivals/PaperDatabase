#!/usr/bin/env bash
# Crée le venv local et installe requirements.txt. Idempotent.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [ -d .venv ]; then
  echo "venv déjà présent : .venv"
else
  if ! python3 -m venv .venv; then
    python3 -m pip install -q --target .cache/virtualenv virtualenv
    PYTHONPATH=.cache/virtualenv python3 -m virtualenv --clear .venv
  fi
  echo "venv créé : .venv"
fi
.venv/bin/pip install -q -r requirements.txt
.venv/bin/python -c "import pymupdf, lxml, requests, slugify; print('ok')"
