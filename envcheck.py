#!/usr/bin/env python3
"""envcheck - Validate .env files for common issues."""
import re
import sys
from pathlib import Path

def validate_env(filepath: str) -> list[str]:
    """Validate a .env file and return list of issues found."""
    issues = []
    path = Path(filepath)
    if not path.exists():
        return [f"File not found: {filepath}"]

    seen_keys = set()
    for lineno, line in enumerate(path.read_text().splitlines(), 1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if "=" not in stripped:
            issues.append(f"Line {lineno}: Missing = sign: {stripped[:40]}")
            continue
        key, _, value = stripped.partition("=")
        key = key.strip()
        if not re.match(r"^[A-Z_][A-Z0-9_]*$", key, re.IGNORECASE):
            issues.append(f"Line {lineno}: Invalid key name: {key}")
        if key in seen_keys:
            issues.append(f"Line {lineno}: Duplicate key: {key}")
        seen_keys.add(key)
        if value and not value.startswith("\"") and " " in value:
            issues.append(f"Line {lineno}: Unquoted value with spaces: {key}")
    return issues

def main():
    files = sys.argv[1:] or [".env"]
    exit_code = 0
    for f in files:
        issues = validate_env(f)
        if issues:
            print(f"\\n{f}: {len(issues)} issue(s)")
            for issue in issues:
                print(f"  - {issue}")
            exit_code = 1
        else:
            print(f"{f}: OK")
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
