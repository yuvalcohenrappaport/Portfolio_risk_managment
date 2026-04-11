#!/bin/bash
export VIRTUAL_ENV="/home/yuval/trading/.venv"
export PATH="$VIRTUAL_ENV/bin:$PATH"
cd /home/yuval/trading
exec python import_subprocess.py
