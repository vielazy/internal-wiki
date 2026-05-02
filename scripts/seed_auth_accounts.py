from __future__ import annotations

import argparse
from getpass import getpass

import bcrypt

from wiki_runtime import apply_schema, load_admin_database_settings, open_db_connection, set_search_path


DEFAULT_ACCOUNTS = [
    {
        "role": "editor",
        "username": "editor",
        "display_name": "Internal Editor",
        "password": "editor123",
    },
    {
        "role": "admin",
        "username": "admin",
        "display_name": "Site Admin",
        "password": "admin123",
    },
]


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def upsert_account(connection, role: str, username: str, display_name: str, password_hash: str) -> None:
    connection.execute(
        """
        INSERT INTO auth_accounts (role, username, display_name, password_hash, active)
        VALUES (%s, %s, %s, %s, 1)
        ON CONFLICT (role) DO UPDATE SET
            username = EXCLUDED.username,
            display_name = EXCLUDED.display_name,
            password_hash = EXCLUDED.password_hash,
            updated_at = CURRENT_TIMESTAMP::text,
            active = 1
        """,
        (role, username, display_name, password_hash),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Seed auth accounts into Supabase.")
    parser.add_argument("--init", action="store_true", help="Apply schema before seeding accounts.")
    parser.add_argument("--admin-password", default="", help="Optional admin password override.")
    parser.add_argument("--editor-password", default="", help="Optional editor password override.")
    args = parser.parse_args()

    settings = load_admin_database_settings()
    if not settings:
        print("ADMIN_DATABASE_URL chưa được cấu hình.")
        return 1

    if args.init:
        apply_schema(settings)

    editor_password = args.editor_password or getpass("Editor password [default editor123]: ") or "editor123"
    admin_password = args.admin_password or getpass("Admin password [default admin123]: ") or "admin123"

    accounts = [
        {**DEFAULT_ACCOUNTS[0], "password": editor_password},
        {**DEFAULT_ACCOUNTS[1], "password": admin_password},
    ]

    with open_db_connection(settings) as connection:
        set_search_path(connection, settings)
        with connection.transaction():
            for account in accounts:
                upsert_account(
                    connection,
                    account["role"],
                    account["username"],
                    account["display_name"],
                    hash_password(account["password"]),
                )

    print("Đã seed auth_accounts thành công.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
