#!/bin/bash
# Convenience script for running LPMD files

cd /Users/abhishekshivakumar/4096
source venv/bin/activate
python lpmd_executor.py "$@"
