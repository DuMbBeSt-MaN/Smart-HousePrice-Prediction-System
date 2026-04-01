#!/bin/bash
cd "$(dirname "$0")"
export PYTHONPATH="$(pwd)"
uvicorn app.main:app --reload
