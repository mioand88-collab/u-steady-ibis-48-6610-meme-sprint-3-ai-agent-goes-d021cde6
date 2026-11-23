#!/usr/bin/env python3
"""Meme Sprint 3: AI Agent Goes Rogue.

Copies the meme image shipped in this repository (entry.png) to
/output/entry.png byte-for-byte, so the judge sees exactly the picture
drawn in this session. Standard library only, no network, deterministic.

The output directory is created when missing and is never deleted or
emptied by this program. If source and destination resolve to the same
file, the copy is skipped. After copying, the destination is verified
against the source by size and SHA-256 so a truncated write cannot
silently pass.
"""
import hashlib
import os
import shutil
import sys

SOURCE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "entry.png")
OUTPUT_DIR = "/output"
DEST = os.path.join(OUTPUT_DIR, "entry.png")


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    if not os.path.isfile(SOURCE):
        print("error: source image not found: %s" % SOURCE, file=sys.stderr)
        return 1
    # Create /output when missing; never remove or empty it.
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    # Same-file guard, resolving symlinks so an aliased path is caught too.
    if os.path.realpath(SOURCE) == os.path.realpath(DEST):
        return 0
    shutil.copyfile(SOURCE, DEST)
    # Verify the copy is byte-for-byte identical to the source.
    if os.path.getsize(SOURCE) != os.path.getsize(DEST):
        print("error: size mismatch after copy", file=sys.stderr)
        return 1
    if sha256_of(SOURCE) != sha256_of(DEST):
        print("error: checksum mismatch after copy", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
