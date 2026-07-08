#!/usr/bin/env bash
set -e
python src/scheduler.py --config config/polls.example.yaml --dry-run
