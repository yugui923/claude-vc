# Contributing to Claude-VC

Thank you for your interest in contributing to claude-vc.

## Development Setup

### Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (Python package manager)
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) (for smoke
  tests only)

### Getting Started

```bash
git clone https://github.com/yugui923/claude-vc.git
cd claude-vc
uv sync          # Install dev dependencies
```

### Verify Your Setup

```bash
uv run ruff check .            # Linter
uv run ruff format --check .   # Formatter
uv run pyright scripts/ tests/ # Type checker
uv run pytest                  # Layer 1 tests (172 tests)
```

All four must pass before submitting a PR.

## Adding a New Sub-Skill

1. Create `skills/vc-<name>/SKILL.md` with frontmatter:

   ```yaml
   ---
   name: vc-<name>
   description: >
     Brief description with trigger phrases for the router.
   ---
   ```

2. Define the workflow in the SKILL.md body: input handling, analysis steps,
   output format, edge cases, and disclaimer requirement.

3. Add reference files (if needed) to `skills/vc/references/`.

4. Register the route in `skills/vc/SKILL.md` (routing table and
   intent-matching logic).

5. Add a Layer 2 smoke test in `tests/layer2/test_skill_smoke.py`.

## Adding a New Python Script Command

1. Add the command to `captable.py`, `financial_model.py`, or create a new
   script if the domain is distinct.

2. Follow the CLI pattern: first argument is `command`, JSON input from
   stdin.

3. Use stdlib only (no third-party runtime deps). Type-annotate all function
   signatures.

4. Add test fixtures in `tests/fixtures/<script>/` and Layer 1 tests in
   `tests/layer1/test_<script>_<command>.py`.

5. Verify invariants: cap tables must sum to 100% ownership; financial
   models must satisfy A=L+E and cash flow linkage.

## Code Quality

| Tool    | Command                          | Checks             |
| ------- | -------------------------------- | ------------------ |
| Ruff    | `uv run ruff check .`           | Linting            |
| Ruff    | `uv run ruff format --check .`  | Formatting         |
| Pyright | `uv run pyright scripts/ tests/`| Type correctness   |
| Pytest  | `uv run pytest`                 | Tests (172 tests)  |

All must pass. New Python code must have type annotations and pass pyright.

## Commit Messages

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add portfolio export to Excel
fix: correct SAFE conversion when cap < discount price
docs: update user guide with portfolio workflow
chore: bump ruff to 0.9.x
refactor: extract waterfall calculation into helper
test: add MFN SAFE resolution edge case tests
```

Imperative mood, under 72 characters, body for non-trivial changes.

## Pull Request Process

1. Fork and create a feature branch from `main`
2. Make changes following the conventions above
3. Run all quality gates (ruff, pyright, pytest)
4. Write a clear PR description explaining what and why
5. Link related issues
6. Keep PRs focused -- one logical change per PR

PRs require one approving review. Address feedback with new commits (do not
force-push during review).

## Testing

See [tests/TESTING.md](tests/TESTING.md) for the full strategy. Layer 1
(unit/integration) tests are fast and deterministic. Layer 2 (smoke) tests
require Claude CLI and are optional during development.

## Code of Conduct

We follow the
[Contributor Covenant v2.1](https://www.contributor-covenant.org/version/2/1/code_of_conduct/).

## License

By contributing, you agree that your contributions will be licensed under the
[MIT License](LICENSE).
