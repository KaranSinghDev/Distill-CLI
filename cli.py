#!/usr/bin/env python3
"""
CLI entry point for Distill CLI
"""
import argparse
import sys
import json
from distill import compress


def main():
    parser = argparse.ArgumentParser(
        description="Distill CLI - Compress CLI output for LLM",
        epilog="Examples:\n  git diff | distill -t git-diff\n  npm test | distill -t npm-test"
    )
    parser.add_argument("--type", "-t", default="generic", help="Output type (git-diff, npm-test, terraform, generic)")
    parser.add_argument("--prompt", "-p", default="", help="Specific prompt for extraction")
    parser.add_argument("--lines", "-l", type=int, default=20, help="Max lines for generic")
    parser.add_argument("--format", "-f", default="text", help="Output format (text, json, markdown)")
    parser.add_argument("--version", action="store_true", help="Show version")

    args = parser.parse_args()

    if args.version:
        from distill import __version__
        print(f"distill {__version__}")
        return

    output = sys.stdin.read()

    result = compress(output, args.type, args.prompt)

    if args.format == "json":
        print(json.dumps({"result": result, "type": args.type}))
    elif args.format == "markdown":
        print(f"```{args.type}\n{result}\n```")
    else:
        print(result)


if __name__ == "__main__":
    main()