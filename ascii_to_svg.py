import sys
from PIL import Image, ImageEnhance

IMAGE_PATH = "85209734.jpg"
SVG_PATH = "dark.svg"
WIDTH = 54  # Ancho en caracteres para el marco del escáner

# Caracteres ordenados de mayor densidad a menor densidad
ASCII_CHARS = ["@", "%", "#", "*", "+", "=", "-", ":", "."]

try:
    img = Image.open(IMAGE_PATH).convert("L")
except Exception as e:
    print(f"Error cargando imagen: {e}")
    sys.exit(1)

# Ajuste de contraste para destacar rasgos faciales
enhancer = ImageEnhance.Contrast(img)
img = enhancer.enhance(1.4)

# Calcular dimensiones proporcionales a fuente monospace de terminal
w, h = img.size
aspect_ratio = h / w
new_height = int(WIDTH * aspect_ratio * 0.55)
img = img.resize((WIDTH, new_height))

# Convertir explícitamente a lista para evitar error de rebanado (slice)
pixels = list(img.getdata())
lines = []
for i in range(0, len(pixels), WIDTH):
    row = pixels[i : i + WIDTH]
    line = "".join([ASCII_CHARS[int(p / 256 * len(ASCII_CHARS))] for p in row])
    lines.append(line)

# Ajustar al límite de líneas visibles en el marco
lines = lines[:53]

# Coordenadas exactas para la tipografía de dark.svg
y_start = 79.98
y_step = 7.55
tspans = []
for idx, line in enumerate(lines):
    curr_y = f"{y_start + idx * y_step:.2f}"
    safe_line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    tspans.append(f'<tspan x="30" y="{curr_y}" xml:space="preserve">{safe_line}</tspan>')

ascii_block = "\n".join(tspans)

# Actualizar el bloque de la cara dentro de dark.svg
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
    print("dark.svg actualizado exitosamente con tu rostro.")
else:
    print("No se encontró el marcador del bloque ASCII en dark.svg.")
