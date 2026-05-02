from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[2]
RAW_REPOS_DIR = ROOT / "raw" / "repos"


COMMON_FILE_NAMES = [
    "README.md",
    "README.mdx",
    "AGENTS.md",
    "CLAUDE.md",
    "CONTRIBUTING.md",
    "docs",
    "src",
    "app",
    "packages",
]

CODE_EXTENSIONS = {
    ".py",
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
    ".java",
    ".go",
    ".rb",
    ".rs",
    ".php",
    ".cs",
    ".cpp",
    ".c",
    ".h",
    ".hpp",
    ".kt",
    ".swift",
}

TEXT_EXTENSIONS = {".md", ".mdx", ".txt", ".rst", ".yml", ".yaml", ".json", ".toml"}

MAX_FILE_BYTES = 250_000
MAX_SNIPPETS = 8
MAX_DECISIONS = 8
MAX_PATTERNS = 10


@dataclass
class ExtractedContent:
    patterns: list[str]
    decisions: list[str]
    examples: list[str]
    files_scanned: list[str]


def normalize_repo_url(url: str) -> str:
    url = url.strip().rstrip("/")
    if url.endswith(".git"):
        url = url[:-4]
    parsed = urlparse(url)
    if parsed.netloc.lower() != "github.com":
        raise ValueError("Chỉ hỗ trợ GitHub repo URL.")
    parts = [p for p in parsed.path.split("/") if p]
    if len(parts) < 2:
        raise ValueError("URL repo GitHub không hợp lệ.")
    return f"https://github.com/{parts[0]}/{parts[1]}"


def repo_slug(repo_url: str) -> str:
    parts = repo_url.rstrip("/").split("/")
    return f"{parts[-2]}-{parts[-1]}"


def clone_repo(repo_url: str, target_dir: Path) -> None:
    cmd = ["git", "clone", "--depth", "1", repo_url, str(target_dir)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "Không thể clone repository.")


def is_binary(path: Path) -> bool:
    try:
        sample = path.read_bytes()[:1024]
    except OSError:
        return True
    return b"\x00" in sample


def walk_candidate_files(repo_dir: Path) -> list[Path]:
    files: list[Path] = []
    for root, dirs, filenames in os.walk(repo_dir):
        dirs[:] = [d for d in dirs if d not in {".git", "node_modules", "dist", "build", "target", "vendor"}]
        for filename in filenames:
            path = Path(root) / filename
            if path.suffix.lower() in CODE_EXTENSIONS | TEXT_EXTENSIONS or filename in COMMON_FILE_NAMES:
                files.append(path)
    return files


def scan_repo(repo_dir: Path) -> ExtractedContent:
    patterns: list[str] = []
    decisions: list[str] = []
    examples: list[str] = []
    scanned: list[str] = []

    for path in walk_candidate_files(repo_dir):
        if len(scanned) >= 40:
            break
        if path.is_dir() or is_binary(path):
            continue
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if len(content) > MAX_FILE_BYTES:
            continue

        rel = str(path.relative_to(repo_dir)).replace("\\", "/")
        scanned.append(rel)

        lower = content.lower()

        if "architecture" in lower or "design" in lower or "trade-off" in lower:
            for line in content.splitlines():
                if re.search(r"(architecture|decision|trade[- ]off|why we use|we chose)", line, re.I):
                    decisions.append(f"{rel}: {line.strip()}")
                    break

        if any(token in lower for token in ["pattern", "workflow", "approach", "strategy"]):
            for line in content.splitlines():
                if re.search(r"(pattern|workflow|approach|strategy)", line, re.I):
                    patterns.append(f"{rel}: {line.strip()}")
                    break

        if path.suffix.lower() in CODE_EXTENSIONS:
            lines = content.splitlines()
            for i, line in enumerate(lines):
                if line.strip().startswith(("def ", "class ", "function ", "export function", "export const", "public class", "type ")):
                    snippet = "\n".join(lines[max(0, i - 2): min(len(lines), i + 8)])
                    examples.append(f"[{rel}]\n```\n{snippet}\n```")
                    break
        else:
            if "```" in content:
                fence_blocks = re.findall(r"```[\s\S]*?```", content)
                if fence_blocks:
                    examples.append(f"[{rel}]\n{fence_blocks[0]}")

    patterns = dedupe_limit(patterns, MAX_PATTERNS)
    decisions = dedupe_limit(decisions, MAX_DECISIONS)
    examples = dedupe_limit(examples, MAX_SNIPPETS)
    return ExtractedContent(patterns, decisions, examples, scanned)


def dedupe_limit(items: list[str], limit: int) -> list[str]:
    seen = set()
    result: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        result.append(item)
        if len(result) >= limit:
            break
    return result


def write_markdown(repo_url: str, extracted: ExtractedContent) -> Path:
    RAW_REPOS_DIR.mkdir(parents=True, exist_ok=True)
    discovered = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    slug = repo_slug(repo_url)
    target = RAW_REPOS_DIR / f"{discovered}-{slug}.md"

    title = f"GitHub Repo: {slug}"
    content = f'''---
title: "{title}"
url: "{repo_url}"
discovered: "{discovered}"
topic: "AI Coding Workflows"
source_type: "github-repo"
---

# {title}

## Repository Overview

- URL: {repo_url}
- Files scanned: {len(extracted.files_scanned)}

## Architecture Decisions

{format_bullets(extracted.decisions, "Chưa trích xuất được architecture decision rõ ràng.")}

## Patterns

{format_bullets(extracted.patterns, "Chưa trích xuất được pattern rõ ràng.")}

## Code Examples

{format_examples(extracted.examples, "Chưa trích xuất được code example rõ ràng.")}

## Files Scanned

{format_bullets(extracted.files_scanned, "Không có file phù hợp.")}
'''
    target.write_text(content, encoding="utf-8")
    return target


def format_bullets(items: list[str], fallback: str) -> str:
    if not items:
        return f"- {fallback}"
    return "\n".join(f"- {item}" for item in items)


def format_examples(items: list[str], fallback: str) -> str:
    if not items:
        return f"- {fallback}"
    return "\n\n".join(f"- {item}" for item in items)


def ingest_repo(repo_url: str) -> Path:
    normalized = normalize_repo_url(repo_url)
    with tempfile.TemporaryDirectory(prefix="llm-wiki-repo-") as tmp:
        clone_target = Path(tmp) / "repo"
        clone_repo(normalized, clone_target)
        extracted = scan_repo(clone_target)
        return write_markdown(normalized, extracted)


def main() -> int:
    if len(sys.argv) != 2:
        print("Cách dùng: python ingest_repo.py [GitHub Repo URL]", file=sys.stderr)
        return 1

    repo_url = sys.argv[1].strip()
    try:
        markdown_file = ingest_repo(repo_url)
    except Exception as exc:
        print(f"Lỗi: {exc}", file=sys.stderr)
        return 1

    print(f"Đã tạo: {markdown_file}")
    print(f"Chạy lệnh sau trong Cursor để ingest: /llm-wiki ingest {markdown_file.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
