#!/usr/bin/env python3
"""Development checks, not an LLM evaluator. No runtime dependencies added."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
NAMES = set('food-nutrition fitness healthy-living travel-planner personal-finance learning-coach career-assistant home-living relationship-advisor leisure-entertainment'.split())
CATEGORIES = set('typical missing cross-domain simple boundary markdown'.split())


def read_lines(path):
    return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line.strip()]


def check_output(text):
    """Format guard only. Markdown-shaped unsafe/wrong answers still need review."""
    errors = []
    if not isinstance(text, str) or not text.strip():
        return ['empty/non-string answer']
    stripped = text.strip()
    if re.search(r'<!doctype|</?(?:html|head|body|div|span|style|script|iframe|table|svg)\b', text, re.I):
        errors.append('HTML/web markup')
    if re.search(r'```\s*(?:json|yaml|yml|xml|html|css|javascript|js)\b', text, re.I):
        errors.append('structured/web code block as deliverable')
    try:
        value = json.loads(stripped)
        if isinstance(value, (dict, list)):
            errors.append('raw JSON deliverable')
    except ValueError:
        pass
    if re.match(r'(?:<\?xml|<[A-Za-z][\w:-]*(?:\s[^>]*)?>)', stripped):
        errors.append('raw XML/tag deliverable')
    if re.match(r'^(?:---\s*\n)?[\w-]+:\s*\S', stripped, re.ASCII) and len(re.findall(r'^[\w-]+:', stripped, re.M | re.ASCII)) > 1:
        errors.append('possible raw YAML deliverable; review required')
    if re.search(r'!\[|\]\((?:sandbox:|file:|/)|\]\([^)]*\.(?:pdf|docx|xlsx|png|jpg|html)(?:[?#][^)]*)?\)', text, re.I):
        errors.append('image/file deliverable')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runtime', type=Path, help='optional local zhizhi-agent-runtime source')
    parser.add_argument('--responses', type=Path, help='JSONL containing case id and actual text; full 70-case set required')
    args = parser.parse_args()
    files = sorted((ROOT / 'skills').glob('*/SKILL.md'))
    if {p.parent.name for p in files} != NAMES:
        raise ValueError('expected exactly the 10 named skills')
    for path in files:
        text = path.read_text(encoding='utf-8')
        header, body = text.removeprefix('---\n').split('\n---\n', 1)
        fields = dict(line.split(': ', 1) for line in header.splitlines())
        if fields.get('name') != path.parent.name or not fields.get('description'):
            raise ValueError(f'{path}: invalid metadata')
        if set(fields) != {'name', 'description'} or len(fields['description']) > 1024:
            raise ValueError(f'{path}: unexpected metadata or long description')
        if len(text.encode()) > 65536 or 'Markdown' not in body or 'JSON' not in body or 'HTML' not in body:
            raise ValueError(f'{path}: missing output protocol or oversized instructions')
    cases = read_lines(ROOT / 'evals/cases.jsonl')
    routing = read_lines(ROOT / 'evals/routing.jsonl')
    ids = {case['id'] for case in cases + routing}
    if len(ids) != 70:
        raise ValueError('case IDs must be unique, 60 task + 10 routing cases')
    for name in NAMES:
        selected = [case for case in cases if case['skill'] == name]
        if len(selected) != 6 or {case['category'] for case in selected} != CATEGORIES:
            raise ValueError(f'{name}: incomplete behavioral case coverage')
    print('PASS package: 10 skills; 60 behavioral + 10 routing cases (fixtures only)')
    if args.runtime:
        runtime = args.runtime.resolve()
        if not (runtime / 'go.mod').is_file():
            raise ValueError('runtime source must contain go.mod')
        with tempfile.TemporaryDirectory(prefix='zhizhi-skill-check-') as folder:
            Path(folder, 'go.mod').write_text(
                'module zhizhi-skills-check\n\ngo 1.25.0\n\nrequire github.com/cocoyes/zhizhi-agent-runtime v0.0.0\n'
                f'\nreplace github.com/cocoyes/zhizhi-agent-runtime => {json.dumps(str(runtime))}\n')
            subprocess.run(['go', 'run', '-mod=mod', str(ROOT / 'tools/runtimecheck.go'), str(ROOT / 'skills')],
                           cwd=folder, env={**os.environ, 'GOWORK': 'off'}, check=True)
    if args.responses:
        rows = read_lines(args.responses)
        actual = {row['id']: row for row in rows}
        if len(actual) != len(rows) or set(actual) != ids:
            raise ValueError('responses require exactly one actual answer for every case ID')
        for case in cases + routing:
            row = actual[case['id']]
            errors = check_output(row.get('text'))
            if row.get('skill') != case['skill']:
                errors.append(f"routing: expected {case['skill']!r}, got {row.get('skill')!r}")
            if errors:
                raise ValueError(f"{case['id']}: {', '.join(errors)}")
        print('PASS response format/routing labels: 70 actual responses; manual semantic review still required')


if __name__ == '__main__':
    main()
