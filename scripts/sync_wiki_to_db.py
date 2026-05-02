from __future__ import annotations

import argparse
import json
import sys

from wiki_runtime import apply_schema, load_admin_database_settings, load_database_settings, sync_database


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sync markdown wiki data into PostgreSQL while keeping wiki/ as source of truth."
    )
    parser.add_argument(
        "--init",
        action="store_true",
        help="Apply scripts/db_init.sql before syncing.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print sync summary as JSON.",
    )
    args = parser.parse_args()

    runtime_settings = load_database_settings()
    if not runtime_settings:
        print(
            "Chưa có cấu hình PostgreSQL runtime. Tạo .env từ .env.example hoặc set DATABASE_URL / POSTGRES_* trước.",
            file=sys.stderr,
        )
        return 1

    try:
        if args.init:
            admin_settings = load_admin_database_settings()
            if admin_settings:
                try:
                    apply_schema(admin_settings)
                except Exception as exc:
                    print(
                        f"Cảnh báo: bỏ qua --init vì không thể kết nối admin DB ({exc}). "
                        f"Nếu bạn đã chạy SQL init thủ công trên Supabase thì có thể tiếp tục sync runtime.",
                        file=sys.stderr,
                    )
            else:
                print(
                    "Cảnh báo: không tìm thấy ADMIN_DATABASE_URL, bỏ qua bước init và tiếp tục sync runtime.",
                    file=sys.stderr,
                )
        summary = sync_database(runtime_settings)
    except Exception as exc:
        print(f"Lỗi sync PostgreSQL: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(f"Đã sync wiki -> PostgreSQL schema `{runtime_settings.schema}`")
        for key, value in summary.items():
            print(f"- {key}: {value}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
