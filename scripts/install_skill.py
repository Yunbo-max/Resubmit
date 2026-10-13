#!/usr/bin/env python3
"""Copy the complete local skill; no network, shell, or overwrite operations."""
import argparse
from pathlib import Path
import shutil
import sys


def install(source: Path, destination: Path) -> Path:
    source = source.resolve()
    destination = destination.expanduser().absolute()
    if not (source / 'SKILL.md').is_file():
        raise ValueError('Source must contain SKILL.md')
    if destination.exists() or destination.is_symlink():
        raise FileExistsError(f'Already exists; back it up or choose another destination: {destination}')
    if destination.resolve().is_relative_to(source):
        raise ValueError('Destination cannot be inside the source directory')
    if any(p.is_symlink() for p in source.rglob('*')):
        raise ValueError('Skill source must not contain symlinks')
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, destination, ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '.DS_Store'))
    return destination


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--agent', choices=('codex', 'claude'))
    group.add_argument('--destination', type=Path, help='Full destination skill directory')
    parser.add_argument('--skill', choices=('resubmitting-papers', 'selecting-conference-venues'),
                        default='resubmitting-papers', help='Skill to install (default: LaTeX editing)')
    args = parser.parse_args()
    source = Path(__file__).resolve().parents[1] / 'skills' / args.skill
    destination = args.destination or (Path.home() / ('.agents' if args.agent == 'codex' else '.claude') / 'skills' / args.skill)
    try:
        result = install(source, destination)
    except (OSError, ValueError) as exc:
        parser.exit(2, f'{exc}\n')
    print(f'Installed files at {result}\nOpen a new agent session and verify that {args.skill} is discovered.')
    return 0

if __name__ == '__main__':
    sys.exit(main())
