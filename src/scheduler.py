import argparse
from datetime import datetime
from pathlib import Path
import sys
import yaml

from models import PollJob
from validator import validate_poll_dict


def load_jobs(config_path: Path) -> list[PollJob]:
    data = yaml.safe_load(config_path.read_text()) or {}
    items = data.get("polls", [])
    jobs = []
    for idx, item in enumerate(items, start=1):
        errors = validate_poll_dict(item)
        if errors:
            joined = "; ".join(errors)
            raise ValueError(f"Poll #{idx} is invalid: {joined}")
        
        pub_at = item["publish_at"]
        if isinstance(pub_at, str):
            pub_at = datetime.fromisoformat(pub_at)

        jobs.append(
            PollJob(
                question=item["question"].strip(),
                options=[str(opt).strip() for opt in item["options"]],
                publish_at=pub_at,
                timezone=item["timezone"],
                audience=item.get("audience", "public"),
                dry_run=bool(item.get("dry_run", True)),
            )
        )
    return jobs



def print_schedule(jobs: list[PollJob]) -> None:
    for idx, job in enumerate(sorted(jobs, key=lambda x: x.publish_at), start=1):
        print(f"[{idx}] {job.publish_at.isoformat()} {job.timezone} :: {job.question}")
        for opt_idx, option in enumerate(job.options, start=1):
            print(f"    {opt_idx}. {option}")
        print(f"    audience={job.audience} dry_run={job.dry_run}")


def main() -> int:
    parser = argparse.ArgumentParser(description="LinkedIn Poll Scheduler starter CLI")
    parser.add_argument("--config", required=True, help="Path to YAML config file")
    parser.add_argument("--dry-run", action="store_true", help="Force dry-run output")
    args = parser.parse_args()

    config_path = Path(args.config)
    if not config_path.exists():
        print(f"Config file not found: {config_path}", file=sys.stderr)
        return 1

    jobs = load_jobs(config_path)
    if args.dry_run:
        for job in jobs:
            job.dry_run = True

    print_schedule(jobs)
    print(f"Loaded {len(jobs)} scheduled poll job(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
