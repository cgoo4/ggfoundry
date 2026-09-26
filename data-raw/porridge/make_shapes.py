"""Original vector porridge symbols: paired outline and fill artwork.

All variants share one 200 x 200 canvas and bowl geometry.
Steam lives in the fill layer and shares the bowl's fill colour.
The generated source artwork is converted to Cairo SVG by rsvg-convert.
"""
from pathlib import Path
import argparse
import shutil
import subprocess
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--rsvg-convert", default=shutil.which("rsvg-convert"),
                    help="Path to the developer-only librsvg converter")
parser.add_argument("--output-dir", type=Path,
                    default=ROOT.parents[1] / "inst" / "extdata")
args = parser.parse_args()
if not args.rsvg_convert:
    parser.error("rsvg-convert is not on PATH; supply --rsvg-convert /path/to/rsvg-convert")
RAW = ROOT / "source-svg"
OUT = args.output_dir
RAW.mkdir(exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)

SILHOUETTE = """M 30 96
C 34 91 42 89 48 88 C 47 82 54 76 61 80
C 63 71 73 70 80 74 C 84 65 94 65 100 71
C 107 64 117 68 120 75 C 129 70 138 77 139 84
C 147 79 155 85 154 91 C 161 91 168 94 170 97
C 166 117 152 140 133 152 C 119 159 82 158 68 152
C 49 140 34 118 30 96 Z"""

PORRIDGE_WINDOW = """M 39 95
C 42 93 48 93 54 91 C 51 85 56 82 63 86
C 65 78 72 75 80 80 C 86 72 93 70 100 77
C 107 70 115 74 118 82 C 128 77 134 82 134 91
C 143 85 151 90 149 96 C 137 102 116 106 100 106
C 78 106 55 102 39 95 Z"""

BOWL_WINDOW = """M 39 104
C 54 111 77 115 100 115 C 122 115 147 111 161 105
C 156 122 143 138 130 147 C 117 153 84 153 71 147
C 56 138 44 121 39 104 Z"""

GRAINS = [
    "M 70 90 C 70 88 73 87 75 89 L 78 92 C 78 94 76 95 74 93 Z",
    "M 96 86 C 95 84 97 82 100 83 L 104 85 C 106 87 104 89 102 88 Z",
    "M 125 97 C 124 95 125 93 128 93 L 131 94 C 133 96 130 98 128 98 Z",
]

WISP = "M 97 60 C 79 47 108 39 96 23 C 118 37 92 47 102 57 C 105 61 101 64 97 60 Z"
STEAM = {"bowl2": [-23, 23], "bowl1": [0], "bowl0": []}

def path(d, colour="black", rule="nonzero", extra=""):
    return f'<path fill="{colour}" fill-rule="{rule}" d="{d}" {extra}/>'

def document(paths):
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" '
            'viewBox="0 0 200 200">\n' + "\n".join(paths) + '\n</svg>\n')

for name, offsets in STEAM.items():
    outline = [path(" ".join([SILHOUETTE, PORRIDGE_WINDOW, BOWL_WINDOW]), rule="evenodd")]
    outline += [path(d) for d in GRAINS]
    fill = [path(BOWL_WINDOW)]
    fill += [path(WISP, extra=f'transform="translate({dx}, 0)"') for dx in offsets]
    for layer, contents in [("col", outline), ("fill", fill)]:
        source = RAW / f"container-{name}_{layer}.svg"
        target = OUT / f"container-{name}_{layer}-cairo.svg"
        source.write_text(document(contents))
        subprocess.run([args.rsvg_convert, "--format=svg", "--output", str(target), str(source)], check=True)
        # Modern librsvg/Cairo omits the surface group on simple drawings.
        # Restore that neutral wrapper for grImport2's Cairo-format detector.
        namespace = "http://www.w3.org/2000/svg"
        ET.register_namespace("", namespace)
        tree = ET.parse(target)
        root = tree.getroot()
        surface = ET.Element(f"{{{namespace}}}g", {"id": "surface1"})
        for child in list(root):
            root.remove(child)
            surface.append(child)
        root.append(surface)
        ET.indent(tree, space="  ")
        tree.write(target, encoding="utf-8", xml_declaration=True)

print(f"Created {len(STEAM) * 2} Cairo SVG files in {OUT}")
