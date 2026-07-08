# LinkedIn Poll Scheduler

A starter app to prepare, schedule, and manage LinkedIn poll posts from a structured YAML configuration.

## What this app does
- Stores poll definitions in YAML.
- Validates poll structure before scheduling.
- Generates a run queue for scheduled publication.
- Supports dry-run mode for safe verification.
- Provides a simple CLI for local execution.

## Current scope
This starter package is designed to be ready for local use and extension. It does not bypass LinkedIn platform restrictions and does not include unofficial browser automation for posting to LinkedIn.

## Quick start
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/scheduler.py --config config/polls.example.yaml --dry-run
```

## Project structure
- `src/scheduler.py` - main scheduler CLI
- `src/models.py` - poll data model helpers
- `src/validator.py` - validation logic
- `config/polls.example.yaml` - editable sample poll schedule
- `docs/USAGE.md` - detailed usage guide
- `scripts/run_example.sh` - helper script

## Notes
Use this app to manage poll content and scheduling workflows. Connect it to your approved publishing workflow or internal posting layer.
