import tempfile
import os
from envcheck import validate_env

def test_valid_env():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
        f.write("DB_HOST=localhost\nDB_PORT=5432\n")
        f.flush()
        issues = validate_env(f.name)
    os.unlink(f.name)
    assert issues == []

def test_duplicate_key():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
        f.write("KEY=val1\nKEY=val2\n")
        f.flush()
        issues = validate_env(f.name)
    os.unlink(f.name)
    assert any("Duplicate" in i for i in issues)

def test_missing_equals():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
        f.write("BROKEN_LINE\n")
        f.flush()
        issues = validate_env(f.name)
    os.unlink(f.name)
    assert any("Missing" in i for i in issues)
