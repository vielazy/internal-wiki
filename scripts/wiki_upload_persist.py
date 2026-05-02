from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from wiki_runtime import open_db_connection, set_search_path


def persist_upload_artifact(settings, *, uploaded_by: str, filename: str, title: str, topic: str, content_text: str, content_hash: str, duplicate_json: dict[str, Any], storage_path: str, status: str = 'received') -> int:
    with open_db_connection(settings) as connection:
        set_search_path(connection, settings)
        with connection.transaction():
            row = connection.execute(
                """
                INSERT INTO upload_artifacts (uploaded_by, filename, title, topic, content_text, content_hash, duplicate_json, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                (uploaded_by, filename, title, topic, content_text, content_hash, json.dumps(duplicate_json, ensure_ascii=False), status),
            ).fetchone()
            return int(row['id']) if row else -1
