import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

# Add src/ to sys.path to allow imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from scheduler import load_jobs
from models import PollJob

class TestScheduler(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_dir_path = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_load_jobs_valid(self):
        content = """
polls:
  - question: "Question 1"
    options:
      - "Option A"
      - "Option B"
    publish_at: "2026-07-12T09:30:00"
    timezone: "Asia/Kolkata"
    audience: "public"
    dry_run: false
  - question: "Question 2"
    options:
      - "Option C"
      - "Option D"
    publish_at: 2026-07-15T18:00:00
    timezone: "Asia/Kolkata"
"""
        config_file = self.temp_dir_path / "valid_polls.yaml"
        config_file.write_text(content)

        jobs = load_jobs(config_file)
        self.assertEqual(len(jobs), 2)
        
        # Verify first job
        self.assertEqual(jobs[0].question, "Question 1")
        self.assertEqual(jobs[0].options, ["Option A", "Option B"])
        self.assertEqual(jobs[0].publish_at, datetime(2026, 7, 12, 9, 30, 0))
        self.assertEqual(jobs[0].timezone, "Asia/Kolkata")
        self.assertEqual(jobs[0].audience, "public")
        self.assertFalse(jobs[0].dry_run)

        # Verify second job
        self.assertEqual(jobs[1].question, "Question 2")
        self.assertEqual(jobs[1].options, ["Option C", "Option D"])
        self.assertEqual(jobs[1].publish_at, datetime(2026, 7, 15, 18, 0, 0))
        self.assertEqual(jobs[1].timezone, "Asia/Kolkata")
        self.assertEqual(jobs[1].audience, "public")  # Default value
        self.assertTrue(jobs[1].dry_run)  # Default value

    def test_load_jobs_invalid(self):
        content = """
polls:
  - question: "Invalid Poll"
    options:
      - "Only One Option"
    publish_at: "2026-07-12T09:30:00"
    timezone: "Asia/Kolkata"
"""
        config_file = self.temp_dir_path / "invalid_polls.yaml"
        config_file.write_text(content)

        with self.assertRaises(ValueError) as ctx:
            load_jobs(config_file)
        self.assertIn("is invalid", str(ctx.exception))

if __name__ == "__main__":
    unittest.main()
