import sys
import unittest
from datetime import datetime
from pathlib import Path

# Add src/ to sys.path to allow imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from validator import validate_poll_dict

class TestValidator(unittest.TestCase):
    def test_valid_poll(self):
        item = {
            "question": "Which framework do you prefer?",
            "options": ["React", "Vue", "Angular"],
            "publish_at": "2026-07-12T09:30:00",
            "timezone": "Asia/Kolkata",
            "audience": "public"
        }
        errors = validate_poll_dict(item)
        self.assertEqual(errors, [])

    def test_valid_poll_with_datetime_object(self):
        item = {
            "question": "Which framework do you prefer?",
            "options": ["React", "Vue", "Angular"],
            "publish_at": datetime(2026, 7, 12, 9, 30, 0),
            "timezone": "Asia/Kolkata"
        }
        errors = validate_poll_dict(item)
        self.assertEqual(errors, [])

    def test_missing_question(self):
        item = {
            "options": ["A", "B"],
            "publish_at": "2026-07-12T09:30:00",
            "timezone": "Asia/Kolkata"
        }
        errors = validate_poll_dict(item)
        self.assertIn("question is required", errors)

    def test_null_question(self):
        item = {
            "question": None,
            "options": ["A", "B"],
            "publish_at": "2026-07-12T09:30:00",
            "timezone": "Asia/Kolkata"
        }
        errors = validate_poll_dict(item)
        self.assertIn("question is required", errors)

    def test_empty_question(self):
        item = {
            "question": "   ",
            "options": ["A", "B"],
            "publish_at": "2026-07-12T09:30:00",
            "timezone": "Asia/Kolkata"
        }
        errors = validate_poll_dict(item)
        self.assertIn("question cannot be empty", errors)

    def test_invalid_options_count(self):
        # 1 option
        item1 = {
            "question": "Q",
            "options": ["A"],
            "publish_at": "2026-07-12T09:30:00",
            "timezone": "Asia/Kolkata"
        }
        errors1 = validate_poll_dict(item1)
        self.assertIn("at least 2 options are required", errors1)

        # 5 options
        item2 = {
            "question": "Q",
            "options": ["A", "B", "C", "D", "E"],
            "publish_at": "2026-07-12T09:30:00",
            "timezone": "Asia/Kolkata"
        }
        errors2 = validate_poll_dict(item2)
        self.assertIn("no more than 4 options are supported", errors2)

    def test_empty_options(self):
        item = {
            "question": "Q",
            "options": ["A", "  ", "B"],
            "publish_at": "2026-07-12T09:30:00",
            "timezone": "Asia/Kolkata"
        }
        errors = validate_poll_dict(item)
        self.assertIn("options cannot be empty", errors)

    def test_invalid_publish_at_format(self):
        item = {
            "question": "Q",
            "options": ["A", "B"],
            "publish_at": "2026/07/12 09:30:00",
            "timezone": "Asia/Kolkata"
        }
        errors = validate_poll_dict(item)
        self.assertIn("publish_at must be ISO format, e.g. 2026-07-10T09:30:00", errors)

    def test_missing_timezone(self):
        item = {
            "question": "Q",
            "options": ["A", "B"],
            "publish_at": "2026-07-12T09:30:00"
        }
        errors = validate_poll_dict(item)
        self.assertIn("timezone is required", errors)

if __name__ == "__main__":
    unittest.main()
