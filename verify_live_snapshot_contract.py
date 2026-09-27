#!/usr/bin/env python3
"""Fail-closed verifier for an immutable Live Public Snapshot bundle."""
from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path
from urllib.request import urlopen

def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def get(url: str) -> bytes:
    with urlopen(url, timeout=30) as r:
        return r.read()

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--manifest-url', required=True)
    args = ap.parse_args()
    base = args.manifest_url.rsplit('/', 1)[0] + '/'
    try:
        raw = get(args.manifest_url)
        manifest = json.loads(raw.decode('utf-8-sig'))
        files, hashes = manifest.get('files', {}), manifest.get('hashes', {})
        required = ('daily_bridge','weekly_replace','index_daily_bridge','market_scan','sector_scan')
        failures, checks = [], []
        # Every declared digest is a contract.  The five required files are
        # checked even if a faulty manifest omitted them; all other declared
        # hashes are checked too.
        keys = list(dict.fromkeys([*required, *sorted(hashes)]))
        for key in keys:
            rel, expected = files.get(key), hashes.get(key)
            if not rel or not expected:
                failures.append({'key': key, 'reason': 'missing_file_or_hash'})
                continue
            actual = digest(get(base + rel))
            checks.append({'key': key, 'path': rel, 'expected_sha256': expected, 'actual_sha256': actual, 'match': actual == expected})
            if actual != expected:
                failures.append({'key': key, 'reason': 'sha256_mismatch'})
        result = {'result': 'PASS' if not failures else 'FAIL', 'snapshot_id': manifest.get('snapshot_id'), 'checks': checks, 'failures': failures}
    except Exception as exc:
        result = {'result':'FAIL', 'failures':[{'reason':'transport_or_parse_error','detail':str(exc)}]}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['result'] == 'PASS' else 2

if __name__ == '__main__':
    raise SystemExit(main())
