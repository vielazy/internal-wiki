param(
    [string]$RepoRoot = (Split-Path -Parent $PSScriptRoot),
    [string]$Tool = "Cursor"
)

$ErrorActionPreference = "Stop"
Set-Location $RepoRoot

switch ($Tool.ToLowerInvariant()) {
    "cursor" {
        Write-Host "Chạy full cycle trong Cursor: discover → ingest → lint"
        Write-Host "Mở Cursor và chạy: /llm-wiki run"
    }
    "claude" {
        Write-Host "Chạy full cycle trong Claude Code: discover → ingest → lint"
        Write-Host "Chạy: /llm-wiki run"
    }
    default {
        Write-Host "Chạy full cycle: discover → ingest → lint"
        Write-Host "Chạy: /llm-wiki run"
    }
}

if ($env:DATABASE_URL -or (Test-Path (Join-Path $RepoRoot ".env"))) {
    Write-Host "Nếu đang bật PostgreSQL, sync metadata sau ingest:"
    Write-Host "python scripts/sync_wiki_to_db.py"
}
