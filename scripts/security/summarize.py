#!/usr/bin/env python3
"""Publish counts only; secret matches, source snippets and paths stay out of logs."""
import json
from pathlib import Path
import sys


def summarize(tool, report):
    """Reject malformed reports rather than reporting an unknown result as clean."""
    if tool == 'gitleaks':
        if not isinstance(report, list) or not all(isinstance(x, dict) and isinstance(x.get('RuleID'), str) for x in report):
            raise ValueError('invalid report')
        return {'scanner': tool, 'findings': len(report)}
    if tool != 'trivy' or not isinstance(report, dict) or report.get('SchemaVersion') != 2:
        raise ValueError('invalid report')
    results = report.get('Results', [])
    if not isinstance(results, list):
        raise ValueError('invalid results')
    counts = {'vulnerability': 0, 'secret': 0, 'misconfiguration': 0}
    for result in results:
        if not isinstance(result, dict):
            raise ValueError('invalid result')
        for field, kind in [('Vulnerabilities', 'vulnerability'), ('Secrets', 'secret'), ('Misconfigurations', 'misconfiguration')]:
            entries = result.get(field, [])
            if not isinstance(entries, list):
                raise ValueError('invalid entries')
            for entry in entries:
                if not isinstance(entry, dict) or entry.get('Severity') not in {'UNKNOWN', 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'}:
                    raise ValueError('invalid finding')
                if entry['Severity'] in {'HIGH', 'CRITICAL'}:
                    counts[kind] += 1
    return {'scanner': tool, 'findings': sum(counts.values()), 'counts': counts}


def main():
    """Only fixed diagnostic text is emitted when reading or parsing fails."""
    try:
        if len(sys.argv) != 3:
            raise ValueError('arguments')
        result = summarize(sys.argv[1], json.loads(Path(sys.argv[2]).read_text()))
        print(json.dumps(result, sort_keys=True))
        return 1 if result['findings'] else 0
    except (OSError, ValueError, TypeError, KeyError):
        print('Scanner report unavailable or invalid; result is unknown.', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
