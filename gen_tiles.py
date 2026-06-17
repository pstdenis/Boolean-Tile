import base64
from PIL import Image, ImageDraw, ImageFont
import os

def bits(idx):
    return [(idx >> 3) & 1, (idx >> 2) & 1, (idx >> 1) & 1, idx & 1]

def is_live(x, y, b, depth):
    for d in range(depth):
        qx = (x >> (depth - 1 - d)) & 1
        qy = (y >> (depth - 1 - d)) & 1
        if b[qy * 2 + qx] == 0:
            return False
    return True

depth = 6
ts = 2 ** depth
pad = 6
label_h = 20
cols = rows = 4
total_w = ts * cols + pad * (cols - 1)
total_h = ts * rows + pad * (rows - 1) + (label_h + pad) * rows

img = Image.new("RGB", (total_w, total_h), (12, 12, 22))
px = img.load()

live = (55, 175, 255)
dead = (16, 16, 32)

for idx in range(16):
    b = bits(idx)
    tx, ty = idx % 4, idx // 4
    ox = tx * (ts + pad)
    oy = ty * (ts + pad) + label_h * (ty + 1) + pad * ty
    for y in range(ts):
        for x in range(ts):
            c = live if is_live(x, y, b, depth) else dead
            px[ox + x, oy + y] = c

draw = ImageDraw.Draw(img)
names = ["FALSE","AND","A\u2227\u00acB","A",
         "\u00acA\u2227B","B","XOR","OR",
         "NOR","XNOR","\u00acB","A\u2228\u00acB",
         "\u00acA","\u00acA\u2228B","NAND","TRUE"]
try:
    fnt = ImageFont.truetype("segoeui.ttf", 14)
except:
    fnt = ImageFont.load_default()
for idx in range(16):
    tx, ty = idx % 4, idx // 4
    lx = tx * (ts + pad)
    ly = ty * (ts + pad) + label_h * (ty + 1) + pad * ty - label_h
    draw.text((lx, ly), f"{idx:2d} {names[idx]}", fill=(160, 160, 180), font=fnt)

path = r"C:\Users\pauls\Desktop\Boolean Tile\ifs_tiles.png"
img.save(path)
print(f"Saved {img.size[0]}x{img.size[1]} {os.path.getsize(path)} bytes")
with open(path, "rb") as f:
    print("B64:" + base64.b64encode(f.read()).decode())
