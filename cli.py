#!/usr/bin/env python3
"""
CLI entry point for Distill CLI
"""
import argparse
import sys
import json
import os
import re
try:
    import yaml
except ImportError:
    yaml = None
from distill import compress


def validate_lines(value):
    """Validate lines parameter."""
    try:
        lines = int(value)
    except (ValueError, TypeError):
        raise argparse.ArgumentTypeError(f"invalid lines: {value}")
    if lines < 1:
        raise argparse.ArgumentTypeError(f"lines must be >= 1")
    return lines


def main():
    parser = argparse.ArgumentParser(
        description="Distill CLI - Compress CLI output for LLM",
        epilog="Examples:\n"
               "  git diff | distill                Compress git diff output\n"
               "  npm test | distill -t npm-test   Compress npm test output\n"
               "  git diff | distill -f json      Output as JSON\n"
               "  git diff | distill -t git-diff -p 'summarize changes'"
    )
    parser.add_argument("--type", "-t", default=os.environ.get("DISTILL_TYPE", "generic"), help="Output type")
    parser.add_argument("--prompt", "-p", default="", help="Specific prompt for extraction")
    parser.add_argument("--lines", "-l", type=validate_lines, default=int(os.environ.get("DISTILL_LINES", "20")), help="Max lines")
    parser.add_argument("--format", "-f", default=os.environ.get("DISTILL_FORMAT", "text"), choices=["text", "json", "markdown", "yaml"], help="Output format")
    parser.add_argument("--tokens", action="store_true", help="Show token estimate")
    parser.add_argument("-q", "--quiet", action="store_true", help="Quiet mode for scripts")
    parser.add_argument("--version", action="store_true", help="Show version")

    args = parser.parse_args()

    if args.version:
        from distill import __version__
        print(f"distill {__version__}")
        return

    output = sys.stdin.read()

    result = compress(output, args.type, args.prompt, args.lines)

    if args.tokens:
        words = result.split()
        token_est = sum(len(w) for w in words) / 4
        token_est = int(token_est)
        result = f"Tokens: ~{token_est}\n{result}"

    if args.quiet:
        sys.exit(0)
    elif args.format == "json":
        print(json.dumps({"result": result, "type": args.type}))
    elif args.format == "markdown":
        print(f"```{args.type}\n{result}\n```")
    elif args.format == "yaml" and yaml:
        print(yaml.dump({"result": result, "type": args.type}))
    elif args.format == "yaml":
        import warnings
        warnings.warn("yaml not installed, falling back to text")
        print(result)
    else:
        print(result)


if __name__ == "__main__":
    main()