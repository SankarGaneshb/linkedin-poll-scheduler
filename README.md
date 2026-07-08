# LinkedIn Poll Scheduler

A starter application to prepare, validate, and manage LinkedIn poll posts from a structured YAML configuration. It prepares scheduled poll definitions and is intended to be connected to an approved publishing workflow.

## What this app does
- **Structured Definitions**: Stores poll content in structured YAML files.
- **Validation**: Automatically validates question length, option limits, and date formats before scheduling.
- **Queue Generation**: Validates and displays the schedule of poll jobs in chronological order.
- **Robust Execution**: Features a dry-run mode to verify schedules without publishing.
- **AI Poll Generation**: Automatically generates poll content from topics or JSON files using the Gemini API.
- **Local Testing**: Built-in automated unit tests to ensure validation logic reliability.

## Configuration Schema

Poll configurations are defined in YAML files under the `polls` list. Each poll block supports the following keys:

| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `question` | String | Yes | The poll question text (cannot be empty). |
| `options` | List of String | Yes | A list of 2 to 4 choices for the poll (cannot be empty). |
| `publish_at` | String or Datetime | Yes | Scheduled date/time in ISO-8601 format (e.g., `"2026-07-12T09:30:00"`). |
| `timezone` | String | Yes | IANA timezone identifier (e.g., `"Asia/Kolkata"`). |
| `audience` | String | No | Target audience (e.g., `"public"` or `"connections"`). Defaults to `"public"`. |
| `dry_run` | Boolean | No | Flags if the publication should be simulated. Defaults to `true`. |

### Example Config (`config/polls.example.yaml` / `config/my-next-week-polls.yaml`)
```yaml
polls:
  - question: "Which AI workflow helps your team most?"
    options:
      - "Prompt templates"
      - "Agent orchestration"
      - "Evaluation pipelines"
      - "Deployment automation"
    publish_at: "2026-07-12T09:30:00"
    timezone: "Asia/Kolkata"
    audience: "public"
    dry_run: true
```

## Quick Start

### 1. Setup Environment
**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Linux / macOS / Bash:**
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Run Scheduler CLI
Verify the example schedule:
```bash
python src/scheduler.py --config config/polls.example.yaml --dry-run
```

Validate your custom schedule:
```bash
python src/scheduler.py --config config/my-next-week-polls.yaml
```

---

## AI Poll Generator

You can automatically generate new polls using the Gemini API and append them to your YAML schedule file.

### 1. Set your Gemini API Key
Either set it as an environment variable:
```bash
# Windows (PowerShell)
$env:GEMINI_API_KEY="your-api-key"

# Linux / macOS / Bash
export GEMINI_API_KEY="your-api-key"
```
Or pass it directly to the CLI using the `--api-key` flag.

### 2. Generate Polls
Generate a poll from a single topic:
```bash
python src/generator.py --topic "AI Governance" --num-polls 1
```

Generate polls from a JSON topic file:
```bash
python src/generator.py --topic-file config/topics.json --num-polls 1
```

### JSON Topic File Structure
The generator safely parses various JSON structures:
- **Simple Array**: `["AI Governance", "MLOps"]`
- **Object with `topics`**: `{"topics": ["AI Governance", "Ethics"]}`
- **Object with `topic`**: `{"topic": "AI Governance"}`
- **Key-Value Dictionary**: `{"a": "AI Governance", "b": "MLOps"}` (values are treated as topics)

### Generator CLI Options
- `--topic`: A single topic string.
- `--topic-file`: Path to a JSON file containing topic(s).
- `--api-key`: Gemini API Key (optional, defaults to `GEMINI_API_KEY` env var).
- `--output`: Path to write the output YAML file (defaults to `config/my-next-week-polls.yaml`).
- `--num-polls`: Number of polls to generate per topic (default: 1).

---

## Running Automated Tests

A unit test suite is included in the `tests/` directory to verify validation, parsing, and generator logic.

To run the automated tests, execute:
```bash
python -m unittest discover -s tests
```

## Project Structure
- `src/scheduler.py` - Main scheduler command-line interface.
- `src/generator.py` - AI poll generation CLI tool using Gemini API.
- `src/models.py` - Core dataclasses representing poll jobs.
- `src/validator.py` - Poll formatting and requirement validation logic.
- `config/polls.example.yaml` - Template configuration file.
- `config/my-next-week-polls.yaml` - Your active custom schedule.
- `tests/test_validator.py` - Unit tests for validation edge cases.
- `tests/test_scheduler.py` - Unit tests for configuration parsing and loading.
- `tests/test_generator.py` - Unit tests for topic loading and mock API responses.
- `docs/USAGE.md` - Additional usage and extension guide.

## Disclaimer
This project is designed as an internal tool to manage and pre-validate content. It does not bypass LinkedIn API platform restrictions and does not include browser automation for posting. Connect this schedule queue output to your approved publishing platform or OAuth-enabled publishing worker.
