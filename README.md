# Skill Authoring

Create, review, and improve `SKILL.md` files for AI coding agents. Skill Authoring helps turn a task into clear activation conditions, actionable instructions, and checks that distinguish verified results from assumptions.

## What it does

- Creates skills from a stated task and target platform.
- Reviews an existing skill for unclear triggers, conflicting rules, scope gaps, and malformed frontmatter.
- Refactors long skills into a focused `SKILL.md` with supporting references.
- Reports checks performed, limitations, and significant assumptions.

It is intended for **authoring skills**. It does not execute the task described by a skill or replace general documentation tools. Activation depends on the agent and its skill-discovery settings.

## Getting started

Install the complete folder in a skills directory supported by your agent. Keep the folder name `skill-authoring`, matching the `name` in `SKILL.md`. Installation paths vary by platform; check its documentation before installing.

For example, the third-party `skills` CLI can install from the repository below. Review the source and CLI options before running a command that downloads files:

```bash
npx skills add Kiadttiphoom/skill-authoring
```

Alternatively, copy the repository folder into your agent's skill directory. Restart the agent or start a new session if your platform requires it to discover newly installed skills. CLI installation and agent-specific compatibility have not been verified by this README.

Ask your agent to use `skill-authoring`, for example:

```text
Use skill-authoring to create a skill for reviewing API contracts.
```

```text
Use skill-authoring to review this SKILL.md for ambiguous triggers and conflicting rules.
```

The agent should inspect the available context first and ask only for missing information that materially affects correctness. For an existing file, an explicit request to edit it authorizes the requested changes; the agent should inspect it and preserve relevant instructions.

## Validate a skill

Run from the `skill-authoring` directory with Python 3:

```bash
python3 scripts/validate_skill.py path/to/skill-folder
```

On Windows, if the Python launcher is installed:

```powershell
py scripts\validate_skill.py path\to\skill-folder
```

You can pass a folder containing `SKILL.md` or a path to the file itself. The script reads files and reports findings; it does not modify the skill or access the network.

| Result | Meaning |
| --- | --- |
| `PASS` | The particular check passed. |
| `WARN` | Review the limitation or potential issue. Warnings do not cause exit code 1. |
| `FAIL` | A check failed. The script exits with code 1. |

Exit code `0` means there were no failures, even if warnings remain; `2` indicates a usage error or missing file. The validator checks structure, references and some secret-like patterns. It cannot establish that a skill triggers correctly, its instructions are clear, or all platform requirements are met.

**YAML validation:** PyYAML is optional. With PyYAML, the script parses YAML; without it, the script emits a warning and performs only a simplified frontmatter check. A simplified check is not full YAML validation. Install PyYAML in an appropriate Python environment if full parsing is needed.

## Run validator tests

```bash
python3 -m unittest discover -s tests -v
```

The suite exercises valid input, a folder-name mismatch, missing frontmatter and references, an unclosed code fence, and the simplified-parser warning. The malformed-YAML test requires PyYAML and is skipped when it is unavailable. Review the test output before reporting a check as passed.

## Files

```text
skill-authoring/
├── SKILL.md                         Agent instructions
├── README.md                        This guide
├── assets/skill-template.md         Starter template
├── references/platform-notes.md     Sources and verification status
├── scripts/validate_skill.py        Read-only structural validator
└── tests/test_validate_skill.py     Validator regression tests
```

## Maintaining the skill

1. Inspect the existing instructions and change only what the task requires.
2. Run the validator and regression tests; resolve failures and explain any warnings or skipped tests.
3. Review triggers, scope, examples, and conflicting rules manually. A clean validator run does not prove these are correct.
4. When platform requirements change, verify the official source and update `references/platform-notes.md` with the source and date. Report anything that remains unverified.
