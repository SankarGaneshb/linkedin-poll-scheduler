from datetime import datetime


def validate_poll_dict(item: dict) -> list[str]:
    errors = []
    question = item.get("question", "").strip()
    options = item.get("options", [])
    publish_at = item.get("publish_at", "")
    timezone = item.get("timezone", "")

    if not question:
        errors.append("question is required")
    if not isinstance(options, list) or len(options) < 2:
        errors.append("at least 2 options are required")
    if isinstance(options, list) and len(options) > 4:
        errors.append("no more than 4 options are supported")
    if any(not str(opt).strip() for opt in options if isinstance(options, list)):
        errors.append("options cannot be empty")
    if not publish_at:
        errors.append("publish_at is required")
    else:
        try:
            datetime.fromisoformat(publish_at)
        except ValueError:
            errors.append("publish_at must be ISO format, e.g. 2026-07-10T09:30:00")
    if not timezone:
        errors.append("timezone is required")
    return errors
