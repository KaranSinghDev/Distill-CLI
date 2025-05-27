# Distill CLI

Compress CLI output for LLM consumption - save tokens by extracting only what matters.

## Installation

```bash
pip install -e .
```

Or run directly:

```bash
python cli.py --help
```

## Usage

Pipe any command output through distill:

```bash
git diff | distill --type git-diff
npm test | distill --type npm-test
terraform plan | distill --type terraform
```

## Options

- `--type`, `-t` - Output type (git-diff, npm-test, terraform, generic)
- `--prompt`, `-p` - Specific prompt for extraction
- `--lines`, `-l` - Max lines for generic
- `--format`, `-f` - Output format (text, json, markdown)
- `--version` - Show version

## Examples

```bash
git diff | distill -t git-diff
npm test | distill -t npm-test
terraform plan | distill -t terraform
cat logs.txt | distill
```

## Features

- Compress git diff output
- Compress npm test output
- Compress terraform plan output
- Multiple output formats (text, JSON, markdown)
- Custom prompt support
- Pipe-friendly design

## License

MIT License - see LICENSE file