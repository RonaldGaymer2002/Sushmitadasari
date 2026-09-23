import sys
from PIL import Image, ImageEnhance

IMAGE_PATH = "85209734.jpg"
SVG_PATH = "dark.svg"

# Dimensiones exactas de la rejilla para cubrir el recuadro VISUAL.MAP
COLS = 82
ROWS = 58

ASCII_CHARS = ["@", "%", "#", "*", "+", "=", "-", ":", "."]

try:
    img = Image.open(IMAGE_PATH).convert("L")
except Exception as e:
    print(f"Error cargando imagen: {e}")
    sys.exit(1)

# Realce de contraste
enhancer = ImageEnhance.Contrast(img)
img = enhancer.enhance(1.45)

# --- RECORTE INTELIGENTE (ZOOM) PARA LLENAR EL ANCHO ---
# Recortamos margen sobrante de arriba/abajo para que el torso y cabeza se ensanchen al 100%
w, h = img.size
crop_top = int(h * 0.05)       # Cortar un poco de aire superior
crop_bottom = int(h * 0.85)    # Tomar torso superior y hombros completos
img = img.crop((0, crop_top, w, crop_bottom))

# Redimensionar directamente a la matriz completa del visor
img = img.resize((COLS, ROWS))

pixels = list(img.getdata())
lines = []
for i in range(0, len(pixels), COLS):
    row = pixels[i : i + COLS]
    line = "".join([ASCII_CHARS[int(p / 256 * len(ASCII_CHARS))] for p in row])
    lines.append(line)

# Posicionamiento: arranca en x="24" para cubrir de izquierda a derecha
y_start = 54.00
y_step = 7.30
tspans = []
for idx, line in enumerate(lines):
    curr_y = f"{y_start + idx * y_step:.2f}"
    safe_line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    tspans.append(f'<tspan x="24" y="{curr_y}" xml:space="preserve">{safe_line}</tspan>')

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
    print("¡dark.svg actualizado con zoom y ancho completo!")
else:
    print("No se encontró el marcador del bloque ASCII.")
