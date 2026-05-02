from __future__ import annotations

import base64
import json
import os
from dataclasses import dataclass
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class StorageResult:
    storage_path: str
    public_url: str | None = None
    signed_url: str | None = None


def supabase_storage_config() -> tuple[str | None, str | None, str | None]:
    url = os.getenv('SUPABASE_URL', '').strip() or os.getenv('SUPABASE_PROJECT_URL', '').strip()
    key = os.getenv('SUPABASE_SERVICE_ROLE_KEY', '').strip() or os.getenv('SUPABASE_ANON_KEY', '').strip()
    bucket = os.getenv('SUPABASE_UPLOAD_BUCKET', 'wiki-uploads').strip() or 'wiki-uploads'
    return url or None, key or None, bucket


def upload_to_supabase_storage(*, filename: str, data: bytes, content_type: str = 'application/octet-stream') -> StorageResult | None:
    supabase_url, api_key, bucket = supabase_storage_config()
    if not supabase_url or not api_key:
        return None
    object_path = f"uploads/{filename}"
    endpoint = f"{supabase_url.rstrip('/')}/storage/v1/object/{bucket}/{quote(object_path)}"
    req = Request(endpoint, data=data, method='POST')
    req.add_header('Authorization', f'Bearer {api_key}')
    req.add_header('apikey', api_key)
    req.add_header('Content-Type', content_type)
    req.add_header('x-upsert', 'true')
    try:
        with urlopen(req, timeout=30) as resp:
            if resp.status not in (200, 201):
                return None
    except HTTPError:
        return None
    public_url = f"{supabase_url.rstrip('/')}/storage/v1/object/public/{bucket}/{quote(object_path)}"
    signed_url = None
    return StorageResult(storage_path=f"{bucket}/{object_path}", public_url=public_url, signed_url=signed_url)
