#!/usr/bin/env python3
"""
CLI entry point for Distill CLI
"""
import argparse
import sys
import json
from distill import compress


def main():
    parser = argparse.ArgumentParser(description="Distill CLI - Compress CLI output for LLM")
    parser.add_argument("--type", "-t", default="generic", help="Output type (git-diff, npm-test, terraform, generic)")
    parser.add_argument("--prompt", "-p", default="", help="Specific prompt for extraction")
    parser.add_argument("--lines", "-l", type=int, default=20, help="Max lines for generic")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--version", action="store_true", help="Show version")

    args = parser.parse_args()

    if args.version:
        from distill import __version__
        print(f"distill {__version__}")
        return

    output = sys.stdin.read()

    result = compress(output, args.type, args.prompt)

    if args.json:
        print(json.dumps({"compressed": result, "type": args.type}))
    else:
        print(result)


if __name__ == "__main__":
    main()