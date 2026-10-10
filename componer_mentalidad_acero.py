import os
import sys
from PIL import Image, ImageDraw, ImageFont

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

def obtener_fuente(nombre, tamano):
    rutas_posibles = [
        f"C:\\Windows\\Fonts\\{nombre}",
        f"C:\\Windows\\Fonts\\impact.ttf",
        f"C:\\Windows\\Fonts\\arialbd.ttf",
        f"C:\\Windows\\Fonts\\arial.ttf"
    ]
    for r in rutas_posibles:
        if os.path.exists(r):
            try:
                return ImageFont.truetype(r, tamano)
            except Exception:
                continue
    return ImageFont.load_default()

import math

def dibujar_flecha(draw, start, end, color, width=3):
    draw.line([start, end], fill=color, width=width)
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    angle = math.atan2(dy, dx)
    arrow_len = 14
    arrow_angle = math.pi / 6
    p1 = (end[0] - arrow_len * math.cos(angle - arrow_angle), end[1] - arrow_len * math.sin(angle - arrow_angle))
    p2 = (end[0] - arrow_len * math.cos(angle + arrow_angle), end[1] - arrow_len * math.sin(angle + arrow_angle))
    draw.polygon([end, p1, p2], fill=color)

def componer_infografia_mentalidad(
    imagen_base_path,
    titulo_superior="MENTALIDAD ERRÓNEA",
    subtitulo_superior="EL POBRECITO",
    items_izquierda=[
        "ES CULPA DE OTROS",
        "SIEMPRE SE QUEJA",
        "TODO LE SALE MAL",
        "VIVE EN EXCUSAS",
        "BUSCA LÁSTIMA",
        "SE SIENTE VÍCTIMA"
    ],
    items_derecha=[
        "ASUME RESPONSABILIDAD",
        "BUSCA SOLUCIONES",
        "APRENDE DE DIFICULTADES",
        "TRABAJA DURO",
        "NO BUSCA LÁSTIMA",
        "SE LEVANTA Y SIGUE"
    ],
    frase_linea1="LA POBREZA PUEDE SER UNA CIRCUNSTANCIA,",
    frase_linea2="PERO LA MENTALIDAD DE VÍCTIMA PUEDE SER UNA PRISIÓN.",
    output_path="mentalidad_infografia_final.jpg"
):
    # Formato vertical óptimo para Facebook: 1080 x 1350 (4:5)
    ancho_final = 1080
    alto_final = 1350

    img_base = Image.open(imagen_base_path).convert("RGBA")
    # Redimensionar cubriendo el lienzo central
    img_ratio = img_base.width / img_base.height
    target_ratio = ancho_final / alto_final

    if img_ratio > target_ratio:
        new_h = alto_final
        new_w = int(alto_final * img_ratio)
    else:
        new_w = ancho_final
        new_h = int(ancho_final / img_ratio)

    img_resized = img_base.resize((new_w, new_h), Image.Resampling.LANCZOS)
    left = (new_w - ancho_final) // 2
    top = (new_h - alto_final) // 2
    canvas = img_resized.crop((left, top, left + ancho_final, top + alto_final))

    # Capas de sombreado superior e inferior para legibilidad perfecta
    overlay = Image.new("RGBA", (ancho_final, alto_final), (0, 0, 0, 0))
    draw_ov = ImageDraw.Draw(overlay)

    # Degradado superior (0 a 240px)
    for y in range(240):
        alpha = int(220 * (1 - (y / 240.0) ** 1.3))
        draw_ov.line([(0, y), (ancho_final, y)], fill=(0, 0, 0, alpha))

    # Degradado inferior (1050 a 1350px)
    for y in range(1050, alto_final):
        alpha = int(240 * ((y - 1050) / 300.0) ** 1.1)
        draw_ov.line([(0, y), (ancho_final, y)], fill=(0, 0, 0, alpha))

    # Viñeta lateral tenue para resaltar textos
    for x in range(180):
        alpha = int(140 * (1 - (x / 180.0) ** 1.2))
        draw_ov.line([(x, 240), (x, 1050)], fill=(0, 0, 0, alpha))
        draw_ov.line([(ancho_final - 1 - x, 240), (ancho_final - 1 - x, 1050)], fill=(0, 0, 0, alpha))

    canvas = Image.alpha_composite(canvas, overlay)
    draw = ImageDraw.Draw(canvas)

    # 1. ENCABEZADO SUPERIOR
    font_titulo = obtener_fuente("impact.ttf", 64)
    font_subtitulo = obtener_fuente("impact.ttf", 80)

    # Texto: MENTALIDAD ERRÓNEA (blanco con sombra)
    bbox_t = draw.textbbox((0, 0), titulo_superior, font=font_titulo)
    w_t = bbox_t[2] - bbox_t[0]
    x_t = (ancho_final - w_t) // 2
    y_t = 35

    draw.text((x_t + 3, y_t + 3), titulo_superior, fill=(0, 0, 0, 240), font=font_titulo)
    draw.text((x_t, y_t), titulo_superior, fill=(255, 255, 255, 255), font=font_titulo)

    # Texto: EL POBRECITO (amarillo oro con sombra profunda)
    bbox_s = draw.textbbox((0, 0), subtitulo_superior, font=font_subtitulo)
    w_s = bbox_s[2] - bbox_s[0]
    x_s = (ancho_final - w_s) // 2
    y_s = 105

    draw.text((x_s + 4, y_s + 4), subtitulo_superior, fill=(0, 0, 0, 250), font=font_subtitulo)
    draw.text((x_s, y_s), subtitulo_superior, fill=(245, 175, 25, 255), font=font_subtitulo)

    # Línea roja decorativa bajo el título
    draw.line([(x_s, y_s + 90), (x_s + w_s, y_s + 90)], fill=(220, 38, 38, 240), width=4)

    # 2. ELEMENTOS IZQUIERDA (Mentalidad Débil)
    font_items = obtener_fuente("impact.ttf", 30)

    y_start_izq = 260
    espacio_y_izq = 115

    for i, item in enumerate(items_izquierda[:6]):
        cur_y = y_start_izq + (i * espacio_y_izq)
        bbox_it = draw.textbbox((0, 0), item, font=font_items)
        w_it = bbox_it[2] - bbox_it[0]

        # Sombra y texto
        draw.text((32, cur_y + 2), item, fill=(0, 0, 0, 240), font=font_items)
        draw.text((30, cur_y), item, fill=(241, 245, 249, 255), font=font_items)

        # Flecha indicadora hacia el centro/personaje
        start_x = 40 + w_it + 15
        end_x = start_x + 55
        target_y = cur_y + 16
        dibujar_flecha(draw, (start_x, target_y), (end_x, target_y), (148, 163, 184, 220), width=3)

    # 3. ELEMENTOS DERECHA (Mentalidad de Acero)
    y_start_der = 260
    espacio_y_der = 115

    for i, item in enumerate(items_derecha[:6]):
        cur_y = y_start_der + (i * espacio_y_der)
        bbox_it = draw.textbbox((0, 0), item, font=font_items)
        w_it = bbox_it[2] - bbox_it[0]
        cur_x = ancho_final - 35 - w_it

        # Flecha indicadora hacia el personaje/centro
        start_x = cur_x - 15
        end_x = start_x - 55
        target_y = cur_y + 16
        dibujar_flecha(draw, (start_x, target_y), (end_x, target_y), (245, 175, 25, 240), width=3)

        # Sombra y texto
        draw.text((cur_x + 2, cur_y + 2), item, fill=(0, 0, 0, 240), font=font_items)
        draw.text((cur_x, cur_y), item, fill=(255, 255, 255, 255), font=font_items)

    # 4. FRASE SENTENCIA INFERIOR
    font_frase1 = obtener_fuente("impact.ttf", 36)
    font_frase2 = obtener_fuente("impact.ttf", 40)
    font_firma = obtener_fuente("arialbd.ttf", 22)

    # Línea 1 (Blanca)
    bbox_f1 = draw.textbbox((0, 0), frase_linea1, font=font_frase1)
    w_f1 = bbox_f1[2] - bbox_f1[0]
    x_f1 = (ancho_final - w_f1) // 2
    y_f1 = 1130

    draw.text((x_f1 + 3, y_f1 + 3), frase_linea1, fill=(0, 0, 0, 240), font=font_frase1)
    draw.text((x_f1, y_f1), frase_linea1, fill=(255, 255, 255, 255), font=font_frase1)

    # Línea 2 (Amarillo Oro)
    bbox_f2 = draw.textbbox((0, 0), frase_linea2, font=font_frase2)
    w_f2 = bbox_f2[2] - bbox_f2[0]
    x_f2 = (ancho_final - w_f2) // 2
    y_f2 = 1180

    draw.text((x_f2 + 3, y_f2 + 3), frase_linea2, fill=(0, 0, 0, 250), font=font_frase2)
    draw.text((x_f2, y_f2), frase_linea2, fill=(245, 175, 25, 255), font=font_frase2)

    # Firma: — MENTALIDAD DE ACERO —
    firma = "— MENTALIDAD DE ACERO —"
    bbox_fi = draw.textbbox((0, 0), firma, font=font_firma)
    w_fi = bbox_fi[2] - bbox_fi[0]
    x_fi = (ancho_final - w_fi) // 2
    y_fi = 1260

    draw.text((x_fi + 2, y_fi + 2), firma, fill=(0, 0, 0, 220), font=font_firma)
    draw.text((x_fi, y_fi), firma, fill=(148, 163, 184, 240), font=font_firma)

    # Guardar en JPEG alta calidad
    canvas.convert("RGB").save(output_path, "JPEG", quality=95)
    print(f"✅ Infografía de Mentalidad generada con éxito en: {output_path}")

if __name__ == "__main__":
    base_img = sys.argv[1] if len(sys.argv) > 1 else "C:\\Users\\JMSOLUTIONS8825\\.gemini\\antigravity\\brain\\89115b35-5a7e-4589-b341-10e2a7da7397\\mentalidad_de_acero_1791642856974.jpg"
    out = sys.argv[2] if len(sys.argv) > 2 else "ejemplo_mentalidad_acero_viral.jpg"
    componer_infografia_mentalidad(base_img, output_path=out)
