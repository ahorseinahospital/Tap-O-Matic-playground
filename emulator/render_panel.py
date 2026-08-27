#!/usr/bin/env python3
"""
Render the module panel SVG to the PNG the emulator uses as its background.

Why a raster: browsers substitute fonts on SVG <text>, mangling the panel
labels. We rasterize once, up front, so the browser just shows a picture.

Why Inkscape and not rsvg-convert: the panel sets Fraunces' variable-font axes
(font-variation-settings: 'opsz' 144, 'wght' 100). librsvg ignores that property
outright, so labels come out at the default weight *and* the wider text-size
optical cut, and long ones collide. Inkscape draws exactly what the panel was
drawn in.

Pipeline:
  1. Inkscape exports the page onto a solid background (default black).
  2. Autocrop the uniform background border so 0%/100% == panel edges in the CSS.

Edit the panel SVG, then just re-run:  python3 emulator/render_panel.py

Requirements: Inkscape, python3, Pillow (PIL), plus the fonts the SVG asks for.
"""
from pathlib import Path
import shutil
import subprocess
import tempfile
from PIL import Image, ImageChops

# ---- Config (tweak freely) -------------------------------------------------
REPO         = Path(__file__).resolve().parent.parent
SRC_SVG      = REPO / "panel" / "foxtail" / "foxtail_panel_v1.1.1.svg"
DST_PNG      = REPO / "emulator" / "web" / "Foxtail.png"
BG_COLOR     = "#000000"     # background behind the panel (export color + trim)
RENDER_WIDTH = 2000          # output width in px before cropping (higher = sharper)
INKSCAPE     = "/Applications/Inkscape.app/Contents/MacOS/inkscape"
# ---------------------------------------------------------------------------


def inkscape_bin() -> str:
    exe = shutil.which("inkscape") or (INKSCAPE if Path(INKSCAPE).exists() else None)
    if not exe:
        raise SystemExit("Inkscape not found — install it or fix INKSCAPE above.")
    return exe


def hex_to_rgb(h: str):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def trim(im: Image.Image, color, tol: int = 8) -> Image.Image:
    """Crop away a border that is within `tol` of `color` (per channel)."""
    diff = ImageChops.difference(im, Image.new("RGB", im.size, color)).convert("L")
    bbox = diff.point(lambda p: 255 if p > tol else 0).getbbox()
    return im.crop(bbox) if bbox else im


def main():
    with tempfile.TemporaryDirectory() as td:
        out_png = Path(td) / "panel.png"
        subprocess.run(
            [inkscape_bin(), "--export-type=png",
             f"--export-filename={out_png}",
             f"--export-width={RENDER_WIDTH}",
             f"--export-background={BG_COLOR}",
             "--export-background-opacity=1",
             str(SRC_SVG)],
            check=True,
        )
        im = trim(Image.open(out_png).convert("RGB"), hex_to_rgb(BG_COLOR))

    DST_PNG.parent.mkdir(parents=True, exist_ok=True)
    im.save(DST_PNG)
    w, h = im.size
    print(f"wrote {DST_PNG.relative_to(REPO)}  ({w}x{h}, aspect {w/h:.4f})")
    print(f"  -> CSS:  aspect-ratio: {w} / {h};")


if __name__ == "__main__":
    main()