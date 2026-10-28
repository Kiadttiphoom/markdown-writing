---
name: replace-with-skill-name
description: Replace with one or two sentences saying what the skill does. Use when <situations and phrases users actually type>. Do not use for <nearby tasks that belong elsewhere>.
---

# Skill: Replace With Skill Title

## Purpose

State the problem this skill solves and the outcome it produces.

## Scope

### In Scope

- Responsibility covered by this skill.

### Out of Scope

- Responsibility that belongs elsewhere, with the skill or action to hand off to.

## Prerequisites

- Information, tools, or context that must exist before starting.
- What to do when a prerequisite is missing (ask the user or record an assumption).

## Mandatory Rules

- **MUST** state the required behavior, the condition, and how to verify it.
- **MUST NOT** state the prohibited behavior and what to do instead.

### Recommended Practices

- Advice that improves quality but is not enforced. Label it as a recommendation.

## Workflow

1. Analyze the request and the available context.
2. Identify missing requirements and ask or record assumptions.
3. Execute the task.
4. Verify the result with a concrete check.
5. Report the outcome, including anything not verified.

## Expected Output Structure

Describe the required format of the deliverable, if the skill produces one.

## Examples

### Example A: Typical request

Input: `Replace with a realistic user request.`

Expected behavior:

- Replace with observable behavior.

## Gotchas / Edge Cases

| Situation | Handling |
|---|---|
| Replace with an unusual condition | Replace with the recovery behavior |

## Validation Checklist

- [ ] Frontmatter parses and `name` matches the folder name.
- [ ] `description` contains both use-when and do-not-use-when conditions.
- [ ] No conflicting rules.
- [ ] Examples agree with the rules.
- [ ] Untested items are reported as such.
