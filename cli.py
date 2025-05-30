#!/usr/bin/env python3
"""
CLI entry point for Distill CLI
"""
import argparse
import sys
import json
import os
from distill import compress


def main():
    parser = argparse.ArgumentParser(
        description="Distill CLI - Compress CLI output for LLM",
        epilog="Examples:\n  git diff | distill -t git-diff\n  npm test | distill -t npm-test"
    )
    parser.add_argument("--type", "-t", default=os.environ.get("DISTILL_TYPE", "generic"), help="Output type")
    parser.add_argument("--prompt", "-p", default="", help="Specific prompt for extraction")
    parser.add_argument("--lines", "-l", type=int, default=int(os.environ.get("DISTILL_LINES", "20")), help="Max lines")
    parser.add_argument("--format", "-f", default=os.environ.get("DISTILL_FORMAT", "text"), help="Output format")
    parser.add_argument("-q", "--quiet", action="store_true", help="Quiet mode for scripts")
    parser.add_argument("--version", action="store_true", help="Show version")

    args = parser.parse_args()

    if args.version:
        from distill import __version__
        print(f"distill {__version__}")
        return

    output = sys.stdin.read()

    result = compress(output, args.type, args.prompt)

    if args.quiet:
        sys.exit(0)
    elif args.format == "json":
        print(json.dumps({"result": result, "type": args.type}))
    elif args.format == "markdown":
        print(f"```{args.type}\n{result}\n```")
    else:
        print(result)


if __name__ == "__main__":
    main()