#!/usr/bin/env python3
"""Read-only source-scope checks for a bounded LaTeX edit.
Only the explicitly inventoried surface is monitored. This is NOT a TeX parser,
scientific audit, repository sandbox, or proof that the inventory is complete.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re


def names_checked(root: Path, names: list[str]) -> dict[str, Path]:
    root = root.resolve()
    if not root.is_dir() or not isinstance(names, list):
        raise ValueError('Existing project root and explicit list required')
    result = {}
    for name in names:
        if not isinstance(name, str) or not name or '\\' in name:
            raise ValueError('Use relative POSIX file paths')
        rel = Path(name)
        if rel.is_absolute() or '..' in rel.parts or str(rel) != name:
            raise ValueError(f'Unsafe or ambiguous path: {name}')
        path = (root/rel).resolve()
        if not path.is_relative_to(root) or name in result:
            raise ValueError(f'Escaping or duplicate path: {name}')
        if path.exists() and not path.is_file():
            raise ValueError(f'Not a regular file: {name}')
        result[name] = path
    return result


def digest(path: Path) -> str | None:
    if not path.is_file():
        return None
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024*1024), b''):
            h.update(block)
    return h.hexdigest()


def capture(root: Path, files: list[str]) -> dict:
    paths = names_checked(root, files)
    if not paths or any(not p.is_file() for p in paths.values()):
        raise ValueError('Snapshot needs a nonempty list of existing files')
    return {'schema_version': 1, 'files': {n: digest(p) for n, p in sorted(paths.items())}}


def check(root: Path, baseline: dict, allowed: list[str], protected: list[str],
          current_files: list[str] | None = None) -> dict:
    if not isinstance(baseline, dict) or type(baseline.get('schema_version')) is not int or baseline['schema_version'] != 1:
        raise ValueError('Unsupported baseline schema')
    old = baseline.get('files')
    if not isinstance(old, dict) or not old or any(not isinstance(v, str) or not re.fullmatch('[0-9a-f]{64}', v) for v in old.values()):
        raise ValueError('Baseline needs nonempty path -> SHA-256 mapping')
    for ns in (list(old), allowed, protected, current_files or []):
        names_checked(root, ns)
    if set(allowed) & set(protected):
        raise ValueError('Protected files cannot be on the allowed-edit list')
    if not set(protected) <= set(old):
        raise ValueError('Protect templates before editing: no baseline hash available')
    names = sorted(set(old) | set(allowed) | set(protected) | set(current_files or []))
    now = {n: digest(p) for n, p in names_checked(root, names).items()}
    changed = [n for n in names if old.get(n) != now[n]]
    outside = sorted(set(changed)-set(allowed))
    locked = sorted(set(changed) & set(protected))
    return {'schema_version': 1, 'changed': changed, 'out_of_scope': outside,
            'protected_changes': locked, 'within_scope': not outside and not locked,
            'certifies_semantics': False, 'monitored_files': names,
            'current': {'schema_version': 1, 'files': now},
            'limitations': 'Explicit file surface only; unlisted files are not discovered. '
                          'File hashes do not prove semantic preservation, style compliance, '
                          'build freshness, or completeness. Also inspect the source diff.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='command', required=True)
    snap = sub.add_parser('snapshot'); snap.add_argument('root', type=Path)
    snap.add_argument('--files', nargs='+', required=True); snap.add_argument('--out', type=Path, required=True)
    verify = sub.add_parser('check'); verify.add_argument('root', type=Path)
    verify.add_argument('--baseline', type=Path, required=True)
    verify.add_argument('--allow', nargs='*', default=[]); verify.add_argument('--protect', nargs='*', default=[])
    verify.add_argument('--current-files', nargs='*', default=[]); verify.add_argument('--out', type=Path)
    a = p.parse_args()
    try:
        r = capture(a.root, a.files) if a.command == 'snapshot' else check(
            a.root, json.loads(a.baseline.read_text()), a.allow, a.protect, a.current_files)
        text = json.dumps(r, ensure_ascii=False, indent=2)+'\n'
        if a.out:
            # Never clobber either a source, a baseline, or a prior report.
            a.out.parent.mkdir(parents=True, exist_ok=True)
            with a.out.open('x', encoding='utf-8') as f: f.write(text)
        print(text, end='')
        return 0 if a.command == 'snapshot' or r['within_scope'] else 1
    except (ValueError, OSError, TypeError) as e:
        p.exit(2, f'{e}\n')

if __name__ == '__main__': raise SystemExit(main())
