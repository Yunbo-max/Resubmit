#!/usr/bin/env python3
"""Validate a per-revision DAG and list downstream work invalidated by a change.
This is a planner, not a job scheduler or background agent.
"""
import argparse
import json
from pathlib import Path

def order(graph: dict) -> list[str]:
    if not isinstance(graph, dict) or not graph:
        raise ValueError('DAG must be a nonempty object of node -> dependency list')
    for node, deps in graph.items():
        if not isinstance(node, str) or not isinstance(deps, list) or any(not isinstance(x, str) for x in deps):
            raise ValueError('Invalid node or dependency list')
        if len(set(deps)) != len(deps) or any(d not in graph for d in deps):
            raise ValueError(f'Duplicate or unknown dependency for {node}')
    done = []
    while len(done) < len(graph):
        ready = [n for n, ds in graph.items() if n not in done and all(d in done for d in ds)]
        if not ready:
            raise ValueError('Dependency cycle: feedback belongs to the NEXT revision')
        done.extend(ready)
    return done

def affected(graph: dict, changed: list[str]) -> list[str]:
    sequence = order(graph)
    if not changed or any(n not in graph for n in changed):
        raise ValueError('Specify at least one existing changed node')
    dirty = set(changed)
    for n in sequence:
        if any(d in dirty for d in graph[n]): dirty.add(n)
    return [n for n in sequence if n in dirty]

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--graph',type=Path,default=Path(__file__).resolve().parents[1]/'assets/workflow.json')
    p.add_argument('--changed',nargs='+',help='Changed node IDs; report invalidated nodes')
    a=p.parse_args()
    try:
        g=json.loads(a.graph.read_text()); result=affected(g,a.changed) if a.changed else order(g)
        print(json.dumps({'mode':'invalidate' if a.changed else 'order','nodes':result},indent=2))
    except (ValueError,OSError) as e: p.exit(2,f'{e}\n')
if __name__=='__main__': main()
