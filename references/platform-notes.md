# Platform Notes

Read this file when Step 1 of the workflow requires checking the target standard, or when the user asks which fields or limits a platform supports.

## Contents

- Verification status
- Agent Skills open format
- Claude Code
- Codex
- How to update this file

## Verification status

| Item | Status |
|---|---|
| Agent Skills open format (agentskills.io) | Partially verified on 2026-10-28 from search excerpts of the published specification and secondary mirrors. Re-check the live specification before asserting a rule as mandatory. |
| Claude Code skill behavior | NOT VERIFIED in this file. Check official Claude Code documentation. |
| Codex skill behavior | NOT VERIFIED in this file. Check official Codex documentation. |

Do not report a platform as "compliant" based on this file alone.

## Agent Skills open format

Source: https://agentskills.io/specification (retrieved via search excerpts, 2026-10-28).

| Item | Rule as retrieved |
|---|---|
| Required file | `SKILL.md` containing YAML frontmatter followed by Markdown |
| `name` | Required. Max 64 characters. Lowercase letters, digits, hyphens only. Must not start or end with a hyphen. No consecutive hyphens. Should match the parent directory name |
| `description` | Required. 1 to 1024 characters. Should describe what the skill does and when to use it |
| Optional fields | `license`, `compatibility`, `metadata`, `allowed-tools` (the last is marked experimental and support varies by implementation) |
| Optional directories | `scripts/`, `references/`, `assets/` |
| Loading model | Metadata (name + description) is always loaded; the SKILL.md body loads on activation; bundled files load on demand |
| Body size | Under 5000 tokens recommended; under about 500 lines is a common guideline |
| File references | Keep references one level deep from SKILL.md |
| Reference validator | `skills-ref validate ./my-skill` (from the agentskills project; not run in this environment) |

## Claude Code

NOT VERIFIED. Before relying on any Claude Code specific behavior (extra frontmatter fields, install locations, invocation syntax), consult the official Claude Code documentation and record the findings here with the date.

## Codex

NOT VERIFIED. Before relying on any Codex specific behavior (skill discovery paths, supported fields, metadata files), consult the official Codex documentation and record the findings here with the date.

## How to update this file

1. Fetch the official documentation for the platform.
2. Copy only facts the documentation states. Do not infer.
3. Record the source URL and the retrieval date next to each fact.
4. Change the status in the Verification status table to match what was actually checked.
