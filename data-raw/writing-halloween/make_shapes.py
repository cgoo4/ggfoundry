"""Original ink-style writing and Halloween shapes for ggfoundry.

All visible elements are closed filled paths. Deliberately unequal curves
and variable-width ribbons give a drawn appearance without raster noise.
Outline and fill share a 200 x 200 canvas; fills never paint over details.
Python standard library + rsvg-convert are needed only for regeneration.
"""
from pathlib import Path
import argparse
import math
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
PKG = ROOT.parent.parent
NS = "http://www.w3.org/2000/svg"


def fmt(n):
    return f"{n:.3f}".rstrip("0").rstrip(".")


def curve(points, close=False):
    """Catmull-Rom to cubic Beziers through individually placed points."""
    p = list(points)
    result = [f"M{fmt(p[0][0])} {fmt(p[0][1])}"]
    count = len(p) if close else len(p) - 1
    for i in range(count):
        a = p[(i - 1) % len(p)] if close or i else p[0]
        b = p[i]
        c = p[(i + 1) % len(p)]
        d = p[(i + 2) % len(p)] if close or i + 2 < len(p) else p[-1]
        q = (b[0] + (c[0] - a[0]) / 6, b[1] + (c[1] - a[1]) / 6,
             c[0] - (d[0] - b[0]) / 6, c[1] - (d[1] - b[1]) / 6,
             c[0], c[1])
        result.append("C" + " ".join(fmt(x) for x in q))
    if close:
        result.append("Z")
    return " ".join(result)


def ribbon(points, width=2.6, taper=False):
    """A filled, wavering ink stroke with unequal width and rounded ends."""
    left, right = [], []
    for i, b in enumerate(points):
        a, c = points[max(i - 1, 0)], points[min(i + 1, len(points) - 1)]
        dx, dy = c[0] - a[0], c[1] - a[1]
        length = math.hypot(dx, dy)
        w = width * (0.46 + 0.08 * math.sin(i * 1.9 + 0.7))
        if taper and i in (0, len(points) - 1):
            w *= 0.28
        left.append((b[0] - dy / length * w, b[1] + dx / length * w))
        right.append((b[0] + dy / length * w, b[1] - dx / length * w))
    return curve(left + right[::-1], close=True)


def blob(cx, cy, rx, ry, phase=0):
    return curve([(cx + rx * (1 + 0.055 * math.sin(i * 2.2 + phase)) * math.cos(i * math.pi / 4),
                   cy + ry * (1 + 0.075 * math.sin(i * 1.7 + phase)) * math.sin(i * math.pi / 4))
                  for i in range(8)], close=True)


def rotated(d, angle=-29):
    # Every path here uses absolute M/L/C coordinates, so pairs can be rotated.
    c, s = math.cos(math.radians(angle)), math.sin(math.radians(angle))
    tokens = re.findall(r"[MLCZ]|-?\d+(?:\.\d+)?", d)
    result, i = [], 0
    while i < len(tokens):
        if tokens[i] in "MLCZ":
            result.append(tokens[i]); i += 1
        else:
            x, y = float(tokens[i]) - 100, float(tokens[i + 1]) - 100
            result.extend((fmt(100 + c * x - s * y), fmt(100 + s * x + c * y)))
            i += 2
    return " ".join(result)


def shape():
    return {"col": [], "fill": []}


def shell(s, outer, inner, marks=()):
    s["col"].append((outer + " " + inner, "evenodd"))
    s["col"].extend((m, "nonzero") for m in marks)
    s["fill"].append((" ".join([inner, *marks]), "evenodd"))


def ink(s, *marks):
    s["col"].extend((m, "nonzero") for m in marks)


def thread(s, points, width=3):
    outside, inside = ribbon(points, width), ribbon(points, width * 0.38)
    shell(s, outside, inside)


SHAPES = {}

# Front-facing clothbound book: uneven cover, soft spine and blank title label.
s = shape()
outer = "M48 34 C74 31 105 34 135 30 C143 29 151 33 151 42 L153 158 C154 168 146 174 136 174 C106 176 76 173 48 175 C39 174 35 168 35 160 L34 48 C34 40 40 35 48 34 Z"
inner = "M53 40 C77 37 104 40 134 36 C141 35 145 38 145 45 L147 157 C148 163 144 167 136 168 C108 170 82 167 54 169 C52 144 54 122 52 96 C52 75 52 57 53 40 Z"
marks = [ribbon([(66,53),(94,51),(121,52),(133,50)],2.2),
         ribbon([(67,150),(92,152),(117,150),(134,151)],2.2)]
shell(s, outer, inner, marks)
ink(s, ribbon([(46,42),(44,70),(46,97),(45,132),(46,162)],2.7),
    ribbon([(40,158),(41,165),(46,169)],2.3),
    ribbon([(55,177),(80,178),(108,177),(141,178)],2.8))
# Label is a transparent inset bounded by a variable-width frame.
label_out = "M70 72 C84 70 110 72 129 70 L130 109 C114 111 89 108 70 110 Z"
label_in = "M74 76 C89 74 109 76 125 74 L126 105 C109 107 92 104 74 106 Z"
label = label_out + " " + label_in
# Cut label frame out of body fill; the label paper keeps the mapped fill.
s["col"].append((label,"evenodd"))
s["fill"][0] = (" ".join([inner,*marks,label_out,label_in]),"evenodd")
ink(s, ribbon([(84,88),(97,87),(117,88)],2.0),
    ribbon([(88,96),(101,97),(113,96)],1.7))
s["fill"][0] = (s["fill"][0][0] + " " + s["col"][-2][0] + " " + s["col"][-1][0],"evenodd")
SHAPES["bookfront"] = ("writing",s)

# Open book: unequal page fans, a deep gutter and loose lines of writing.
s = shape()
left_out = "M98 58 C77 42 50 41 27 46 L23 145 C45 137 72 144 98 160 C100 130 100 91 98 58 Z"
left_in = "M93 61 C76 48 51 47 32 51 L29 137 C51 133 71 140 93 151 C95 124 95 87 93 61 Z"
right_out = "M101 59 C123 43 150 43 176 50 L179 149 C152 139 128 147 102 161 C101 131 103 91 101 59 Z"
right_in = "M107 61 C127 49 148 49 171 55 L173 140 C151 134 131 141 107 152 C106 125 109 91 107 61 Z"
left_marks = [ribbon([(41,y),(55,y-1),(70,y+2),(83,y+7)],2.0,taper=True) for y in (70,85,101,118)]
right_marks = [ribbon([(118,y+5),(132,y),(148,y-2),(161,y)],2.0,taper=True) for y in (71,88,104,121)]
shell(s,left_out,left_in,left_marks); shell(s,right_out,right_in,right_marks)
ink(s, ribbon([(23,153),(44,149),(69,155),(94,168),(101,169),(128,157),(155,149),(179,156)],3.5),
    ribbon([(100,64),(99,97),(100,128),(100,160)],2.0))
SHAPES["bookopen"] = ("writing",s)

# Fountain nib: sculpted shoulders, breather hole, long slit and two engravings.
s = shape()
outer = "M61 37 C84 44 111 45 135 35 C138 61 143 89 149 112 C143 132 120 157 98 178 C79 158 59 139 52 115 C56 91 60 65 61 37 Z"
inner = "M66 44 C86 51 108 50 130 43 C133 67 137 91 143 112 C136 131 116 153 98 170 C81 152 64 135 58 114 C62 91 65 67 66 44 Z"
hole = blob(99,91,6.3,6.8,1)
slit = ribbon([(99,98),(100,119),(98,139),(98,158)],2.8)
marks = [hole,slit,ribbon([(73,65),(77,91),(69,111),(81,130)],2.0,taper=True),
         ribbon([(123,65),(120,89),(131,110),(117,131)],2.0,taper=True)]
shell(s,outer,inner,marks)
SHAPES["nib"] = ("writing",s)

# Full fountain pen, with the cap posted and an exposed nib; diagonal stance.
s = shape()
shell(s,"M87 64 C85 87 88 116 88 137 C87 144 94 148 101 146 C110 149 114 143 113 136 C112 110 114 89 112 64 Z",
      "M92 69 C91 91 93 112 93 137 C93 141 98 142 102 141 C107 142 108 139 108 134 L107 69 Z",
      [ribbon([(96,82),(95,103),(97,127)],1.7,taper=True)])
shell(s,"M88 22 C95 18 108 20 113 24 L115 74 C108 79 94 78 85 74 L86 29 C85 26 86 24 88 22 Z",
      "M91 27 C96 24 104 25 108 28 L110 70 C104 73 95 72 90 70 Z",
      [ribbon([(106,33),(105,49),(106,65)],2.8)])
ink(s,ribbon([(88,78),(102,80),(113,78)],3.3),ribbon([(90,136),(101,137),(112,136)],3.0))
shell(s,"M91 146 C96 149 106 149 111 146 L112 159 C109 168 105 176 101 183 C95 177 90 168 87 160 Z",
      "M94 152 C99 154 105 153 108 152 L108 158 C106 165 103 172 101 177 C97 171 93 166 92 159 Z",
      [blob(101,160,2,2.7),ribbon([(101,163),(101,168),(101,173)],1.3)])
for layer in s:
    s[layer] = [(rotated(d),rule) for d,rule in s[layer]]
SHAPES["fountainpen"] = ("writing",s)

# Inkpot: octagonal shoulders, squat glass reservoir and a resting stopper.
s = shape()
outer = "M64 72 C79 68 115 70 135 72 L153 91 C155 112 153 141 154 157 C152 166 140 170 127 170 L71 169 C59 168 47 165 47 156 L48 96 C49 86 57 81 64 72 Z"
inner = "M66 78 C85 75 112 76 133 78 L147 94 C149 113 147 140 148 156 C145 163 134 164 123 164 L72 163 C62 162 54 160 53 155 L54 98 C56 90 62 84 66 78 Z"
marks = [ribbon([(61,104),(65,129),(63,149)],2.2,taper=True),
         ribbon([(73,151),(97,153),(125,151),(138,153)],2.5),
         ribbon([(66,96),(91,99),(116,97),(139,99)],2.6)]
shell(s,outer,inner,marks)
shell(s,"M69 54 C85 51 114 53 131 52 L135 72 C119 77 85 76 65 72 Z",
      "M74 59 C88 56 112 58 127 57 L129 68 C112 71 88 70 72 68 Z")
shell(s,"M78 36 C91 32 108 33 120 36 L124 51 C110 56 87 55 75 51 Z",
      "M81 40 C93 37 108 38 117 40 L119 48 C108 51 91 50 80 48 Z")
ink(s,ribbon([(55,156),(61,161),(70,162)],2.0))
SHAPES["inkpot"] = ("writing",s)

# Quill: a long taper, unequal barbs and ink laid down at (44,166).
s = shape()
outer = "M169 22 C173 34 168 47 160 59 L154 63 L154 69 C148 82 143 94 133 103 L126 106 L127 111 C117 121 103 128 91 130 L84 129 L78 136 L65 141 C57 129 57 116 60 106 L66 96 L64 93 C67 79 75 69 84 60 L91 58 L91 53 C105 42 119 33 136 29 L143 30 L149 26 C157 24 163 23 169 22 Z"
inner = "M165 29 C167 37 163 46 156 54 L148 60 L149 66 C142 81 138 91 129 99 L120 103 L120 108 C109 117 98 123 88 124 L81 125 L75 131 L67 135 C62 124 63 116 65 109 L73 97 L71 93 C73 83 79 75 89 66 L97 61 L97 56 C110 46 124 38 137 35 L145 35 L152 31 Z"
marks = [ribbon([(78,87),(88,87),(103,90)],2.0,taper=True),
         ribbon([(89,70),(102,70),(119,74)],2.0,taper=True),
         ribbon([(111,51),(123,54),(135,58)],1.8,taper=True),
         ribbon([(118,83),(134,77),(143,69)],2.0,taper=True),
         ribbon([(103,102),(117,95),(129,87)],2.0,taper=True),
         ribbon([(83,119),(96,111),(105,103)],1.8,taper=True)]
shell(s,outer,inner,marks)
ink(s,ribbon([(44,166),(62,143),(79,121),(101,95),(122,72),(143,48),(161,31)],3.7,taper=True),
    blob(44,166,4.5,2.8,2),
    ribbon([(44,167),(56,171),(70,169),(80,163),(90,161),(98,164)],3.3,taper=True),
    blob(33,175,1.7,1.2,3))
# Shaft is removed from the feather fill wherever it runs within the inset.
# The section inside the feather is separate to avoid an even-odd island outside it.
shaft_inner = ribbon([(70,132),(79,121),(101,95),(122,72),(143,48),(156,34)],3.7,taper=True)
s["fill"][0] = (" ".join([inner,*marks,shaft_inner]),"evenodd")
SHAPES["quill"] = ("writing",s)

# Skeleton: large skull and sparse ribs keep the little figure legible.
s = shape()
outer = "M79 29 C88 23 107 23 120 28 C130 34 131 48 126 57 L120 62 L119 70 C107 75 89 74 78 69 L78 62 C68 58 67 48 70 40 C70 35 74 31 79 29 Z"
inner = "M82 34 C91 28 106 29 117 33 C125 37 125 47 121 53 L115 59 L114 66 C104 70 92 69 83 65 L83 58 C75 55 73 48 75 41 C76 38 78 36 82 34 Z"
marks = [blob(85,47,5.4,6.1,1),blob(113,47,5,5.6,3),
         "M98 49 C95 53 94 57 97 59 C100 60 104 58 103 55 L101 49 Z",
         ribbon([(92,61),(93,67)],1.8),ribbon([(103,62),(103,68)],1.8)]
shell(s,outer,inner,marks)
thread(s,[(99,75),(100,88),(99,103),(100,117)],5.0)
for pts in ([(95,84),(85,80),(75,83),(79,91),(95,94)],
            [(106,84),(116,81),(127,86),(121,92),(106,95)],
            [(94,98),(81,94),(78,101),(93,106)],
            [(107,98),(120,95),(123,102),(108,107)],
            [(94,110),(85,107),(84,113),(95,118)],
            [(107,110),(116,108),(117,114),(106,119)]):
    thread(s,pts,4.7)
shell(s,"M78 119 C84 117 93 120 100 123 C108 119 118 117 124 122 L119 137 C111 141 106 138 101 132 C96 140 84 141 79 136 Z",
      "M83 124 C89 123 96 126 100 128 C108 124 113 122 118 125 L115 133 C109 135 104 130 101 128 C96 134 89 136 84 132 Z")
for pts in ([(74,81),(62,89),(54,106)],[(52,111),(47,126),(54,138)],
            [(127,86),(142,96),(149,111)],[(150,115),(143,127),(133,134)],
            [(87,142),(78,153),(81,163)],[(81,166),(85,177),(78,184)],
            [(114,143),(121,154),(119,164)],[(119,168),(113,178),(116,184)]):
    thread(s,pts,7.8)
ink(s,ribbon([(55,139),(60,143),(58,148)],2.2),ribbon([(55,140),(51,147),(54,149)],2.2),
    ribbon([(131,135),(125,138),(127,143)],2.2),ribbon([(131,136),(133,142),(130,146)],2.2),
    ribbon([(78,184),(72,185),(67,183)],4),ribbon([(117,184),(124,185),(129,183)],4))
SHAPES["skeleton"] = ("halloween",s)

# Ghost: windblown sheet, uneven hem and deliberately unequal features.
s = shape()
outer = "M68 43 C78 27 97 24 115 30 C134 36 143 52 144 69 C145 89 156 103 168 112 C173 117 170 124 164 124 L150 117 C156 137 150 153 161 172 C145 176 136 158 126 159 C119 161 120 176 109 179 C96 180 95 163 83 164 C74 165 72 180 61 175 C50 173 50 157 41 161 L30 169 C28 155 35 140 40 126 L45 112 C34 120 28 118 29 112 C35 100 46 99 53 87 C57 74 57 55 68 43 Z"
inner = "M73 46 C82 33 99 30 113 35 C130 40 136 53 138 70 C139 91 151 106 163 116 C155 111 149 110 144 110 C144 134 146 149 152 165 C139 163 133 151 124 154 C114 157 115 171 107 173 C99 171 98 158 83 158 C72 157 69 173 63 169 C56 164 56 152 47 154 L38 159 C38 151 43 136 47 126 L53 104 C46 106 40 110 35 112 C45 106 53 98 58 89 C63 74 63 57 73 46 Z"
marks = [blob(83,68,5.2,7.2,1),blob(114,66,5,6.2,3),blob(98,91,7.1,9.6,2),
         ribbon([(69,129),(65,142),(66,150)],2.0,taper=True),
         ribbon([(126,121),(133,136),(135,146)],2.0,taper=True)]
shell(s,outer,inner,marks)
SHAPES["ghost"] = ("halloween",s)

# Web: hand-placed skew spokes and sagging, non-concentric thread segments.
s = shape()
centre = (103,93)
tips = [(100,19),(152,34),(181,89),(167,149),(107,183),(45,158),(20,99),(44,39)]
for i,(tx,ty) in enumerate(tips):
    thread(s,[centre,(103+(tx-103)*.34+(-1)**i*2,93+(ty-93)*.34-1),
              (103+(tx-103)*.68+(-1)**i*1.6,93+(ty-93)*.68+1.5),(tx,ty)],2.8)
for r in (.25,.49,.73,.94):
    nodes = [(103+(x-103)*r,93+(y-93)*r) for x,y in tips]
    for i,a in enumerate(nodes):
        b = nodes[(i+1)%8]
        mid = ((a[0]+b[0])*.5,(a[1]+b[1])*.5)
        sag = ((103-mid[0])*.13,(93-mid[1])*.13)
        thread(s,[a,(mid[0]+sag[0]+math.sin(i*2+r),mid[1]+sag[1]+math.cos(i+r)),b],2.4)
SHAPES["spiderweb"] = ("halloween",s)

# Reaper: crooked hood, robe folds, skeletal hand and a sweeping scythe.
s = shape()
outer = "M77 35 C87 24 105 27 115 38 C123 49 123 59 121 72 C129 76 136 83 143 96 L134 111 L124 104 C123 128 129 157 136 180 C121 184 109 178 96 182 C81 186 64 177 48 182 C51 161 56 139 57 113 L43 123 L34 108 C45 90 57 79 69 74 C66 57 67 46 77 35 Z"
inner = "M82 39 C90 30 103 33 110 42 C117 51 117 62 115 76 C126 80 133 88 136 96 L131 103 L119 97 C117 125 123 156 128 174 C116 176 108 172 95 176 C82 180 69 172 55 176 C59 155 63 131 64 105 L46 115 L42 108 C50 94 61 84 75 79 C73 61 73 48 82 39 Z"
face = "M84 46 C92 41 105 43 110 51 C109 61 103 68 97 73 C89 69 82 60 80 55 Z"
marks = [face,ribbon([(83,91),(77,116),(71,141),(68,164)],2.6,taper=True),
         ribbon([(103,91),(105,118),(115,150),(119,166)],2.6,taper=True),
         ribbon([(88,131),(85,151),(92,167)],2.2,taper=True),
         ribbon([(60,95),(51,104),(48,109)],2.0,taper=True)]
shell(s,outer,inner,marks)
# Cut two little glints out of the shadow, using vector holes rather than white.
eyes = [blob(89,54,2.4,1.9,1),blob(103,54,2.3,1.8,2)]
s["col"][1] = (" ".join([face,*eyes]),"evenodd")
s["fill"][0] = (" ".join([inner,*marks]),"evenodd")
thread(s,[(157,44),(156,75),(160,111),(159,145),(164,180)],7.0)
shell(s,"M159 47 C145 28 123 22 88 24 C112 10 143 13 159 25 C170 33 173 45 171 59 L165 70 C165 59 163 52 159 47 Z",
      "M162 43 C148 26 135 24 110 21 C128 17 145 21 154 29 C163 35 167 43 167 51 C166 48 165 45 162 43 Z")
ink(s,ribbon([(132,98),(143,96),(155,97)],4.3),
    ribbon([(141,94),(143,104),(151,106)],2.4),ribbon([(146,94),(148,103),(155,104)],2.4))
SHAPES["grimreaper"] = ("halloween",s)

# Gravestone: lopsided arch, fine crack, hand-lettered RIP and tufted grass.
s = shape()
outer = "M50 169 L49 73 C48 52 65 34 86 30 C110 24 136 34 147 51 C153 61 153 72 151 86 L153 169 C122 173 86 168 50 169 Z"
inner = "M56 163 L55 75 C53 57 68 40 88 36 C109 31 130 39 141 54 C148 64 147 77 146 87 L147 163 C120 167 91 161 56 163 Z"
r_letter = ribbon([(70,102),(70,84),(80,83),(86,89),(82,95),(71,95),(85,107)],2.8)
i_letter = ribbon([(94,84),(103,84)],2.7) + " " + ribbon([(99,86),(98,104)],2.9) + " " + ribbon([(94,106),(104,106)],2.7)
p_letter = ribbon([(116,107),(116,85),(127,84),(132,90),(128,96),(118,96)],2.9)
marks = [r_letter,i_letter,p_letter,ribbon([(69,125),(88,124),(104,126),(130,124)],2.1,taper=True),
         ribbon([(79,138),(97,139),(120,137)],1.8,taper=True),
         ribbon([(122,43),(117,55),(124,60),(119,73)],2.0,taper=True)]
shell(s,outer,inner,marks)
ink(s,ribbon([(34,174),(59,172),(87,175),(113,173),(140,176),(166,172)],3.6),
    ribbon([(46,172),(39,157),(45,162),(50,167)],2.2),
    ribbon([(56,174),(57,160),(61,164),(64,170)],2.2),
    ribbon([(144,174),(148,157),(152,167),(160,160),(157,173)],2.2))
SHAPES["gravestone"] = ("halloween",s)

COLOURS = {"bookfront":"#B494AA","bookopen":"#E4CBA2","nib":"#C8B474",
           "fountainpen":"#8DACA4","inkpot":"#9EAFB9","quill":"#E1CFA7",
           "skeleton":"#DED2B6","ghost":"#D5DDD3","spiderweb":"#AFBEB6",
           "grimreaper":"#A596B5","gravestone":"#AEA99C"}


def path(d,rule="nonzero",colour="black"):
    return f'<path fill="{colour}" fill-rule="{rule}" d="{d}"/>'


def document(paths):
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 200 200">\n'
            + "\n".join(paths) + '\n</svg>\n')


def convert(source,target,converter):
    subprocess.run([converter,"--format=svg","--output",str(target),str(source)],check=True)
    ET.register_namespace("",NS)
    tree = ET.parse(target)
    root = tree.getroot()
    children = list(root)
    if not (len(children)==1 and children[0].get("id","").startswith("surface")):
        surface = ET.Element(f"{{{NS}}}g",{"id":"surface1"})
        for child in children:
            root.remove(child); surface.append(child)
        root.append(surface)
    ET.indent(tree,space="  ")
    tree.write(target,encoding="utf-8",xml_declaration=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir",type=Path,default=PKG/"inst"/"extdata")
    parser.add_argument("--preview-dir",type=Path,default=ROOT/"preview-svg")
    parser.add_argument("--rsvg-convert",default=shutil.which("rsvg-convert") or "/opt/local/bin/rsvg-convert")
    args = parser.parse_args()
    converter = shutil.which(args.rsvg_convert) or (args.rsvg_convert if Path(args.rsvg_convert).is_file() else None)
    if not converter:
        raise SystemExit("rsvg-convert is needed only for regeneration; converted SVGs are supplied.")
    for directory in (ROOT/"source-svg",args.output_dir,args.preview_dir):
        directory.mkdir(parents=True,exist_ok=True)
    for name,(group,s) in SHAPES.items():
        for layer in ("col","fill"):
            source = ROOT/"source-svg"/f"{group}-{name}_{layer}.svg"
            target = args.output_dir/f"{group}-{name}_{layer}-cairo.svg"
            source.write_text(document([path(d,rule) for d,rule in s[layer]]))
            convert(source,target,converter)
        for mode in ("filled","outline"):
            paths = [path(d,rule,"#36312F") for d,rule in s["col"]]
            if mode=="filled":
                paths += [path(d,rule,COLOURS[name]) for d,rule in s["fill"]]
            (args.preview_dir/f"{name}-{mode}.svg").write_text(document(paths))
    print(f"Generated {len(SHAPES)} shapes: 22 source SVGs, 22 Cairo SVGs and paired previews.")


if __name__ == "__main__":
    main()
