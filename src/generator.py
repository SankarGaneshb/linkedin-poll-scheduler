import argparse
import os
import sys
import json
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime, timedelta
import yaml

# Add current directory to path just in case
sys.path.insert(0, str(Path(__file__).parent))

from validator import validate_poll_dict

def load_topics(topic: str | None, topic_file: str | None) -> list[str]:
    if topic:
        return [topic.strip()]
    if topic_file:
        path = Path(topic_file)
        if not path.exists():
            raise FileNotFoundError(f"Topic file not found: {path}")
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                return [str(item).strip() for item in data if item]
            if isinstance(data, dict):
                if "topics" in data and isinstance(data["topics"], list):
                    return [str(item).strip() for item in data["topics"] if item]
                if "topic" in data:
                    return [str(data["topic"]).strip()]
                # Fallback to dictionary values
                return [str(v).strip() for v in data.values() if isinstance(v, (str, int, float))]
            raise ValueError("JSON file must contain a list or object with 'topics' or 'topic' key")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {e}")
    raise ValueError("Either --topic or --topic-file must be specified")

def generate_polls_for_topic(topic: str, num_polls: int, api_key: str) -> list[dict]:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    start_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    prompt = (
        f"Generate {num_polls} engaging LinkedIn poll post definition(s) about the topic: '{topic}'.\n"
        f"Provide the output strictly matching this JSON schema:\n"
        f"{{\n"
        f"  \"polls\": [\n"
        f"    {{\n"
        f"      \"question\": \"string (clear, engaging, under 140 chars)\",\n"
        f"      \"options\": [\n"
        f"        \"string (option 1, under 30 chars)\",\n"
        f"        \"string (option 2, under 30 chars)\",\n"
        f"        \"string (option 3, under 30 chars, optional)\",\n"
        f"        \"string (option 4, under 30 chars, optional)\"\n"
        f"      ],\n"
        f"      \"publish_at\": \"string (ISO datetime like 'YYYY-MM-DDTHH:MM:SS', starting from tomorrow {start_date} onwards, spaced by at least 1 day)\",\n"
        f"      \"timezone\": \"string (e.g. 'Asia/Kolkata')\",\n"
        f"      \"audience\": \"string ('public' or 'connections')\",\n"
        f"      \"dry_run\": true\n"
        f"    }}\n"
        f"  ]\n"
        f"}}\n"
    )

    payload = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }],
        "generationConfig": {
            "responseMimeType": "application/json"
        }
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as res:
            response_data = json.loads(res.read().decode("utf-8"))
            
        candidate = response_data.get("candidates", [{}])[0]
        text_content = candidate.get("content", {}).get("parts", [{}])[0].get("text", "")
        
        if not text_content:
            raise ValueError("Empty response text from Gemini API")
            
        result = json.loads(text_content.strip())
        if not isinstance(result, dict) or "polls" not in result:
            raise ValueError("Invalid response structure from Gemini API (missing 'polls' key)")
            
        return result["polls"]
    except urllib.error.HTTPError as e:
        error_msg = e.read().decode("utf-8")
        raise RuntimeError(f"Gemini API request failed: HTTP {e.code} - {error_msg}")
    except Exception as e:
        raise RuntimeError(f"Error communicating with Gemini API: {e}")

def save_polls_to_yaml(polls: list[dict], output_path: Path) -> None:
    existing_data = {}
    if output_path.exists():
        try:
            existing_data = yaml.safe_load(output_path.read_text()) or {}
        except Exception as e:
            print(f"Warning: Failed to read existing output file ({e}). Overwriting.")
            existing_data = {}
            
    existing_polls = existing_data.get("polls", [])
    if not isinstance(existing_polls, list):
        existing_polls = []
        
    existing_polls.extend(polls)
    
    # Save back
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(yaml.safe_dump({"polls": existing_polls}, sort_keys=False), encoding="utf-8")

def main() -> int:
    parser = argparse.ArgumentParser(description="Generate LinkedIn poll schedules using Gemini API.")
    parser.add_argument("--topic", help="Topic to generate poll about.")
    parser.add_argument("--topic-file", help="Path to JSON file containing list of topics.")
    parser.add_argument("--api-key", help="Gemini API Key (optional, defaults to GEMINI_API_KEY environment variable).")
    parser.add_argument("--output", default="config/my-next-week-polls.yaml", help="Path to save generated polls (YAML).")
    parser.add_argument("--num-polls", type=int, default=1, help="Number of polls to generate per topic.")
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: Gemini API key must be provided via --api-key or GEMINI_API_KEY environment variable.", file=sys.stderr)
        return 1

    try:
        topics = load_topics(args.topic, args.topic_file)
    except Exception as e:
        print(f"Error loading topics: {e}", file=sys.stderr)
        return 1

    all_generated_polls = []
    for topic in topics:
        print(f"Generating {args.num_polls} poll(s) for topic: '{topic}'...")
        try:
            raw_polls = generate_polls_for_topic(topic, args.num_polls, api_key)
            validated = []
            for idx, p in enumerate(raw_polls, start=1):
                errors = validate_poll_dict(p)
                if errors:
                    print(f"  Warning: Generated poll #{idx} is invalid: {'; '.join(errors)}. Skipping.")
                else:
                    validated.append(p)
            print(f"  Successfully generated {len(validated)} valid poll(s).")
            all_generated_polls.extend(validated)
        except Exception as e:
            print(f"  Error generating polls for topic '{topic}': {e}", file=sys.stderr)

    if not all_generated_polls:
        print("No valid polls were generated. Exiting.", file=sys.stderr)
        return 1

    try:
        save_polls_to_yaml(all_generated_polls, Path(args.output))
        print(f"Successfully saved {len(all_generated_polls)} polls to {args.output}")
        return 0
    except Exception as e:
        print(f"Error saving polls to YAML: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
