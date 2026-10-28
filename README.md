# Skill Authoring: Markdown Documents

This skill helps an AI agent write and improve Markdown documents such as project plans, specifications, guides, reports, and README files. It focuses on clear structure, accurate content, and formatting that is easy to read.

## Use

Ask your agent to use `skill-authoring` and identify the document or task. For example:

```text
Use skill-authoring to improve the structure and readability of this project plan.
```

```text
Use skill-authoring to write a Thai Markdown guide from these requirements.
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
