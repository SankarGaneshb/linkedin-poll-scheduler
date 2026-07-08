import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add src/ to sys.path to allow imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from generator import load_topics, generate_polls_for_topic

class TestGenerator(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_dir_path = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_load_topics_from_string(self):
        topics = load_topics("AI Governance", None)
        self.assertEqual(topics, ["AI Governance"])

    def test_load_topics_from_json_list(self):
        content = '["AI Governance", "MLOps"]'
        f = self.temp_dir_path / "topics_list.json"
        f.write_text(content)
        
        topics = load_topics(None, str(f))
        self.assertEqual(topics, ["AI Governance", "MLOps"])

    def test_load_topics_from_json_object_topics(self):
        content = '{"topics": ["AI Governance", "Ethics"]}'
        f = self.temp_dir_path / "topics_obj.json"
        f.write_text(content)
        
        topics = load_topics(None, str(f))
        self.assertEqual(topics, ["AI Governance", "Ethics"])

    def test_load_topics_from_json_object_single(self):
        content = '{"topic": "Compliance"}'
        f = self.temp_dir_path / "topics_single.json"
        f.write_text(content)
        
        topics = load_topics(None, str(f))
        self.assertEqual(topics, ["Compliance"])

    def test_load_topics_from_json_fallback_values(self):
        content = '{"a": "A", "b": "B"}'
        f = self.temp_dir_path / "topics_fallback.json"
        f.write_text(content)
        
        topics = load_topics(None, str(f))
        self.assertEqual(topics, ["A", "B"])

    def test_load_topics_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            load_topics(None, "non_existent_file.json")

    def test_load_topics_invalid_json(self):
        f = self.temp_dir_path / "invalid.json"
        f.write_text("invalid json content")
        
        with self.assertRaises(ValueError):
            load_topics(None, str(f))

    @patch("urllib.request.urlopen")
    def test_generate_polls_for_topic_success(self, mock_urlopen):
        # Mock Gemini API response
        mock_response = MagicMock()
        gemini_response = {
            "candidates": [{
                "content": {
                    "parts": [{
                        "text": json.dumps({
                            "polls": [
                                {
                                    "question": "What is AI Governance?",
                                    "options": ["A framework", "A law", "Both"],
                                    "publish_at": "2026-07-12T09:30:00",
                                    "timezone": "Asia/Kolkata",
                                    "audience": "public",
                                    "dry_run": True
                                }
                            ]
                        })
                    }]
                }
            }]
        }
        mock_response.read.return_value = json.dumps(gemini_response).encode("utf-8")
        mock_urlopen.return_value.__enter__.return_value = mock_response

        polls = generate_polls_for_topic("AI Governance", 1, "test_api_key")
        
        self.assertEqual(len(polls), 1)
        self.assertEqual(polls[0]["question"], "What is AI Governance?")
        self.assertEqual(polls[0]["options"], ["A framework", "A law", "Both"])

if __name__ == "__main__":
    unittest.main()
