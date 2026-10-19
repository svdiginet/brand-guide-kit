#!/usr/bin/env python3
"""Check local Markdown links and required kit entrypoints; no network access."""
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ['README.md', 'AGENTS.md', 'CLAUDE.md', 'docs/brand-system-standard.md', 'docs/references.md', 'templates/brand-guide.md', 'templates/audit.md', 'templates/3d-spec.md', 'skills/brand-guide-kit/SKILL.md', 'assets/banner.png']

def check(root):
    issues = []
    for name in REQUIRED:
        if not (root / name).is_file():
            issues.append(f'Missing required file: {name}')
    for path in sorted(root.rglob('*.md')):
        if '.git' in path.parts:
            continue
        source = path.read_text(encoding='utf-8')
        for line_number, line in enumerate(source.splitlines(), 1):
            if '\u2014' in line or '\u2013' in line:
                issues.append(f'{path.relative_to(root)}:{line_number}: long dash')
        for target in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)', source):
            target = target.strip().strip('<>')
            parts = urlsplit(target)
            if parts.scheme or not parts.path:
                continue
            resolved = (path.parent / unquote(parts.path)).resolve()
            if not resolved.is_relative_to(root.resolve()):
                issues.append(f'{path.relative_to(root)}: link leaves repository')
            elif not resolved.exists():
                issues.append(f'{path.relative_to(root)}: missing link target {target}')
    skill = root / 'skills/brand-guide-kit/SKILL.md'
    if skill.exists() and not skill.read_text().startswith('---\nname: brand-guide-kit\ndescription:'):
        issues.append('Skill requires expected name and description frontmatter')
    return issues

if __name__ == '__main__':
    failures = check(ROOT)
    for failure in failures:
        print(f'FAIL: {failure}')
    print(f'{"FAIL" if failures else "PASS"}: documentation integrity ({len(failures)} issue(s)); not visual or security certification')
    sys.exit(bool(failures))
