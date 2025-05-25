# Distill CLI tests
from distill import compress


def test_compress_generic():
    """Test generic compression."""
    output = "line1\nline2\nline3\nline4\nline5\nline6\nline7\nline8\nline9\nline10\nline11\nline12\nline13\nline14\nline15\nline16\nline17\nline18\nline19\nline20\nline21\nline22"
    result = compress(output, "generic")
    assert "22 lines" in result


def test_compress_git_diff():
    """Test git diff compression."""
    output = "diff --git a/file.txt b/file.txt\n@@ -1,3 +1,4 @@\n+new line"
    result = compress(output, "git-diff")
    assert "Files changed" in result or "Hunks" in result


def test_version():
    """Test version is set."""
    from distill import __version__
    assert __version__ == "0.1.0"