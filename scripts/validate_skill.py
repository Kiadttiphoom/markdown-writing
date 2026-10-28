#!/usr/bin/env python3
"""Validate a SKILL.md file against the Agent Skills format.

Usage:
    python3 scripts/validate_skill.py [path/to/skill-dir-or-SKILL.md]
    python3 scripts/validate_skill.py --help

Exit codes:
    0  no FAIL results (WARN results may exist)
    1  at least one FAIL result
    2  usage error or file not found

Checks performed (each reported as PASS, FAIL, or WARN):
    frontmatter, name, name/folder match, description, unknown fields,
    line count, heading hierarchy, code fences, referenced files, secret patterns.

Limits: this script checks structure only. It does not test trigger quality,
instruction clarity, or rule conflicts. Those need manual or agent review.
"""
import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
KNOWN_FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"ghp_[A-Za-z0-9]{30,}"),
    re.compile(r"(?i)(password|passwd|api[_-]?key|secret|token)\s*[:=]\s*['\"]?[A-Za-z0-9/+_\-]{12,}"),
]
MAX_NAME = 64
MAX_DESC = 1024
MAX_LINES = 500

results = []


def report(status, check, note=""):
    results.append((status, check, note))


def parse_frontmatter(text):
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    if not m:
        return None, None
    raw = m.group(1)
    try:
        import yaml  # optional dependency
        data = yaml.safe_load(raw)
        return data, raw
    except ImportError:
        pass
    except Exception as exc:  # malformed YAML
        return exc, raw
    # Minimal fallback parser: top-level "key: value" lines only.
    data = {}
    for line in raw.splitlines():
        if re.match(r"^[A-Za-z0-9_-]+\s*:", line):
            key, _, value = line.partition(":")
            data[key.strip()] = value.strip().strip("'\"")
    return data, raw


def check_headings(lines):
    in_fence = False
    fence_marker = ""
    prev_level = 0
    h1_count = 0
    problems = []
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        fence = re.match(r"^(`{3,}|~{3,})", stripped)
        if fence:
            marker = fence.group(1)
            if not in_fence:
                in_fence, fence_marker = True, marker
            elif marker[0] == fence_marker[0] and len(marker) >= len(fence_marker):
                in_fence = False
            continue
        if in_fence:
            continue
        h = re.match(r"^(#{1,6})\s+\S", line)
        if h:
            level = len(h.group(1))
            if level == 1:
                h1_count += 1
            if prev_level and level > prev_level + 1:
                problems.append(f"line {i}: jumps from H{prev_level} to H{level}")
            prev_level = level
    return h1_count, problems, in_fence


def check_fences(lines):
    in_fence = False
    marker = ""
    for line in lines:
        m = re.match(r"^\s*(`{3,}|~{3,})", line)
        if not m:
            continue
        mk = m.group(1)
        if not in_fence:
            in_fence, marker = True, mk
        elif mk[0] == marker[0] and len(mk) >= len(marker):
            in_fence = False
    return not in_fence


def main(argv):
    if any(a in ("-h", "--help") for a in argv):
        print(__doc__)
        return 0
    target = Path(argv[0]) if argv else Path(".")
    skill_md = target / "SKILL.md" if target.is_dir() else target
    if not skill_md.is_file():
        print(f"ERROR: file not found: {skill_md}", file=sys.stderr)
        return 2

    skill_dir = skill_md.resolve().parent
    text = skill_md.read_text(encoding="utf-8")
    lines = text.splitlines()

    fm, _raw = parse_frontmatter(text)
    if fm is None:
        report("FAIL", "Frontmatter", "not found or not closed with ---")
        fm = {}
    elif isinstance(fm, Exception):
        report("FAIL", "Frontmatter", f"YAML error: {fm}")
        fm = {}
    elif not isinstance(fm, dict):
        report("FAIL", "Frontmatter", "not a key/value mapping")
        fm = {}
    else:
        report("PASS", "Frontmatter", "parsed")

    name = fm.get("name")
    if not name:
        report("FAIL", "name", "missing")
    elif not isinstance(name, str) or not NAME_RE.fullmatch(name) or len(name) > MAX_NAME:
        report("FAIL", "name", f"must be 1-{MAX_NAME} chars, lowercase letters/digits/single hyphens, "
               "no leading or trailing hyphen")
    else:
        report("PASS", "name", name)
        if skill_dir.name != name:
            report("WARN", "name/folder match", f"folder is '{skill_dir.name}', name is '{name}'")
        else:
            report("PASS", "name/folder match", "matches")

    desc = fm.get("description")
    if not desc or not isinstance(desc, str):
        report("FAIL", "description", "missing or empty")
    else:
        n = len(desc)
        if n > MAX_DESC:
            report("FAIL", "description", f"{n} chars exceeds {MAX_DESC}")
        else:
            report("PASS", "description", f"{n} chars")
        low = desc.lower()
        if "use when" not in low and "use for" not in low and "use this" not in low:
            report("WARN", "description trigger", "no explicit 'Use when ...' phrase found")
        if "do not use" not in low and "don't use" not in low:
            report("WARN", "description boundary", "no explicit 'Do not use ...' phrase found")

    unknown = sorted(set(fm) - KNOWN_FIELDS)
    if unknown:
        report("WARN", "unknown fields", ", ".join(unknown) + " (may be unsupported by the platform)")
    elif fm:
        report("PASS", "unknown fields", "none")

    if len(lines) > MAX_LINES:
        report("WARN", "line count", f"{len(lines)} lines exceeds recommended {MAX_LINES}")
    else:
        report("PASS", "line count", f"{len(lines)} lines")

    h1_count, problems, unclosed = check_headings(lines)
    if h1_count != 1:
        report("WARN", "H1 count", f"expected exactly 1, found {h1_count}")
    if problems:
        report("FAIL", "heading hierarchy", "; ".join(problems[:5]))
    else:
        report("PASS", "heading hierarchy", "no skipped levels")

    if check_fences(lines):
        report("PASS", "code fences", "balanced")
    else:
        report("FAIL", "code fences", "unclosed fence")

    refs = set(re.findall(r"`((?:scripts|references|assets)/[A-Za-z0-9_./\-]+)`", text))
    missing = sorted(r for r in refs if not (skill_dir / r).exists())
    if missing:
        report("FAIL", "referenced files", "missing: " + ", ".join(missing))
    else:
        report("PASS", "referenced files", f"{len(refs)} referenced, all exist")

    hits = []
    for i, line in enumerate(lines, 1):
        if any(p.search(line) for p in SECRET_PATTERNS):
            hits.append(str(i))
    if hits:
        report("WARN", "secret patterns", "possible secret on line(s) " + ", ".join(hits[:10]))
    else:
        report("PASS", "secret patterns", "none detected")

    width = max(len(c) for _, c, _ in results)
    for status, check, note in results:
        print(f"{status:<5} {check:<{width}}  {note}")
    fails = sum(1 for s, _, _ in results if s == "FAIL")
    warns = sum(1 for s, _, _ in results if s == "WARN")
    print(f"\nSummary: {fails} FAIL, {warns} WARN")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
