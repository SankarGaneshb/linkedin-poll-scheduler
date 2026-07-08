from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class PollJob:
    question: str
    options: List[str]
    publish_at: datetime
    timezone: str
    audience: str = "public"
    dry_run: bool = True
