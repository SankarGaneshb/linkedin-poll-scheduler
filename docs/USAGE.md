# Usage

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run example schedule
```bash
python src/scheduler.py --config config/polls.example.yaml --dry-run
```

## Create your own schedule
1. Copy `config/polls.example.yaml`.
2. Update the question, options, publish time, timezone, and audience.
3. Run the validator through the scheduler CLI.

## Expected format
- `question`: poll text
- `options`: list of 2 to 4 options
- `publish_at`: ISO datetime like `2026-07-12T09:30:00`
- `timezone`: IANA timezone like `Asia/Kolkata`
- `audience`: optional, for your workflow metadata
- `dry_run`: optional boolean

## Extension ideas
- Add calendar integration.
- Add queue persistence.
- Add approved posting integration.
- Add unit tests with pytest.
