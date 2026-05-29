#!/usr/bin/env bash
# Vitalis Core Launcher
cd "$(dirname "$0")/.."
echo "⚡️ Initializing Vitalis Core Engine..."
# Launching the core module
python3 -m vitalis.__main__ "$@"
