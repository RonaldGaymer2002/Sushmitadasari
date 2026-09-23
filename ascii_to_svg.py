import sys
from PIL import Image, ImageEnhance

IMAGE_PATH = "85209734.jpg"
SVG_PATH = "dark.svg"

WIDTH = 76
ROWS = 58

ASCII_CHARS = ["@", "%", "#", "*", "+", "=", "-", ":", "."]

try:
    img = Image.open(IMAGE_PATH).convert("L")
except Exception as e:
    print(f"Error cargando imagen: {e}")
    sys.exit(1)

# Contraste pronunciado para marcar bien tus rasgos
enhancer = ImageEnhance.Contrast(img)
img = enhancer.enhance(1.45)

# --- RECORTE INTELIGENTE: Eliminamos el fondo blanco de los lados para hacer zoom ---
w, h = img.size
crop_left = int(w * 0.15)      # Cortamos 15% de espacio vacío a la izquierda
crop_right = int(w * 0.85)     # Cortamos 15% de espacio vacío a la derecha
crop_top = int(h * 0.03)       # Empezamos justo arriba del pelo
crop_bottom = int(h * 0.82)    # Bajamos hasta el pecho/hombros
img = img.crop((crop_left, crop_top, crop_right, crop_bottom))

# Redimensionamos al lienzo completo
img = img.resize((WIDTH, ROWS))

pixels = list(img.getdata())
lines = []
for i in range(0, len(pixels), WIDTH):
    row = pixels[i : i + WIDTH]
    line = "".join([ASCII_CHARS[int(p / 256 * len(ASCII_CHARS))] for p in row])
    lines.append(line)

lines = lines[:ROWS]

# Centro exacto del recuadro VISUAL.MAP (x=257) con centrado nativo
CENTER_X = 257
y_start = 55.00
y_step = 7.30
tspans = []
for idx, line in enumerate(lines):
    curr_y = f"{y_start + idx * y_step:.2f}"
    safe_line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    tspans.append(f'<tspan x="{CENTER_X}" y="{curr_y}" text-anchor="middle" xml:space="preserve">{safe_line}</tspan>')

ascii_block = "\n".join(tspans)

with open(SVG_PATH, "r", encoding="utf-8") as f:
    svg_content = f.read()

start_marker = '<text x="30" y="0" class="ascii">'
end_marker = '</text>'

start_pos = svg_content.find(start_marker)
if start_pos != -1:
    end_pos = svg_content.find(end_marker, start_pos)
    new_svg = (
        svg_content[: start_pos + len(start_marker)]
        + "\n"
        + ascii_block
        + "\n"
        + svg_content[end_pos:]
    )
    with open(SVG_PATH, "w", encoding="utf-8") as f:
        f.write(new_svg)
    print("¡dark.svg actualizado con zoom y proporciones anchas!")
else:
    print("No se encontró el marcador del bloque ASCII.")
