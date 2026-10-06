# Genera los iconos PWA de Arduino Academy en img/
from PIL import Image, ImageDraw

BASE = 512

def draw_icon(size):
    s = size / BASE
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    teal = (0, 151, 157, 255)
    dark = (0, 97, 100, 255)
    white = (255, 255, 255, 255)

    # Fondo redondeado con degradado simulado (dos tonos)
    d.rounded_rectangle([0, 0, size, size], radius=int(96 * s), fill=teal)
    d.rounded_rectangle([0, int(size * 0.55), size, size], radius=int(96 * s), fill=dark)
    # Redondear la zona inferior del degradado: repintar esquinas superiores del bloque oscuro
    r = int(96 * s)
    d.rectangle([0, int(size * 0.55), r, size - 1], fill=dark)
    d.rectangle([size - r, int(size * 0.55), size - 1, size - 1], fill=dark)

    # Chip (microcontrolador): cuerpo
    cx = cy = size / 2
    cw = ch = size * 0.42
    d.rounded_rectangle([cx - cw/2, cy - ch/2, cx + cw/2, cy + ch/2],
                        radius=int(18 * s), fill=white)
    # Pines
    pin_l = size * 0.075
    pin_w = size * 0.035
    n = 4
    for i in range(n):
        off = -cw/2 + cw * (i + 0.5) / n
        # Arriba y abajo
        d.rounded_rectangle([cx + off - pin_w/2, cy - ch/2 - pin_l, cx + off + pin_w/2, cy - ch/2],
                            radius=int(6*s), fill=white)
        d.rounded_rectangle([cx + off - pin_w/2, cy + ch/2, cx + off + pin_w/2, cy + ch/2 + pin_l],
                            radius=int(6*s), fill=white)
        # Izquierda y derecha
        d.rounded_rectangle([cx - cw/2 - pin_l, cy + off - pin_w/2, cx - cw/2, cy + off + pin_w/2],
                            radius=int(6*s), fill=white)
        d.rounded_rectangle([cx + cw/2, cy + off - pin_w/2, cx + cw/2 + pin_l, cy + off + pin_w/2],
                            radius=int(6*s), fill=white)

    # Símbolo infinito (∞) estilizado en el chip, tono teal
    d.ellipse([cx - cw*0.34, cy - ch*0.16, cx - cw*0.02, cy + ch*0.16], outline=teal, width=int(14*s))
    d.ellipse([cx + cw*0.02, cy - ch*0.16, cx + cw*0.34, cy + ch*0.16], outline=teal, width=int(14*s))

    return img

sizes = {
    "icon-192.png": 192,
    "icon-512.png": 512,
    "icon-maskable-192.png": 192,
    "icon-maskable-512.png": 512,
    "apple-touch-icon.png": 180,
}

for name, sz in sizes.items():
    img = draw_icon(sz)
    if "maskable" in name:
        # Reescalar dentro de zona segura (80% del lienzo) sobre fondo teal sólido
        canvas = Image.new("RGBA", (sz, sz), (0, 121, 124, 255))
        inner = int(sz * 0.78)
        icon = draw_icon(inner).resize((inner, inner), Image.LANCZOS)
        off = (sz - inner) // 2
        canvas.paste(icon, (off, off), icon)
        img = canvas
    if name == "apple-touch-icon.png":
        bg = Image.new("RGB", (sz, sz), (0, 151, 157))
        bg.paste(img, (0, 0), img)
        img = bg
    img.save(f"img/{name}")
    print("OK", name)

# Favicon 32x32 (y 16) desde el icono base
icon32 = draw_icon(32)
icon32.save("img/favicon-32.png")
icon16 = draw_icon(16)
icon16.save("img/favicon-16.png")
print("OK favicons")
