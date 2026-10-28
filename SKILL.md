---
name: skill-authoring
description: Create, review, and improve SKILL.md files (Agent Skills) for AI coding agents such as Claude Code and Codex, including frontmatter, trigger conditions, scope, workflow, and a validation report. Use whenever the user asks to write, generate, audit, fix, refactor, or shorten a skill or SKILL.md, even if they do not name the file format. Do not use for general README or documentation writing, or for executing the task that a skill describes.
---

# Skill: Skill Authoring

## Purpose

Create and improve `SKILL.md` files so that an AI agent reading them knows (1) when to activate the skill, (2) what to do and in what order, (3) what it must not do, and (4) how to verify the result, without guessing or inventing requirements.

A good skill is a document that controls agent behavior. It is not a document that merely looks polished or long. Prioritize correctness, clarity, and real-world usability over formal completeness.

## Scope

### In Scope

- Creating new SKILL.md files from user requirements.
- Reviewing and fixing existing SKILL.md files (YAML, triggers, conflicting rules, ambiguity).
- Shortening a long skill or splitting it into `references/` files.
- Producing a Validation Report.

### Out of Scope

- Executing the task that the authored skill describes.
- Writing general documentation that is not a skill.
- Guaranteeing that a skill will be activated every time (activation depends on the platform's selection mechanism).

## Prerequisites

Before starting, obtain or ask for these four items:

1. What the skill does and which problem it solves.
2. The target platform (Claude Code, Codex, other).
3. Example real user requests that should activate the skill.
4. The required output format, if any.

## Mandatory Rules

- **MUST** read the entire source file before modifying an existing skill, and preserve rules that are still valid.
- **MUST** state every significant assumption, classified as one of: user-specified, standard-defined, author's suggestion, or unconfirmed assumption.
- **MUST** put both "use when" and "do not use when" conditions in `description`, because the platform uses that field to select skills.
- **MUST** write verifiable instructions (see Instruction Design).
- **MUST** validate YAML with a real tool whenever a shell is available.
- **MUST** check the file for self-contradicting rules before delivery.
- **MUST NOT** claim a file meets a standard, passed a test, or was saved successfully unless that was actually done.
- **MUST NOT** invent tool names, fields, or platform capabilities that lack evidence.
- **MUST NOT** overwrite an existing file without inspecting its contents, and **MUST NOT** modify unrelated files.
- **MUST NOT** include real tokens, passwords, or API keys in examples.
- **MUST NOT** write instructions that make an agent reveal secrets, bypass required approvals, or destroy data outside the task scope.
- **MUST NOT** place conversational filler in the SKILL.md file.

### Recommended Practices

- Give a short reason for each important rule. Agents handle edge cases better when they know why a rule exists.
- Write `description` slightly assertively and include phrases users actually type, because skills tend to be under-triggered.
- Keep SKILL.md under roughly 500 lines. Move the remainder to `references/`.
- Remove any section that would not change the agent's behavior.

## Workflow

### Step 1: Verify the target standard

1. Identify the platform. If the user did not specify one, choose a suitable platform and record it as an assumption.
2. If a web search tool is available, check the official documentation before asserting that any rule is mandatory.
3. If verification is not possible, state "not verified against official documentation" in the report.

Requirements of the Agent Skills open format (agentskills.io) as last retrieved. Other platforms may differ. Read `references/platform-notes.md` for sources, dates, and verification status, and confirm against the target platform every time:

| Item | Requirement |
|---|---|
| `name` | 1 to 64 characters; lowercase letters, digits, single hyphens; no leading or trailing hyphen; matches the folder name |
| `description` | Required; 1 to 1024 characters |
| Optional fields | `license`, `compatibility`, `metadata`, `allowed-tools` (support varies) |
| File name | `SKILL.md` in the casing the platform requires |

### Step 2: Gather information

1. Inspect the available context and existing files first.
2. If missing items from Prerequisites materially affect correctness, ask only the necessary questions (at most 3 per round).
3. If the gap is minor, produce a draft and list the assumptions. Do not invent project details such as libraries or repository structure.

### Step 3: Design

1. Define the purpose, scope, and out-of-scope items.
2. Write `description` (what it does, when to use it, when not to use it).
3. Choose a structure based on complexity (see Structure Selection).
4. Specify when the skill must hand off to another skill or ask the user.

### Step 4: Write

1. Follow Markdown Rules and Instruction Design.
2. Keep rules, workflow, examples, reference material, edge cases, and validation in separate sections.
3. Do not let examples introduce rules that are absent from the Rules section.

### Step 5: Validate

1. Run `scripts/validate_skill.py` on the skill (see Validation Commands).
2. Check heading hierarchy, closed code fences, and conflicting rules.
3. Test triggers with at least 3 prompts that should activate the skill and 2 that should not. State clearly whether the test was run against a real agent or reasoned through manually.
4. Fix issues and re-validate until no fixable `FAIL` remains.

### Step 6: Deliver

Deliver according to Expected Output Structure.

## Bundled Resources

| File | Read or run it when |
|---|---|
| `scripts/validate_skill.py` | Step 5 of the workflow, and after every edit to a SKILL.md. Run it; do not read it unless it fails unexpectedly |
| `references/platform-notes.md` | Step 1, when asserting what a platform requires or supports |
| `assets/skill-template.md` | Step 4, when starting a new skill. Copy it and fill in each placeholder |

If a bundled file is missing, state which one and continue using the rules in this file.

## Structure Selection

| Complexity | Structure to use |
|---|---|
| Low (single step, few rules) | Frontmatter + Purpose + Rules + Example |
| Medium | Add Scope, When to Use / When Not to Use, Workflow, Edge Cases |
| High (multiple domains or over ~500 lines) | SKILL.md holds the workflow and branch selection; details move to `references/<topic>.md` with a note on when to read each |

Do not add sections only to make the file look complete or formal.

Starter skeleton for medium to high complexity skills:

````markdown
---
name: example-skill
description: <What it does>. Use when <situations or user phrases>. Do not use for <unrelated work>.
---

# Skill: Example Skill

## Purpose
## Scope
### In Scope
### Out of Scope
## When to Use
## When Not to Use
## Mandatory Rules
### Recommended Practices
## Workflow
## Expected Output Structure
## Examples
## Gotchas / Edge Cases
## Validation Checklist
````

## Trigger Design

`description` must cover: the capability, use-when conditions, do-not-use-when conditions, and boundaries that belong to other skills.

- **MUST** use wording that names real tasks. Avoid broad wording that causes over-triggering (for example, "helps with code").
- **MUST** include phrases users actually type.
- **MUST NOT** define conditions that contradict the skill's purpose.
- **MUST NOT** claim that a trigger will always fire.

Comparison:

| Weak | Strong |
|---|---|
| `Helps with Go code.` | `Review Go backend code that uses MQTT (topics, QoS, reconnect, duplicate messages, auth). Use when the user asks to review or audit MQTT handling in Go. Do not use for non-Go code or generic Go style review.` |

## Instruction Design

Any instruction that affects correctness or safety must include the elements it needs from these five: **Action, Condition, Constraint, Verification, Failure Handling**.

Good example:

```markdown
- When editing Go files, run the relevant tests if the environment supports it.
- If tests fail, investigate the cause and report the result.
- Do not report tests as passing unless they were actually run.
- If tests cannot be run, state the limitation explicitly.
```

Do not use the following wording as rules because it cannot be verified: "handle it well", "try to be appropriate", "check as needed", "use the best method possible". If an instruction is only advice, move it to Recommended Practices and label it as a recommendation.

## Markdown Rules

- Use `#` exactly once for the skill title, `##` for main sections, `###` for subsections, and `####` only when truly needed. Do not skip levels.
- Do not use headings as a substitute for bold text.
- Use bullets for unordered items, numbered lists for ordered steps, and tables for comparing multiple items.
- Use fenced code blocks with a language tag. Use a 4-backtick outer fence when the block contains nested code fences.
- Use standard Markdown. Avoid HTML and platform-specific syntax unless necessary.
- Quote YAML values that contain `:` or other special characters, and keep Markdown out of the frontmatter.

## Consistency Check

Before delivery, look for contradicting rules, for example: do not edit files vs. edit the same file; answer briefly vs. always show full detail; allow a tool vs. forbid the same tool; auto-fix vs. wait for approval; output structure in Rules differs from the one in Examples.

When a conflict is found:

1. Identify the conflicting rules and their locations.
2. Check whether a precedence order is defined. Platform requirements and user instructions take priority.
3. Align rules at the same level so they agree.
4. If it cannot be resolved, report the conflict and ask for confirmation.
5. **MUST NOT** delete important user requirements arbitrarily to resolve a conflict.

## Validation Commands

Use these when a shell is available. If not, set the related items to `NOT RUN` with a reason.

```bash
python3 scripts/validate_skill.py path/to/skill-folder
```

The script reports `PASS`, `FAIL`, or `WARN` for: frontmatter, `name`, folder match, `description`, unknown fields, line count, heading hierarchy, code fences, referenced files, and secret patterns. It exits with code 1 when any `FAIL` exists.

Rules for using the result:

- **MUST** fix every `FAIL` and re-run, or report why it could not be fixed.
- **MUST** review each `WARN` and either fix it or note why it is acceptable.
- **MUST NOT** treat a clean script run as proof that triggers, rule clarity, or rule consistency are correct. Those checks remain manual.
- The script works without PyYAML by using a simplified parser. When PyYAML is installed, it performs full YAML parsing. If PyYAML is missing, state that YAML was only checked at the simplified level.
- If the official `skills-ref validate` tool is available, running it is optional extra evidence. Report it as `NOT RUN` when unavailable.

## Expected Output Structure

When creating or modifying a skill, deliver in this order:

1. **Skill File:** Save SKILL.md at the location the user specifies. If none is specified, inspect the project structure first. When editing an existing file, change only the necessary parts and do not rewrite the whole file without need.
2. **Validation Report:** A table in the format below.
3. **Summary:** What was created or changed, file location, checks actually performed, assumptions, and remaining limitations.

Allowed statuses only:

- `PASS`: checked and passed.
- `FAIL`: checked and failed.
- `NOT RUN`: not checked.
- `NOT APPLICABLE`: not relevant to this skill.

```markdown
| Check | Status | Evidence / Notes |
|---|---|---|
| Frontmatter syntax | PASS | Parsed with PyYAML |
| Required metadata | PASS | name, description |
| Markdown structure and heading hierarchy | PASS | Manual review |
| Trigger conditions | NOT RUN | Not tested with a real agent |
| Instruction consistency | PASS | No conflicting rules found |
| Scope boundaries | PASS | In/Out of Scope present |
| Examples and edge cases | PASS | |
| Compatibility with target platform | NOT RUN | Not compared with official docs |
```

The table above is a format sample only. Every status must come from a check that was actually performed.

## Examples

### Example A: Create a new skill

Input: `Create a skill for reviewing Go backend code that communicates with MQTT.`

Expected behavior:

- Scope triggers to Go + MQTT review and define coverage (topics, QoS, reconnect, duplicates, auth).
- State out-of-scope items and the review report format.
- Do not assume an MQTT library, broker, or repository layout. If unknown, ask or record an assumption.

### Example B: Review an existing skill

Input: `Review this SKILL.md for malformed YAML, unclear instructions, conflicting rules, and missing trigger conditions.`

Expected behavior:

- Read the file first, list issues with locations, explain impact, propose targeted fixes, and re-validate after fixing.
- Preserve existing rules that are still valid.

### Example C: Insufficient information

Input: `Create a production-ready skill for my project.`

Expected behavior:

- Inspect available context, then ask only about what is missing (platform, task type, constraints).
- Do not invent project details.

## Gotchas / Edge Cases

| Situation | Handling |
|---|---|
| Malformed YAML (bad indentation, unquoted `:`, missing closing `---`) | Fix, then re-run the parser |
| Metadata does not match platform requirements | Fix per the platform, or report that it could not be confirmed |
| Trigger is ambiguous or too broad | Add use-when / do-not-use-when and real user phrases |
| User supplies an invalid name (spaces, dots, typos) | Propose a close kebab-case name and ask the user to confirm |
| Skill is too long | Move details to `references/` with a note on when to read them |
| Duplicate rules | Merge them without losing substance |
| Examples read as rules | Move the rule to the Rules section and let the example refer to it |
| No shell or no web search | Mark affected checks `NOT RUN` and give the reason |
| Target file already exists | Read and compare first; do not overwrite without permission |

## Validation Checklist

- [ ] Frontmatter is valid and actually parsed.
- [ ] `name` matches the required format and the folder name.
- [ ] `description` contains both use-when and do-not-use-when conditions.
- [ ] Heading hierarchy is correct and code fences are closed.
- [ ] Purpose and Scope (in and out) are clear.
- [ ] Mandatory Rules are separated from Recommended Practices.
- [ ] No unverifiable vague wording in Rules.
- [ ] No conflicting rules, and examples do not contradict rules.
- [ ] Failure handling exists for risky steps.
- [ ] No secrets or real data in examples.
- [ ] Triggers were tested and untested items are reported.
- [ ] The Validation Report contains no `PASS` that was not actually checked.
