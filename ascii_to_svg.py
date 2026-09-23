import sys
from PIL import Image, ImageEnhance

IMAGE_PATH = "85209734.jpg"
SVG_PATH = "dark.svg"

# Aumentamos el ancho para que abarque todo el ancho del VISUAL.MAP
WIDTH = 64  

# Caracteres de densidad tonal refinada
ASCII_CHARS = ["@", "%", "#", "*", "+", "=", "-", ":", "."]

try:
    img = Image.open(IMAGE_PATH).convert("L")
except Exception as e:
    print(f"Error cargando imagen: {e}")
    sys.exit(1)

# Realce de contraste para rasgos definidos
enhancer = ImageEnhance.Contrast(img)
img = enhancer.enhance(1.45)

# Calculamos altura para llenar verticalmente el cuadro (hasta 58 líneas)
w, h = img.size
aspect_ratio = h / w
new_height = int(WIDTH * aspect_ratio * 0.55)
# Aseguramos un mínimo de 58 filas para abarcar hasta abajo
new_height = max(58, new_height)
img = img.resize((WIDTH, new_height))

pixels = list(img.getdata())
lines = []
for i in range(0, len(pixels), WIDTH):
    row = pixels[i : i + WIDTH]
    line = "".join([ASCII_CHARS[int(p / 256 * len(ASCII_CHARS))] for p in row])
    lines.append(line)

# Tomamos 58 líneas para ocupar todo el alto del contenedor
lines = lines[:58]

# Posicionamiento exacto dentro del recuadro
y_start = 56.00
y_step = 7.30
tspans = []
for idx, line in enumerate(lines):
    curr_y = f"{y_start + idx * y_step:.2f}"
    safe_line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    tspans.append(f'<tspan x="22" y="{curr_y}" xml:space="preserve">{safe_line}</tspan>')

ascii_block = "\n".join(tspans)

# Reemplazar bloque ASCII en dark.svg
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
    print("¡dark.svg ampliado exitosamente a pantalla completa!")
else:
    print("No se encontró el marcador del bloque ASCII.")
