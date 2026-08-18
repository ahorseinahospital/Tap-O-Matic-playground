#!/usr/bin/env bash
#
# Build both Fox Tail flavours and drop them in binaries/ under the version in
# version.txt:
#
#   binaries/Fox-Tail_v<version>.bin          stock
#   binaries/Fox-Tail_v<version>_quirks.bin   QUIRKS=1 (this unit's shift-pot detent)
#
# Version comes from version.txt so the manual and the panel can quote the same
# number; VERSION=0.9.1 ./release.sh overrides it for a one-off.
#
set -euo pipefail

cd "$(dirname "$0")"

VERSION="${VERSION:-$(tr -d ' \t\r\n' < version.txt)}"
[ -n "$VERSION" ] || { echo "release.sh: version.txt is empty" >&2; exit 1; }

OUT_DIR=binaries
mkdir -p "$OUT_DIR"

# The two builds differ only in a -D, and make cannot see that in a timestamp:
# without a clean the second build relinks the first one's objects. The trailing
# clean is the same guard for whatever is built next by hand.
build() {
    local out="$1"; shift
    make clean >/dev/null
    make MODULE=foxtail "$@"
    cp build/Fox-Tail.bin "$out"
    echo "  -> $out"
}

build "$OUT_DIR/Fox-Tail_v${VERSION}.bin"
build "$OUT_DIR/Fox-Tail_v${VERSION}_quirks.bin" QUIRKS=1
make clean >/dev/null

echo
ls -l "$OUT_DIR/Fox-Tail_v${VERSION}.bin" "$OUT_DIR/Fox-Tail_v${VERSION}_quirks.bin"
