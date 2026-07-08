from datetime import datetime


def validate_poll_dict(item: dict) -> list[str]:
    errors = []
    
    question = item.get("question")
    if question is None:
        errors.append("question is required")
    elif not isinstance(question, str):
        errors.append("question must be a string")
    elif not question.strip():
        errors.append("question cannot be empty")

    options = item.get("options")
    if options is None:
        errors.append("options list is required")
    elif not isinstance(options, list):
        errors.append("options must be a list of strings")
    else:
        if len(options) < 2:
            errors.append("at least 2 options are required")
        if len(options) > 4:
            errors.append("no more than 4 options are supported")
        if any(not isinstance(opt, (str, int, float)) or not str(opt).strip() for opt in options):
            errors.append("options cannot be empty")

    publish_at = item.get("publish_at")
    if not publish_at:
        errors.append("publish_at is required")
    elif isinstance(publish_at, datetime):
        pass  # Already a datetime object
    elif isinstance(publish_at, str):
        try:
            datetime.fromisoformat(publish_at)
        except (ValueError, TypeError):
            errors.append("publish_at must be ISO format, e.g. 2026-07-10T09:30:00")
    else:
        errors.append("publish_at must be a string or datetime object")

    timezone = item.get("timezone")
    if timezone is None:
        errors.append("timezone is required")
    elif not isinstance(timezone, str) or not timezone.strip():
        errors.append("timezone cannot be empty")

    return errors

