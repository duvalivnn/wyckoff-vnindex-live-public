#!/usr/bin/env python3
"""Materialize an immutable snapshot from an already validated repository tree."""
from __future__ import annotations
import argparse, hashlib, json, shutil
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

TZ = ZoneInfo('Asia/Ho_Chi_Minh')

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''): h.update(b)
    return h.hexdigest()

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True)
    ap.add_argument('--snapshot-id', required=True)
    args = ap.parse_args()
    root, sid = Path(args.repo), args.snapshot_id
    source_manifest = json.loads((root/'manifest.json').read_text(encoding='utf-8'))
    dst = root/'snapshots'/sid
    if dst.exists(): raise SystemExit(f'REFUSE: snapshot already exists: {dst}')
    dst.mkdir(parents=True)
    # Every item named by the manifest is copied verbatim into the immutable bundle.
    for rel in source_manifest['files'].values():
        src, out = root/rel, dst/rel
        if not src.is_file(): raise SystemExit(f'MISSING: {rel}')
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, out)
    inner = dict(source_manifest)
    inner['snapshot_id'] = sid
    inner['snapshot_mode'] = 'IMMUTABLE_VERSIONED_BUNDLE'
    inner['published_at'] = datetime.now(TZ).isoformat(timespec='seconds')
    inner['publication_contract'] = 'PUBLISH_ALL_FILES_AND_ROOT_MANIFEST_IN_ONE_GIT_COMMIT'
    inner['hashes'] = {key: sha256(dst/rel) for key,rel in inner['files'].items() if (dst/rel).is_file()}
    (dst/'manifest.json').write_text(json.dumps(inner,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    outer = dict(inner)
    outer['snapshot_manifest'] = f'snapshots/{sid}/manifest.json'
    outer['files'] = {key:f'snapshots/{sid}/{rel}' for key,rel in inner['files'].items()}
    # Digests remain associated with the bytes in the immutable inner bundle.
    (root/'manifest.json').write_text(json.dumps(outer,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'snapshot_id':sid,'assets':len(inner['files']),'immutable_manifest':str(dst/'manifest.json')},ensure_ascii=False))
    return 0

if __name__ == '__main__': raise SystemExit(main())
