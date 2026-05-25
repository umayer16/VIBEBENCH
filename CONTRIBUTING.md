# Contributing to VibeBench

Thank you for your interest in VibeBench! We welcome contributions that improve the accuracy of our heuristics or expand our dynamic execution capabilities.

## How to Contribute

1. **Report Bugs**: Use GitHub Issues to report any unexpected behavior in the `CodeExecutor` or `CodeAnalyzer`.
2. **Suggest Heuristics**: If you identify new "AI-isms" or patterns common in LLM-generated code, please open an issue to discuss adding a new static check.
3. **Pull Requests**:
   - Fork the repository.
   - Create a feature branch.
   - Ensure all new logic includes proper docstrings for JOSS compliance.
   - Submit a PR with a detailed description of your changes.

## Seeking Help

If you have questions about using VibeBench for your own research, please open a GitHub Issue.

## Setting Up Pre-commit Hooks

VibeBench uses [pre-commit](https://pre-commit.com/) to enforce
code quality checks before every commit. This catches flake8
lint errors and mypy type errors locally before they reach CI.

### Installation

```bash
pip install pre-commit
pre-commit install
```

After running `pre-commit install`, the hooks run automatically
on staged files before every `git commit`.

### Running Manually

To run the hooks on all files at once:

```bash
pre-commit run --all-files
```

### What the Hooks Check

| Hook | What it catches |
| ------ | ---------------- |
| trailing-whitespace | Trailing spaces on any line |
| end-of-file-fixer | Missing newline at end of file |
| check-yaml | Malformed YAML files |
| check-json | Malformed JSON files |
| check-merge-conflict | Leftover merge conflict markers |
| debug-statements | Accidental `pdb` or `breakpoint()` calls |
| flake8 | PEP 8 style violations (max line length 88) |
| mypy | Type errors in `core/` modules |

### If a Hook Fails

The commit is blocked until the issue is fixed. The hook output
tells you exactly which file and line caused the failure. Fix
the issue, stage the fixed file with `git add`, and commit again.

### Bypassing Hooks (Emergency Only)

```bash
git commit --no-verify -m "your message"
```

Use `--no-verify` only in genuine emergencies. All bypassed
commits will still be caught by CI on GitHub.
