from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlparse
from urllib.request import urlopen

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    NoTranscriptFound,
    TranscriptsDisabled,
    VideoUnavailable,
)


ROOT = Path(__file__).resolve().parents[2]
RAW_VIDEOS_DIR = ROOT / "raw" / "videos"
WIKI_DIR = ROOT / "wiki"


def extract_video_id(url: str) -> str:
    parsed = urlparse(url)

    if parsed.hostname in {"www.youtube.com", "youtube.com", "m.youtube.com"}:
        if parsed.path == "/watch":
            video_id = parse_qs(parsed.query).get("v", [""])[0]
            if video_id:
                return video_id
        parts = [part for part in parsed.path.split("/") if part]
        if parts and parts[0] in {"shorts", "live", "embed"} and len(parts) >= 2:
            return parts[1]

    if parsed.hostname == "youtu.be":
        parts = [part for part in parsed.path.split("/") if part]
        if parts:
            return parts[0]

    raise ValueError(f"Không nhận diện được YouTube video id từ URL: {url}")


def fetch_video_title(url: str) -> str:
    oembed_url = f"https://www.youtube.com/oembed?url={url}&format=json"
    try:
        with urlopen(oembed_url, timeout=20) as response:
            data = json.loads(response.read().decode("utf-8"))
            title = data.get("title")
            if title:
                return title
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError):
        pass
    return "YouTube Video"


def fetch_transcript(video_id: str) -> list[dict[str, str]]:
    try:
        ytt_api = YouTubeTranscriptApi()
        transcript_list = ytt_api.fetch(video_id)
        return [{"start": item.start, "text": item.text} for item in transcript_list]
    except (TranscriptsDisabled, NoTranscriptFound):
        raise RuntimeError(
            "Video không có transcript khả dụng từ youtube-transcript-api."
        )
    except VideoUnavailable as exc:
        raise RuntimeError(f"Video không khả dụng: {exc}") from exc


def slugify_title(title: str) -> str:
    slug = title.lower()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"[\s-]+", "-", slug).strip("-")
    return slug or "youtube-video"


def write_markdown(url: str, title: str, transcript: list[dict[str, str]]) -> Path:
    RAW_VIDEOS_DIR.mkdir(parents=True, exist_ok=True)

    discovered = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    topic = "AI Agents"
    filename = f"{discovered}-{slugify_title(title)}.md"
    target = RAW_VIDEOS_DIR / filename

    transcript_text = "\n\n".join(
        f"[{item['start']:.2f}s] {item['text'].strip()}" for item in transcript
    )

    content = f'''---
title: "{title.replace('"', '\\"')}"
url: "{url}"
discovered: "{discovered}"
topic: "{topic}"
source_type: "youtube"
---

# {title}

## Transcript

{transcript_text}
'''
    target.write_text(content, encoding="utf-8")
    return target


def run_ingest(markdown_file: Path) -> None:
    print(f"Chay lenh sau trong Cursor de ingest: /llm-wiki ingest {markdown_file.name}")

def main() -> int:
    if len(sys.argv) != 2:
        print("Cách dùng: python ingest_video.py [YouTube URL]", file=sys.stderr)
        return 1

    url = sys.argv[1].strip()
    try:
        video_id = extract_video_id(url)
        title = fetch_video_title(url)
        transcript = fetch_transcript(video_id)
    except Exception as exc:
        print(f"Lỗi: {exc}", file=sys.stderr)
        return 1

    markdown_file = write_markdown(url, title, transcript)
    print(f"Da tao: {markdown_file}")
    run_ingest(markdown_file)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
