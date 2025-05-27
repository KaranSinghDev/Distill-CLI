"""
Core compression logic for Distill CLI
"""
import re
from typing import Optional


def compress_git_diff(output: str, prompt: str = "") -> dict:
    """Compress git diff output for LLM returning structured data."""
    if not output.strip():
        return {"files_changed": 0, "hunks": 0, "changes": []}

    lines = output.strip().split("\n")
    files_changed = set()
    hunks = []

    for line in lines:
        if line.startswith("diff --git"):
            match = re.search(r'b/(.+)', line)
            if match:
                files_changed.add(match.group(1))
        elif line.startswith("@@"):
            hunks.append(line)

    return {
        "files_changed": len(files_changed),
        "hunks": len(hunks),
        "changes": hunks[:5],
        "prompt": prompt
    }


def compress_npm_test(output: str, prompt: str = "") -> dict:
    """Compress npm test output."""
    lines = output.strip().split("\n")

    passed = failed = skipped = 0
    summary_line = ""

    for line in lines:
        if "pass" in line.lower() and "%" in line:
            summary_line = line.strip()
        if re.search(r'\d+\s+pass', line, re.I):
            passed = re.search(r'(\d+)', line).group(1) if re.search(r'(\d+)', line) else 0
        if re.search(r'\d+\s+fail', line, re.I):
            failed = re.search(r'(\d+)', line).group(1) if re.search(r'(\d+)', line) else 0

    return {
        "passed": passed,
        "failed": failed,
        "summary": summary_line,
        "prompt": prompt
    }


def compress_terraform(output: str, prompt: str = "") -> dict:
    """Compress terraform plan output."""
    lines = output.strip().split("\n")

    changes = {"add": 0, "change": 0, "destroy": 0}

    for line in lines:
        if "+" in line and not line.startswith("+") and not line.startswith("diff"):
            changes["add"] += 1
        if "~" in line and not line.startswith("~"):
            changes["change"] += 1
        if "-" in line and not line.startswith("-") and not line.startswith("diff"):
            changes["destroy"] += 1

    return {"plan": changes, "prompt": prompt}


def compress(output: str, output_type: str = "summary", prompt: str = "") -> str:
    """General compression function."""
    if output_type == "git-diff":
        return str(compress_git_diff(output, prompt))
    elif output_type == "npm-test":
        return str(compress_npm_test(output, prompt))
    elif output_type == "terraform":
        return str(compress_terraform(output, prompt))
    else:
        return compress_generic(output, prompt)


def compress_generic(output: str, prompt: str = "", max_lines: int = 20) -> str:
    """Generic compression - extract key information."""
    lines = output.strip().split("\n")

    if len(lines) <= max_lines:
        return output

    result = f"Output has {len(lines)} lines\n"
    result += f"First {max_lines} lines:\n"
    result += "\n".join(lines[:max_lines])

    return result