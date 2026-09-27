"""Original editable SVG candidates for ggfoundry: coffee and pumpkins.

No downloaded artwork, fonts, raster textures, or drawing dependencies.
The deliberately unequal Bezier curves and variable-width closed ribbons
give the outlines a loose ink-drawn feel. Every drawable element is a filled
path: ggfoundry recolours paths and draws its fill layer after its outline.
Interior marks are therefore also cut out of the fill geometry.

Run: python3 make_shapes.py
Requires rsvg-convert only to regenerate the supplied Cairo SVGs.
"""
from pathlib import Path
import os
import shutil
import subprocess
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
PKG = ROOT.parent.parent  # package checkout root: data-raw/coffee-autumn/
EXTDATA = PKG / "inst" / "extdata"
SVG_NS = "http://www.w3.org/2000/svg"


def path(d, colour="black", rule="nonzero"):
    return f'<path fill="{colour}" fill-rule="{rule}" d="{d}"/>'


def document(paths):
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" '
            'viewBox="0 0 200 200">\n' + "\n".join(paths) + '\n</svg>\n')


def ring(outer, inner):
    return (outer + " " + inner, "evenodd")


# Cup and saucer. The coffee opening and handle opening are transparent.
CUP_OUT = """M43 83 C53 79 65 78 80 78 C96 77 113 77 128 79
C137 79 143 80 147 84 C147 93 144 101 141 109
C137 121 131 133 118 139 C109 145 95 148 83 143
C67 142 57 132 52 119 C46 108 42 94 43 83 Z"""
CUP_IN = """M48 94 C59 97 66 98 79 99 C96 101 120 100 141 94
C139 105 135 113 132 121 C128 131 119 136 110 139
C100 143 90 142 81 139 C69 138 61 129 57 118
C52 109 50 101 48 94 Z"""
CUP_RIM = """M49 85 C60 81 72 82 84 81 C104 80 124 81 139 85
C137 88 129 91 121 92 C103 96 85 95 72 94
C61 92 54 91 49 88 Z"""
CUP_HANDLE_OUT = """M145 85 C155 80 169 83 175 91
C181 102 173 114 165 121 C157 128 146 128 136 125
L140 118 C151 120 158 118 164 112 C170 106 173 100 169 94
C165 89 155 89 146 93 Z"""
SAUCER = """M32 149 C42 144 54 143 65 142 L70 146
C57 147 46 148 39 151 C53 158 67 161 84 161
C99 163 116 163 132 160 C146 158 160 155 165 151
C157 147 143 147 132 147 L136 143
C150 143 170 145 174 151 C175 157 157 161 151 163
C130 170 106 170 84 167 C63 167 43 163 32 156
C28 154 28 151 32 149 Z"""
CUP_STEAM = """M89 66 C77 58 80 51 87 44 C92 38 92 34 88 28
C99 35 97 41 92 47 C86 53 83 57 91 63
C94 66 92 69 89 66 Z"""

# A generous rounded mug, with subtly uneven sides and two unequal wisps.
MUG_OUT = """M39 66 C44 61 61 61 77 60 C95 60 118 61 134 63
C142 63 144 67 143 77 C141 93 144 110 142 125
C142 139 143 150 135 157 C127 165 109 166 94 165
C79 166 60 164 51 160 C39 155 41 142 40 130
C39 117 41 102 39 90 C39 79 37 73 39 66 Z"""
MUG_IN = """M45 77 C57 80 68 80 81 81 C99 81 121 82 137 77
C136 91 139 107 137 120 C137 132 138 144 133 151
C128 158 112 161 96 160 C80 161 65 160 55 156
C46 153 47 142 46 130 C43 115 46 104 44 91
C44 84 45 80 45 77 Z"""
MUG_RIM = """M45 68 C60 65 73 64 90 65 C108 65 126 65 137 69
C130 74 116 75 100 76 C80 77 60 75 45 72 Z"""
MUG_HANDLE = """M143 79 C155 74 170 77 177 84 C184 93 179 111 172 122
C164 134 155 139 142 139 L143 132 C153 132 162 126 168 116
C174 107 176 95 172 89 C167 83 154 83 143 86 Z"""
MUG_STEAM_1 = """M72 49 C61 42 64 37 69 31 C73 26 72 21 69 17
C80 24 80 28 75 34 C70 40 67 43 74 47 C76 50 74 52 72 49 Z"""
MUG_STEAM_2 = """M106 50 C101 46 100 41 105 36 C110 30 112 25 108 21
C119 29 116 34 111 39 C107 43 105 46 109 49 C112 53 108 54 106 50 Z"""

# Takeaway cup: paper body and sleeve share the fill; lid stays open.
TAKE_OUT = """M52 68 C71 67 94 69 113 67 C127 67 139 68 148 67
C145 84 142 101 140 117 C137 133 134 149 131 164
C130 169 123 171 116 171 C99 173 83 171 73 170
C68 169 66 166 65 159 C63 144 61 130 59 114
C56 99 55 83 52 68 Z"""
TAKE_IN = """M58 73 C77 72 94 74 111 72 C123 72 136 73 141 72
C139 87 138 101 135 117 C132 133 129 149 126 162
C125 166 119 166 114 166 C100 168 82 166 73 165
C70 154 70 145 67 133 C65 121 64 109 62 99
C61 89 59 80 58 73 Z"""
LID_OUT = """M45 60 C50 58 53 58 56 58 L61 45
C62 41 68 41 75 42 C94 40 116 43 135 42
C140 42 142 43 144 48 L148 58 C153 58 156 61 155 67
C155 71 151 73 146 73 C126 73 103 75 83 73
C68 74 56 73 44 72 C40 70 41 63 45 60 Z"""
LID_IN = """M47 63 C55 62 58 63 61 58 L65 47
C84 45 101 47 118 47 C125 47 133 47 138 48 L143 62
C149 63 150 64 149 68 C136 68 124 68 110 69
C89 69 69 69 47 67 Z"""
LID_LINE = """M59 57 C77 55 100 58 119 56 C127 55 135 56 142 57
L143 61 C130 59 122 61 110 60 C92 62 73 60 58 61 Z"""
SLEEVE_TOP = """M64 99 C87 96 111 97 137 97 L136.5 100.5
C112 100 87 101 64.5 102 Z"""
SLEEVE_BASE = """M69 132 C89 135 110 134 133 132 L132.5 136
C111 138 91 139 69.5 136 Z"""

# Coffee bean: an irregular diagonal oval and a flowing off-centre crease.
BEAN_OUT = """M136 36 C148 38 157 47 161 60 C166 74 161 91 154 105
C148 118 136 131 125 142 C113 154 98 166 82 167
C67 169 54 162 46 151 C37 141 35 126 39 111
C42 96 52 80 63 67 C75 54 89 43 105 37
C117 33 127 32 136 36 Z"""
BEAN_IN = """M134 41 C145 42 152 51 156 61 C160 74 156 88 150 102
C144 115 132 127 122 138 C110 150 96 160 82 162
C69 164 58 158 50 148 C43 139 41 126 44 113
C47 98 56 84 67 71 C78 58 92 47 107 42
C118 38 126 38 134 41 Z"""
BEAN_CREASE = """M138 49 C136 66 127 79 113 91 C105 98 96 103 89 110
C80 119 75 132 65 149 C72 133 72 120 81 108
C88 98 98 94 108 86 C122 76 132 62 138 49 Z"""

# A shared asymmetric pumpkin body. Interior marks never overlap the fill.
PUMPKIN_OUT = """M100 57 C88 49 74 49 62 54 C48 50 36 59 30 73
C20 88 18 108 22 124 C26 144 40 164 60 162
C73 172 87 174 101 168 C116 173 130 169 140 162
C157 164 172 152 178 135 C185 116 182 97 175 81
C170 64 157 55 143 56 C129 48 113 50 100 57 Z"""
PUMPKIN_IN = """M100 63 C87 55 75 55 64 60 C51 56 41 63 35 77
C26 91 23 108 28 124 C31 142 43 158 62 157
C75 166 87 168 100 163 C113 167 129 164 139 157
C154 159 167 148 172 132 C179 115 176 98 169 84
C165 70 155 60 142 62 C128 55 115 56 100 63 Z"""
STEM = """M93 61 C97 51 99 42 93 33 C91 30 91 27 94 26
C100 26 107 28 113 31 C116 33 116 35 113 38
C108 44 107 53 108 61 L103 62 C101 53 102 42 107 35
C105 34 101 33 99 33 C103 41 103 51 99 61 Z"""
RIB_LEFT = """M58 65 C49 79 46 91 47 107 C46 126 49 139 58 151
C46 141 38 126 39 109 C38 93 46 75 58 65 Z"""
RIB_RIGHT = """M146 68 C158 82 163 96 162 112 C163 128 153 143 145 150
C152 136 154 124 153 110 C154 95 151 79 146 68 Z"""
RIB_MIDLEFT = """M84 63 C75 80 71 96 73 115 C71 134 76 149 85 160
C72 151 62 135 62 116 C62 95 72 76 84 63 Z"""
RIB_MIDRIGHT = """M115 63 C128 78 137 97 137 115 C137 135 128 150 117 160
C125 144 127 132 126 115 C126 97 124 80 115 63 Z"""
EYE_LEFT = """M63 105 C67 98 73 87 78 82 C82 89 87 99 90 108
C81 107 72 109 63 105 Z"""
EYE_RIGHT = """M111 108 C115 98 120 87 125 81 C130 86 137 97 141 103
C133 107 122 107 111 108 Z"""
NOSE = """M99 105 C102 109 105 113 106 117 C102 118 96 118 93 116
C95 112 96 109 99 105 Z"""
MOUTH = """M60 118 C66 122 70 124 76 125 L78 133 L86 134 L87 128
C94 130 102 130 109 128 L110 135 L119 132 L119 125
C128 123 135 121 141 116 C137 128 131 137 122 142
C115 148 106 151 98 150 C88 150 78 146 72 139
C66 133 63 127 60 118 Z"""
JACK_TOP_LEFT = """M83 64 C80 70 78 76 77 79 L80 79 C82 72 83 69 85 66 Z"""
JACK_TOP_RIGHT = """M115 65 C119 70 121 75 122 78 L125 78 C123 71 120 67 117 65 Z"""


def pumpkin(face=False):
    marks = [RIB_LEFT, RIB_RIGHT]
    marks += ([JACK_TOP_LEFT, JACK_TOP_RIGHT, EYE_LEFT, EYE_RIGHT, NOSE, MOUTH]
              if face else [RIB_MIDLEFT, RIB_MIDRIGHT])
    return ([ring(PUMPKIN_OUT, PUMPKIN_IN), (STEM, "nonzero")]
            + [(d, "nonzero") for d in marks],
            [(" ".join([PUMPKIN_IN] + marks), "evenodd")])


SHAPES = {
    "cup": ("container", [ring(CUP_OUT, CUP_IN + " " + CUP_RIM),
                           (CUP_HANDLE_OUT, "nonzero"), (SAUCER, "nonzero")],
             [(CUP_IN, "nonzero"), (CUP_STEAM, "nonzero")]),
    "mug": ("container", [ring(MUG_OUT, MUG_IN + " " + MUG_RIM),
                           (MUG_HANDLE, "nonzero")],
             [(MUG_IN, "nonzero"), (MUG_STEAM_1, "nonzero"), (MUG_STEAM_2, "nonzero")]),
    "takeaway": ("container", [ring(TAKE_OUT, TAKE_IN), ring(LID_OUT, LID_IN),
                                (LID_LINE, "nonzero"), (SLEEVE_TOP, "nonzero"),
                                (SLEEVE_BASE, "nonzero")],
                 [(" ".join([TAKE_IN, SLEEVE_TOP, SLEEVE_BASE]), "evenodd")]),
    "coffeebean": ("food", [ring(BEAN_OUT, BEAN_IN), (BEAN_CREASE, "nonzero")],
                   [(BEAN_IN + " " + BEAN_CREASE, "evenodd")]),
    "pumpkin": ("food", *pumpkin()),
    "jackolantern": ("food", *pumpkin(face=True)),
}

PREVIEW_FILL = {"cup": "#D9AC73", "mug": "#78A8A4", "takeaway": "#C58EAD",
                "coffeebean": "#AF815F", "pumpkin": "#E4A057", "jackolantern": "#E4A057"}


def convert(source, target, converter):
    subprocess.run([converter, "--format=svg", "--output", str(target), str(source)], check=True)
    # Keep the same neutral Cairo wrapper used by the bowl generator, for
    # grImport2's Cairo-format detector. No visible geometry is added.
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
    converter = os.environ.get("RSVG_CONVERT") or shutil.which("rsvg-convert")
    if not converter and Path("/opt/local/bin/rsvg-convert").is_file():
        converter = "/opt/local/bin/rsvg-convert"
    if not converter:
        raise SystemExit("rsvg-convert is needed for regeneration; the converted SVGs are already supplied.")
    for directory in ("source-svg", "preview-svg"):
        (ROOT / directory).mkdir(parents=True, exist_ok=True)
    EXTDATA.mkdir(parents=True, exist_ok=True)
    for name, (group, outlines, fills) in SHAPES.items():
        for layer, contents in (("col", outlines), ("fill", fills)):
            source = ROOT / "source-svg" / f"{group}-{name}_{layer}.svg"
            target = EXTDATA / f"{group}-{name}_{layer}-cairo.svg"
            source.write_text(document([path(d, rule=rule) for d, rule in contents]))
            convert(source, target, converter)
        composite = [path(d, "#33302D", rule) for d, rule in outlines]
        composite += [path(d, PREVIEW_FILL[name], rule) for d, rule in fills]
        (ROOT / "preview-svg" / f"{name}.svg").write_text(document(composite))
    print(f"Generated {len(SHAPES)} paired symbols (12 source SVGs + 12 Cairo SVGs).")


if __name__ == "__main__":
    main()
