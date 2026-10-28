# skill-authoring

An Agent Skill that helps an AI coding agent create, review, and improve `SKILL.md` files.

This README is for humans. Agents do not need it, and it can be deleted without affecting the skill. If your platform or validator objects to extra top-level files, remove it.

## What it does

- Creates new `SKILL.md` files from your requirements.
- Reviews existing skills for malformed YAML, vague triggers, conflicting rules, and missing scope.
- Splits oversized skills into `references/` files.
- Produces a Validation Report that uses only `PASS`, `FAIL`, `NOT RUN`, and `NOT APPLICABLE`.

## Folder structure

```text
skill-authoring/
├── SKILL.md                      Required. Instructions the agent follows
├── README.md                     This file (for humans)
├── scripts/
│   └── validate_skill.py         Structural validator (Python 3, standard library only)
├── references/
│   └── platform-notes.md         Platform requirements with sources and verification status
└── assets/
    └── skill-template.md         Starter template for new skills
```

## Installation

Place the whole `skill-authoring` folder where your agent loads skills. The folder name must match the `name` field in `SKILL.md`.

Example location on Windows:

```text
C:\Users\<user>\.agents\skills\skill-authoring\
```

The correct location depends on your platform. Confirm it in the official documentation of the agent you use. This README does not verify any platform's skill path.

## Usage

Ask your agent in plain language. Examples:

```text
Create a skill for reviewing Go backend code that communicates with MQTT.
```

```text
Review this SKILL.md for malformed YAML, unclear instructions, conflicting rules, and missing trigger conditions.
```

Whether the agent activates the skill depends on the platform's selection mechanism. If it does not activate, mention the skill by name in your request.

## Validating a skill

Run the validator on any skill folder:

```bash
python3 scripts/validate_skill.py path/to/skill-folder
```

On Windows, use `python` or `py` if `python3` is not available:

```bat
py scripts\validate_skill.py path\to\skill-folder
```

| Result | Meaning |
|---|---|
| `PASS` | The check passed |
| `WARN` | Review it; may be acceptable |
| `FAIL` | Must be fixed; the script exits with code 1 |

The script checks structure only: frontmatter, `name`, folder match, `description` length, unknown fields, line count, heading hierarchy, code fences, referenced files, and secret-like patterns. It does not judge trigger quality, instruction clarity, or rule conflicts. PyYAML is optional; without it the script uses a simplified frontmatter parser.

## Verification status

| Item | Status |
|---|---|
| `SKILL.md` frontmatter and validator run on this skill | PASS (validator run on 2026-10-28) |
| Validator tested against a deliberately broken sample | PASS (reported the expected failures) |
| Trigger behavior with a real agent | NOT RUN |
| Compatibility with Claude Code | NOT RUN |
| Compatibility with Codex | NOT RUN |
| Agent Skills open format rules | Partially verified from search excerpts; see `references/platform-notes.md` |

## Updating

1. Edit `SKILL.md` or the bundled files.
2. Run the validator and resolve every `FAIL`.
3. If you add a bundled file, reference it from `SKILL.md` and say when the agent should read or run it. Files the agent is never told about will not be used.
4. If you change the platform rules you rely on, update `references/platform-notes.md` with the source URL and date.
