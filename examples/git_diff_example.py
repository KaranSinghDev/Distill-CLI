#!/usr/bin/env python3
"""
Example: Compress git diff output
"""
import subprocess
from distill import compress

result = subprocess.run(["git", "diff"], capture_output=True, text=True)
compressed = compress(result.stdout, "git-diff")
print(compressed)