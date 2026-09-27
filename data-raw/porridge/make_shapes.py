"""Generate the loose, ink-style bowl0/1/2 replacement assets for ggfoundry.

All three symbols share one bowl, rim, porridge mound and 200 x 200 canvas.
The only variant is zero, one or two steam wisps, drawn with the fill colour.
The body, rim and small foot use one compound fill path, so the fill SVGs
retain the original one-body-path plus 0/1/2-steam-path structure.
"""
from pathlib import Path
import argparse
import shutil
import subprocess
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
SVG_NS = "http://www.w3.org/2000/svg"

# A lopsided mound: small ledges, unequal lumps and a peak left of centre.
# The interior remains transparent, as in the existing bowl symbols.
PORRIDGE_OUT = """M37 96 C36 91 39 86 43 86
C45 83 49 86 51 84 C52 80 56 79 60 80
C59 76 60 72 64 72 C68 73 70 71 72 68
C68 62 69 58 74 58 C79 61 82 58 85 55
C89 56 92 53 96 54 C103 49 107 52 108 58
C113 55 119 57 120 62 C127 61 129 66 129 71
C136 70 140 73 137 78 C142 76 147 75 148 79
C152 77 155 81 154 86 C160 83 166 86 163 92
C168 89 172 91 171 96 C149 101 115 103 91 103
C70 106 50 104 37 96 Z"""

PORRIDGE_IN = """M41 96 C39 91 42 88 46 90
C47 89 50 90 54 88 C54 84 57 82 63 84
C63 80 62 77 65 76 C70 76 73 73 76 70
C78 68 73 63 75 62 C80 65 85 61 88 59
C90 60 94 57 98 58 C103 54 105 56 105 63
C110 65 114 59 117 64 C118 67 122 65 125 69
C128 72 124 75 130 75 C134 74 136 75 133 80
C133 85 143 79 145 82 C145 85 150 81 151 84
C153 89 147 91 154 91 C159 87 163 89 160 93
C158 98 166 93 168 95 C150 98 128 98 108 99
C83 101 61 100 41 96 Z"""

# The outline and inset are intentionally different curves, creating a
# variable ink width and a gently uneven silhouette without raster noise.
BOWL_OUT = """M36 100 C56 98 76 100 94 99
C114 98 136 96 163 96 C163 110 160 123 158 131
C154 143 152 149 147 152 C137 157 120 161 101 161
C88 162 72 160 61 155 C49 150 45 142 41 132
C36 121 35 110 36 100 Z"""

BOWL_IN = """M41 105 C59 106 78 104 96 104
C116 103 138 101 158 101 C157 111 156 122 152 132
C150 141 147 147 143 149 C131 153 117 157 102 156
C88 158 73 155 64 152 C53 147 49 139 46 130
C42 120 41 112 41 105 Z"""

# A small flared foot, like the bowl in the supplied visual reference.
FOOT_OUT = """M76 157 C91 159 113 159 126 156
C129 161 131 167 134 172 C119 175 87 175 70 172
C71 166 72 161 76 157 Z"""
FOOT_IN = """M79 162 C93 164 109 163 123 161
C125 164 126 168 127 169 C113 171 91 171 77 169
C77 166 78 164 79 162 Z"""

# A broad, slightly tilted rim with a wavering front and unequal ends.
RIM_OUT = """M27 98 C26 95 37 94 46 94
C62 94 80 92 96 93 C115 92 135 91 152 91
C165 90 174 91 175 94 C176 98 164 99 154 100
C139 100 120 102 104 102 C86 104 70 103 51 104
C37 104 25 104 27 98 Z"""
RIM_IN = """M34 98 C45 97 59 97 70 96
C85 95 101 97 116 95 C134 94 154 94 168 94
C161 96 148 96 135 97 C115 99 101 98 87 100
C67 100 49 101 34 100 Z"""

# Loose porridge marks instead of evenly spaced dots or identical scallops.
GRAINS = [
    """M56 88 C61 83 65 83 70 86 C74 88 79 87 83 86
    C80 91 74 91 69 89 C63 86 60 88 56 88 Z""",
    """M82 75 C86 69 89 71 92 67 C95 64 98 65 100 63
    C100 68 95 68 93 71 C89 75 86 73 82 75 Z""",
    """M94 80 C94 74 98 73 100 76 C103 79 101 82 106 85
    C108 87 111 88 113 88 C110 91 105 88 102 86
    C97 82 100 78 97 78 L94 80 Z""",
    """M120 78 C125 77 128 80 127 84 C129 87 133 86 138 83
    C137 88 130 90 126 87 C122 85 125 81 120 80 Z""",
    """M145 91 C148 88 151 89 154 89 C152 91 149 92 145 91 Z""",
]

# Two related but unequal wisps. One-wisp artwork is centred on the canvas.
WISP_CENTRE = """M98 43 C88 38 87 32 94 26 C99 21 100 16 96 12
C107 17 107 24 101 29 C95 34 94 38 100 41
C104 45 101 47 98 43 Z"""
WISP_LEFT = """M73 46 C63 40 65 33 70 29 C77 23 75 19 72 16
C84 22 81 29 77 33 C72 38 69 40 76 45
C80 49 76 50 73 46 Z"""
WISP_RIGHT = """M122 45 C117 41 115 36 121 31 C126 26 128 20 123 16
C135 22 133 29 128 34 C123 38 121 42 125 44
C128 47 124 49 122 45 Z"""
STEAM = {"bowl2": [WISP_LEFT, WISP_RIGHT], "bowl1": [WISP_CENTRE], "bowl0": []}


def path(d, colour="black", rule="nonzero"):
    return f'<path fill="{colour}" fill-rule="{rule}" d="{d}"/>'


def document(paths):
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" '
            'viewBox="0 0 200 200">\n' + "\n".join(paths) + '\n</svg>\n')


def outline_paths(colour="black"):
    # Foot behind body, mound behind lip. The same order is used in previews.
    return [path(FOOT_OUT + " " + FOOT_IN, colour, "evenodd"),
            path(BOWL_OUT + " " + BOWL_IN, colour, "evenodd"),
            path(PORRIDGE_OUT + " " + PORRIDGE_IN, colour, "evenodd"),
            path(RIM_OUT + " " + RIM_IN, colour, "evenodd")] + [path(g, colour) for g in GRAINS]


def fill_paths(wisps, colour="black"):
    return [path(" ".join([BOWL_IN, RIM_IN, FOOT_IN]), colour)] + [path(w, colour) for w in wisps]


def convert(source, target, converter):
    subprocess.run([converter, "--format=svg", "--output", str(target), str(source)], check=True)
    # grImport2 recognises the same neutral Cairo wrapper used by the current
    # bowl assets. This changes no visible geometry.
    ET.register_namespace("", SVG_NS)
    tree = ET.parse(target)
    root = tree.getroot()
    children = list(root)
    if not (len(children) == 1 and children[0].get("id", "").startswith("surface")):
        surface = ET.Element(f"{{{SVG_NS}}}g", {"id": "surface1"})
        for child in children:
            root.remove(child)
            surface.append(child)
        root.append(surface)
    ET.indent(tree, space="  ")
    tree.write(target, encoding="utf-8", xml_declaration=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rsvg-convert", default=shutil.which("rsvg-convert"),
                        help="Path to the developer-only librsvg converter")
    parser.add_argument("--output-dir", type=Path,
                        default=ROOT.parents[1] / "inst" / "extdata")
    parser.add_argument("--preview-dir", type=Path,
                        help="Optionally write standalone coloured preview SVGs")
    args = parser.parse_args()
    if not args.rsvg_convert:
        parser.error("rsvg-convert is not on PATH; supply --rsvg-convert /path/to/rsvg-convert")
    raw = ROOT / "source-svg"
    raw.mkdir(exist_ok=True)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    if args.preview_dir:
        args.preview_dir.mkdir(parents=True, exist_ok=True)
    for name, wisps in STEAM.items():
        for layer, contents in (("col", outline_paths()), ("fill", fill_paths(wisps))):
            source = raw / f"container-{name}_{layer}.svg"
            target = args.output_dir / f"container-{name}_{layer}-cairo.svg"
            source.write_text(document(contents))
            convert(source, target, args.rsvg_convert)
        if args.preview_dir:
            artwork = outline_paths("#33302D") + fill_paths(wisps, "#177E9F")
            (args.preview_dir / f"{name}.svg").write_text(document(artwork))
    print(f"Created six replacement Cairo SVGs in {args.output_dir}")


if __name__ == "__main__":
    main()
