# Markdown Writing

This skill helps an AI agent write and improve Markdown documents such as project plans, specifications, guides, reports, and README files. It focuses on clear structure, accurate content, and formatting that is easy to read.

## Installation

With Node.js and the `skills` CLI, install from this repository:

```bash
npx skills add Kiadttiphoom/skill-authoring --skill markdown-writing
```

The repository name above is the currently configured Git remote. The remote must contain the `markdown-writing` skill for this command to install it; local commits must be pushed first. Review the repository before installing. To select an agent or install globally, consult `npx skills add --help`.

Alternatively, copy the skill directory to the skills location supported by your agent. Restart the agent or start a new session if needed for skill discovery. The installation command has not been tested here.
## Use

Ask your agent to use `markdown-writing` and identify the document or task. For example:

```text
Use markdown-writing to improve the structure and readability of this project plan.
```

```text
Use markdown-writing to write a Thai Markdown guide from these requirements.
```

The agent should preserve the user's requirements, verify relevant sources where practical, and distinguish current implementation from proposals and unknowns. Its `SKILL.md` contains the workflow.

## Files

- `SKILL.md` — instructions for writing Markdown documents.
- `scripts/validate_skill.py` and `tests/` — structural validator and tests retained from the previous skill-authoring workflow. They validate skill files, not the quality or correctness of ordinary Markdown documents.
- `assets/` and `references/` — resources retained from the previous workflow; they are not required for ordinary Markdown writing.

## Validation

To check this skill's metadata and structure:

```bash
python3 scripts/validate_skill.py .
```

PyYAML enables full YAML parsing. Without it, the validator warns that it performed only a simplified check. A structural check does not prove that a document is accurate or that a skill will activate for every matching request.
