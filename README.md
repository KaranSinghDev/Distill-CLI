# distill-cli

> Compress noisy CLI output before sending it to an LLM — cut token usage by up to 25× with zero configuration.

As AI-assisted development becomes standard, developers routinely pipe `git diff`, `pytest`, and `terraform plan` output directly into LLMs. The problem: most of that output is noise. Distill extracts only the signal.

```bash
git diff | distill -t git-diff        # 3,009 chars → 156 chars  (19×)
pytest   | distill -t pytest          # 2,497 chars → 235 chars  (10×)
terraform plan | distill -t terraform # 1,109 chars → 61 chars   (18×)
```

---

## Why this exists

At GPT-4 pricing ($15 / 1M tokens), a CI pipeline that sends raw `pytest` output on every run burns tokens fast. At 500 tests, raw output is ~6,000 tokens per run. Distilled: ~200 tokens. **At 100 runs/day that's a 97% reduction in cost** — without losing any information an LLM actually needs.

---

## Install

```bash
pip install distill-cli
# or
git clone https://github.com/karansingh/distill-cli && pip install -e .
```

No required dependencies. PyYAML optional for `--format yaml`.

---

## Usage

```bash
# Pipe any supported command through distill
git diff          | distill -t git-diff
npm test          | distill -t npm-test
terraform plan    | distill -t terraform
pytest            | distill -t pytest
docker ps         | distill -t docker
kubectl get pods  | distill -t kubectl
cat large.log     | distill             # generic: trims to first 20 lines + count

# Output formats
git diff | distill -t git-diff -f json      # machine-readable
git diff | distill -t git-diff -f markdown  # paste into LLM chat
git diff | distill -t git-diff --tokens     # show estimated token count
```

---

## Benchmarks

Measured over 5,000 iterations on Python 3.10:

| Output type | Raw | Distilled | Ratio | Latency |
|-------------|-----|-----------|-------|---------|
| `git-diff` | 3,009 chars | 156 chars | 19× | 0.050 ms |
| `npm-test` | 1,703 chars | 100 chars | 17× | 0.138 ms |
| `terraform` | 1,109 chars | 61 chars | 18× | 0.011 ms |
| `pytest` | 2,497 chars | 235 chars | 10× | 0.354 ms |
| `generic log` | 18,389 chars | 746 chars | 24× | 0.014 ms |

All under 0.4 ms — imperceptible overhead in any pipeline.

---

## How it works

Each output type has a dedicated compressor that knows what matters:

```
stdin → type-specific compressor → structured dict → format layer → stdout

git-diff  → files changed, hunk count, first 5 hunks
pytest    → pass/fail/skip/error counts + failing test names
terraform → add/change/destroy counts
npm-test  → pass/fail counts + summary line
generic   → first N lines + total line count header
```

All compressors are pure functions — no state, no I/O, fully testable. The CLI is a thin shell: read stdin → call core → format → write stdout.

---

## CI/CD integration

```yaml
# GitHub Actions: compress test output before sending to LLM webhook
- name: Run tests
  run: pytest 2>&1 | distill -t pytest -f json > result.json
```

```bash
# Shell script: check compressed output before LLM call
SUMMARY=$(pytest | distill -t pytest)
curl -s -X POST $LLM_WEBHOOK -d "{\"content\": \"$SUMMARY\"}"
```

---

## Options

| Flag | Description |
|------|-------------|
| `-t, --type` | `git-diff` `npm-test` `terraform` `pytest` `docker` `kubectl` `generic` |
| `-f, --format` | `text` `json` `markdown` `yaml` |
| `-l, --lines` | Max lines for generic mode (default: 20) |
| `-p, --prompt` | Context hint embedded in output |
| `--tokens` | Show estimated token count |
| `-q, --quiet` | No output — for scripting |

**Environment variables:** `DISTILL_TYPE`, `DISTILL_LINES`, `DISTILL_FORMAT`

---

## Stack

Python 3.7+ · zero required dependencies · standard library only (`re`, `json`, `argparse`) · MIT License
