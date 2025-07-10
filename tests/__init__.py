# Distill CLI tests
from distill import compress
from distill.core import compress_git_diff, compress_npm_test, compress_terraform, compress_generic
from distill.core import compress_pytest


def test_compress_empty():
    """Test compress with empty input."""
    result = compress("", "generic")
    assert result == ""


def test_compress_generic():
    """Test generic compression."""
    output = "\n".join([f"line {i}" for i in range(30)])
    result = compress(output, "generic", max_lines=10)
    assert "Output has 30 lines" in result
    assert "First 10 lines" in result


def test_compress_git_diff():
    """Test git diff compression."""
    output = """diff --git a/foo.py b/foo.py
--- a/foo.py
+++ b/foo.py
@@ -1,1 +1,1 @@
-old
+new
"""
    result = compress(output, "git-diff")
    assert "files_changed" in result
    assert "1" in result


def test_compress_npm_test():
    """Test npm test compression."""
    output = "Tests: 10 passed, 2 failed"
    result = compress(output, "npm-test")
    assert "passed" in result


def test_compress_terraform():
    """Test terraform compression."""
    output = "plan: +1, ~2, -3"
    result = compress(output, "terraform")
    assert "add" in result


def test_compress_pytest():
    """Test pytest compression."""
    output = "10 passed, 2 failed"
    result = compress(output, "pytest")
    assert "passed" in result


def test_compress_with_prompt():
    """Test compression with prompt."""
    output = "line1\nline2\nline3"
    result = compress(output, "generic", prompt="get summary", max_lines=2)
    assert "Prompt" in result