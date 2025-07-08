"""
Core compression logic for Distill CLI
"""
import re
from typing import Optional, Dict, List

__all__ = [
    "compress",
    "compress_git_diff", 
    "compress_npm_test",
    "compress_terraform",
    "compress_pytest",
    "compress_generic"
]


def compress_git_diff(output: str, prompt: str = "") -> Dict[str, any]:
    """Compress git diff output for LLM returning structured data."""
    if not output or not output.strip():
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


def compress_npm_test(output: str, prompt: str = "") -> Dict[str, any]:
    """Compress npm test output."""
    if not output or not output.strip():
        return {"passed": 0, "failed": 0, "skipped": 0, "summary": "", "prompt": prompt}
    
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


def compress_terraform(output: str, prompt: str = "") -> Dict[str, any]:
    """Compress terraform plan output."""
    if not output or not output.strip():
        return {"plan": {"add": 0, "change": 0, "destroy": 0}, "prompt": prompt}
    
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


def compress_pytest(output: str, prompt: str = "") -> Dict[str, any]:
    """Compress pytest output."""
    if not output or not output.strip():
        return {"passed": 0, "failed": 0, "errors": 0, "skipped": 0, "prompt": prompt}
    
    lines = output.strip().split("\n")
    
    passed = failed = errors = skipped = 0
    failed_tests = []
    error_tests = []
    
    for line in lines:
        match = re.search(r'(\d+)\s+passed', line, re.I)
        if match:
            passed = int(match.group(1))
        match = re.search(r'(\d+)\s+failed', line, re.I)
        if match:
            failed = int(match.group(1))
        match = re.search(r'(\d+)\s+error', line, re.I)
        if match:
            errors = int(match.group(1))
        match = re.search(r'(\d+)\s+skipped', line, re.I)
        if match:
            skipped = int(match.group(1))
        if "FAILED" in line:
            failed_tests.append(line[:80])
        if "ERROR" in line:
            error_tests.append(line[:80])
    
    return {
        "passed": passed,
        "failed": failed,
        "errors": errors,
        "skipped": skipped,
        "failed_tests": failed_tests[:5],
        "error_tests": error_tests[:5],
        "prompt": prompt
    }


def compress(output: str, output_type: str = "summary", prompt: str = "", max_lines: int = 20) -> str:
    """General compression function."""
    if not output:
        return ""
    
    if output_type == "git-diff":
        return str(compress_git_diff(output, prompt))
    elif output_type == "npm-test":
        return str(compress_npm_test(output, prompt))
    elif output_type == "terraform":
        return str(compress_terraform(output, prompt))
    elif output_type == "pytest":
        return str(compress_pytest(output, prompt))
    else:
        return compress_generic(output, prompt, max_lines)


def compress_generic(output: str, prompt: str = "", max_lines: int = 20) -> str:
    """Generic compression - extract key information."""
    if not output:
        return ""
    
    lines = output.strip().split("\n")

    if len(lines) <= max_lines:
        return output

    result = f"Output has {len(lines)} lines\n"
    if prompt:
        result += f"Prompt: {prompt}\n"
    result += f"First {max_lines} lines:\n"
    result += "\n".join(lines[:max_lines])

    return result