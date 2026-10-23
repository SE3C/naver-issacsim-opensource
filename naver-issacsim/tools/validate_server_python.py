"""Parse project-owned Python files from the extracted server backup without importing them."""

from __future__ import annotations

import ast
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKUP_ROOT = PROJECT_ROOT / "data" / "raw" / "server_backup" / "extracted"
SOURCE_ROOTS = [BACKUP_ROOT / name for name in ("training", "practice_sim", "examples")]


def main() -> int:
    files = sorted(file for root in SOURCE_ROOTS for file in root.rglob("*.py"))
    errors: list[tuple[str, str]] = []
    for file in files:
        try:
            ast.parse(file.read_text(encoding="utf-8"), filename=str(file))
        except (OSError, UnicodeError, SyntaxError) as error:
            errors.append((file.relative_to(BACKUP_ROOT).as_posix(), str(error)))

    print({"python_files": len(files), "syntax_errors": len(errors)})
    for filename, error in errors:
        print(f"{filename}: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
