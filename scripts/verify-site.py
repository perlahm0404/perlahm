#!/usr/bin/env python3
"""Verify the static release locally and optionally through public HTTPS reads."""

import argparse
import concurrent.futures
import hashlib
import json
from pathlib import Path, PurePosixPath
import sys
from urllib.parse import quote, urlsplit
from urllib.request import urlopen


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", help="Public HTTPS site root; no cloud credentials used")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    site = root / "public_html"
    manifest = json.loads((root / "deployment/site-manifest.json").read_text())
    rows = manifest["files"]
    expected = {row["path"] for row in rows}
    errors = []
    if len(expected) != len(rows):
        errors.append("duplicate manifest paths")
    if manifest["file_count"] != len(rows):
        errors.append("manifest file count differs")
    if manifest["total_bytes"] != sum(row["bytes"] for row in rows):
        errors.append("manifest total bytes differs")
    actual = {str(path.relative_to(site)) for path in site.rglob("*") if path.is_file()}
    if actual != expected:
        errors.append("payload file set differs from manifest")
    for row in rows:
        rel = PurePosixPath(row["path"])
        if rel.is_absolute() or ".." in rel.parts:
            errors.append("unsafe manifest path")
            continue
        path = site / row["path"]
        if not path.is_file() or path.is_symlink():
            errors.append(f"missing or symbolic file: {row['path']}")
            continue
        body = path.read_bytes()
        if len(body) != row["bytes"] or hashlib.sha256(body).hexdigest() != row["sha256"]:
            errors.append(f"local integrity mismatch: {row['path']}")
    if args.url:
        url = urlsplit(args.url)
        if url.scheme != "https" or not url.hostname or url.username or url.password or url.query or url.fragment or url.path not in ("", "/"):
            parser.error("--url must be a public HTTPS site root without credentials, query or fragment")
        if not errors:
            def verify_public(row):
                try:
                    with urlopen(args.url.rstrip("/") + "/" + quote(row["path"], safe="/"), timeout=20) as response:
                        if urlsplit(response.geturl()).scheme != "https":
                            return f"non-HTTPS redirect: {row['path']}"
                        body = response.read()
                    if hashlib.sha256(body).hexdigest() != row["sha256"]:
                        return f"public integrity mismatch: {row['path']}"
                except Exception as exc:
                    return f"public read failed: {row['path']} ({type(exc).__name__})"
                return None

            with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
                errors.extend(error for error in pool.map(verify_public, rows) if error)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    mode = "local and public HTTPS" if args.url else "local"
    print(f"PASS: {len(rows)} files, {manifest['total_bytes']} bytes; {mode} checksums match")
    return 0


if __name__ == "__main__":
    sys.exit(main())
