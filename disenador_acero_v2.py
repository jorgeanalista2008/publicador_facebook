import os
import sys
import math
from PIL import Image, ImageDraw, ImageFont

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

def get_font(name, size):
    paths = [
        f"C:\\Windows\\Fonts\\{name}",
        f"C:\\Windows\\Fonts\\segoeuib.ttf",
        f"C:\\Windows\\Fonts\\ariblk.ttf",
        f"C:\\Windows\\Fonts\\arialbd.ttf",
        f"C:\\Windows\\Fonts\\impact.ttf"
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except:
                pass
    return ImageFont.load_default()

def preparar_lienzo_base(bg_path, ancho=1080, alto=1350, oscuridad=0.75):
    """Carga y oscurece un fondo cinemático al tamaño exacto 4:5."""
    if os.path.exists(bg_path):
        img = Image.open(bg_path).convert("RGBA")
        ratio = img.width / img.height
        target_ratio = ancho / alto
        if ratio > target_ratio:
            new_h = alto
            new_w = int(alto * ratio)
        else:
            new_w = ancho
            new_h = int(ancho / ratio)
        img_res = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        left = (new_w - ancho) // 2
        top = (new_h - alto) // 2
        canvas = img_res.crop((left, top, left + ancho, top + alto))
    else:
        canvas = Image.new("RGBA", (ancho, alto), (15, 17, 22, 255))

    # Capa de oscurecimiento y degradado cinemático
    overlay = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))
    d_ov = ImageDraw.Draw(overlay)

    # Base oscura
    d_ov.rectangle([(0, 0), (ancho, alto)], fill=(8, 10, 15, int(255 * oscuridad)))

    # Viñeta suave en bordes
    for y in range(250):
        alpha = int(180 * (1 - (y / 250.0) ** 1.3))
        d_ov.line([(0, y), (ancho, y)], fill=(0, 0, 0, alpha))
    for y in range(alto - 250, alto):
        alpha = int(220 * (((y - (alto - 250)) / 250.0) ** 1.2))
        d_ov.line([(0, y), (ancho, y)], fill=(0, 0, 0, alpha))

    return Image.alpha_composite(canvas, overlay)

# ==============================================================================
# TEMPLATE 1: EL DESPERTADOR DE ACERO (07:00 AM)
# ==============================================================================
def generar_imagen_despertador(bg_path, numero_ley, frase_principal, frase_secundaria, output_path):
    ancho, alto = 1080, 1350
    canvas = preparar_lienzo_base(bg_path, ancho, alto, oscuridad=0.72)
    draw = ImageDraw.Draw(canvas)

    # 1. Badge Superior
    f_badge = get_font("segoeuib.ttf", 26)
    badge_txt = f"⚔️  REGLA INQUEBRANTABLE #{numero_ley:02d}  ⚔️"
    bbox_b = draw.textbbox((0, 0), badge_txt, font=f_badge)
    bw = bbox_b[2] - bbox_b[0]
    bx = (ancho - bw) // 2
    by = 130
    draw.rounded_rectangle([bx - 24, by - 10, bx + bw + 24, by + 40], radius=10, fill=(18, 22, 30, 240), outline=(212, 160, 23, 230), width=2)
    draw.text((bx, by), badge_txt, font=f_badge, fill=(245, 185, 45, 255))

    # 2. Marco decorativo fino
    draw.rectangle([(50, 50), (ancho - 50, alto - 50)], outline=(255, 255, 255, 30), width=1)

    # 3. Frase Principal en gran formato (auto-wrap)
    f_tit = get_font("ariblk.ttf", 52)
    palabras = frase_principal.upper().split()
    lineas = []
    linea_actual = []
    for p in palabras:
        linea_actual.append(p)
        bbox = draw.textbbox((0, 0), " ".join(linea_actual), font=f_tit)
        if (bbox[2] - bbox[0]) > (ancho - 160):
            linea_actual.pop()
            lineas.append(" ".join(linea_actual))
            linea_actual = [p]
    if linea_actual:
        lineas.append(" ".join(linea_actual))

    total_h = len(lineas) * 72
    y_start = 500 - (total_h // 2)

    for i, l in enumerate(lineas):
        bbox_l = draw.textbbox((0, 0), l, font=f_tit)
        lw = bbox_l[2] - bbox_l[0]
        lx = (ancho - lw) // 2
        ly = y_start + (i * 72)
        # Sombra profunda
        draw.text((lx + 4, ly + 4), l, font=f_tit, fill=(0, 0, 0, 250))
        # Color alternado para la última línea
        col = (245, 185, 45, 255) if i == len(lineas) - 1 else (255, 255, 255, 255)
        draw.text((lx, ly), l, font=f_tit, fill=col)

    # Línea divisoria dorada
    sep_y = y_start + total_h + 30
    draw.line([(ancho // 2 - 120, sep_y), (ancho // 2 + 120, sep_y)], fill=(212, 160, 23, 220), width=3)

    # 4. Frase secundaria reflexiva
    if frase_secundaria:
        f_sec = get_font("georgiab.ttf", 32)
        bbox_sec = draw.textbbox((0, 0), frase_secundaria, font=f_sec)
        sw = bbox_sec[2] - bbox_sec[0]
        sx = (ancho - sw) // 2
        sy = sep_y + 40
        draw.text((sx + 2, sy + 2), frase_secundaria, font=f_sec, fill=(0, 0, 0, 240))
        draw.text((sx, sy), frase_secundaria, font=f_sec, fill=(203, 213, 225, 255))

    # 5. Firma de marca
    f_brand = get_font("segoeuib.ttf", 22)
    brand_txt = "—  M E N T A L I D A D   D E   A C E R O  —"
    bbox_br = draw.textbbox((0, 0), brand_txt, font=f_brand)
    draw.text(((ancho - (bbox_br[2] - bbox_br[0])) // 2, alto - 120), brand_txt, font=f_brand, fill=(148, 163, 184, 230))

    canvas.convert("RGB").save(output_path, "JPEG", quality=95)

# ==============================================================================
# TEMPLATE 2: LA BATALLA DE CONTRASTE (12:30 PM)
# ==============================================================================
def generar_imagen_contraste(bg_path, arquetipo, rasgos_debil, rasgos_acero, sentencia, output_path):
    ancho, alto = 1080, 1350
    canvas = preparar_lienzo_base(bg_path, ancho, alto, oscuridad=0.82)
    draw = ImageDraw.Draw(canvas)

    # 1. Cabecera
    f_sub = get_font("segoeuib.ttf", 24)
    head_txt = "MENTALIDAD ERRÓNEA  vs  MENTALIDAD DE ACERO"
    bbox_h = draw.textbbox((0, 0), head_txt, font=f_sub)
    draw.text(((ancho - (bbox_h[2] - bbox_h[0])) // 2, 70), head_txt, font=f_sub, fill=(148, 163, 184, 255))

    # Nombre del arquetipo en dorado
    f_arq = get_font("ariblk.ttf", 52)
    bbox_a = draw.textbbox((0, 0), arquetipo.upper(), font=f_arq)
    aw = bbox_a[2] - bbox_a[0]
    draw.text(((ancho - aw) // 2 + 3, 113), arquetipo.upper(), font=f_arq, fill=(0, 0, 0, 240))
    draw.text(((ancho - aw) // 2, 110), arquetipo.upper(), font=f_arq, fill=(245, 185, 45, 255))

    # Línea decorativa
    draw.line([((ancho - aw) // 2, 180), ((ancho + aw) // 2, 180)], fill=(220, 38, 38, 220), width=3)

    # 2. Tarjetas Glassmorphism Divididas (Izquierda: Débil | Derecha: Acero)
    card_w = 460
    card_top = 220
    card_h = 780
    f_card_head = get_font("ariblk.ttf", 26)
    f_items = get_font("segoeuib.ttf", 22)

    # Tarjeta Izquierda (Roja)
    draw.rounded_rectangle([60, card_top, 60 + card_w, card_top + card_h], radius=16, fill=(26, 16, 18, 230), outline=(220, 38, 38, 160), width=2)
    draw.text((100, card_top + 30), "✕  MENTALIDAD DÉBIL", font=f_card_head, fill=(239, 68, 68, 255))
    draw.line([(80, card_top + 75), (60 + card_w - 20, card_top + 75)], fill=(220, 38, 38, 80), width=1)

    y_item = card_top + 110
    for it in rasgos_debil[:6]:
        draw.text((85, y_item), "✕", font=f_items, fill=(239, 68, 68, 240))
        draw.text((115, y_item), it.upper(), font=f_items, fill=(226, 232, 240, 255))
        y_item += 105

    # Tarjeta Derecha (Dorada/Verde)
    x_der = ancho - 60 - card_w
    draw.rounded_rectangle([x_der, card_top, x_der + card_w, card_top + card_h], radius=16, fill=(16, 26, 22, 230), outline=(212, 160, 23, 180), width=2)
    draw.text((x_der + 40, card_top + 30), "✓  HOMBRE DE ACERO", font=f_card_head, fill=(245, 185, 45, 255))
    draw.line([(x_der + 20, card_top + 75), (x_der + card_w - 20, card_top + 75)], fill=(212, 160, 23, 80), width=1)

    y_item = card_top + 110
    for it in rasgos_acero[:6]:
        draw.text((x_der + 25, y_item), "✓", font=f_items, fill=(245, 185, 45, 255))
        draw.text((x_der + 55, y_item), it.upper(), font=f_items, fill=(255, 255, 255, 255))
        y_item += 105

    # 3. Sentencia Inferior
    f_sent = get_font("georgiab.ttf", 28)
    # Auto-wrap sentencia
    palabras = sentencia.split()
    lineas_s = []
    curr = []
    for p in palabras:
        curr.append(p)
        bbox = draw.textbbox((0, 0), " ".join(curr), font=f_sent)
        if (bbox[2] - bbox[0]) > 900:
            curr.pop()
            lineas_s.append(" ".join(curr))
            curr = [p]
    if curr:
        lineas_s.append(" ".join(curr))

    y_sent = 1050
    for l in lineas_s[:2]:
        bbox_l = draw.textbbox((0, 0), l, font=f_sent)
        lw = bbox_l[2] - bbox_l[0]
        draw.text(((ancho - lw) // 2, y_sent), l, font=f_sent, fill=(245, 185, 45, 255))
        y_sent += 42

    # Firma
    f_brand = get_font("segoeuib.ttf", 20)
    brand_txt = "—  M E N T A L I D A D   D E   A C E R O  —"
    bbox_br = draw.textbbox((0, 0), brand_txt, font=f_brand)
    draw.text(((ancho - (bbox_br[2] - bbox_br[0])) // 2, alto - 80), brand_txt, font=f_brand, fill=(148, 163, 184, 220))

    canvas.convert("RGB").save(output_path, "JPEG", quality=95)

# ==============================================================================
# TEMPLATE 3: LEYES DE GUERRA & ESTRATEGIA (17:30 PM)
# ==============================================================================
def generar_imagen_estrategia(bg_path, titulo_ley, regla_principal, tres_principios, output_path):
    ancho, alto = 1080, 1350
    canvas = preparar_lienzo_base(bg_path, ancho, alto, oscuridad=0.78)
    draw = ImageDraw.Draw(canvas)

    # Badge Superior
    f_badge = get_font("segoeuib.ttf", 24)
    badge_txt = f"🏛️  {titulo_ley.upper()}  🏛️"
    bbox_b = draw.textbbox((0, 0), badge_txt, font=f_badge)
    bw = bbox_b[2] - bbox_b[0]
    draw.rounded_rectangle([(ancho - bw) // 2 - 20, 110, (ancho + bw) // 2 + 20, 155], radius=8, fill=(18, 22, 30, 240), outline=(212, 160, 23, 200), width=2)
    draw.text(((ancho - bw) // 2, 120), badge_txt, font=f_badge, fill=(245, 185, 45, 255))

    # Regla Principal
    f_regla = get_font("ariblk.ttf", 46)
    palabras = regla_principal.upper().split()
    lineas = []
    curr = []
    for p in palabras:
        curr.append(p)
        bbox = draw.textbbox((0, 0), " ".join(curr), font=f_regla)
        if (bbox[2] - bbox[0]) > 900:
            curr.pop()
            lineas.append(" ".join(curr))
            curr = [p]
    if curr:
        lineas.append(" ".join(curr))

    y_r = 240
    for l in lineas:
        bbox_l = draw.textbbox((0, 0), l, font=f_regla)
        lw = bbox_l[2] - bbox_l[0]
        draw.text(((ancho - lw) // 2 + 3, y_r + 3), l, font=f_regla, fill=(0, 0, 0, 240))
        draw.text(((ancho - lw) // 2, y_r), l, font=f_regla, fill=(255, 255, 255, 255))
        y_r += 62

    # 3 Tarjetas de Principios
    card_w = 920
    card_h = 160
    f_ptit = get_font("ariblk.ttf", 26)
    f_ptxt = get_font("segoeuib.ttf", 22)

    y_cards = 550
    for i, (p_tit, p_txt) in enumerate(tres_principios[:3]):
        cx = (ancho - card_w) // 2
        cy = y_cards + (i * 190)
        draw.rounded_rectangle([cx, cy, cx + card_w, cy + card_h], radius=14, fill=(18, 22, 28, 230), outline=(212, 160, 23, 140), width=2)

        # Número en círculo dorado
        draw.ellipse([cx + 25, cy + 30, cx + 85, cy + 90], fill=(212, 160, 23, 230))
        draw.text((cx + 46, cy + 42), str(i + 1), font=f_ptit, fill=(15, 20, 25, 255))

        # Título y descripción
        draw.text((cx + 110, cy + 32), p_tit.upper(), font=f_ptit, fill=(245, 185, 45, 255))
        draw.text((cx + 110, cy + 78), p_txt, font=f_ptxt, fill=(226, 232, 240, 255))

    # Firma
    f_brand = get_font("segoeuib.ttf", 20)
    brand_txt = "—  M E N T A L I D A D   D E   A C E R O  —"
    bbox_br = draw.textbbox((0, 0), brand_txt, font=f_brand)
    draw.text(((ancho - (bbox_br[2] - bbox_br[0])) // 2, alto - 80), brand_txt, font=f_brand, fill=(148, 163, 184, 220))

    canvas.convert("RGB").save(output_path, "JPEG", quality=95)

# ==============================================================================
# TEMPLATE 4: AUDITORÍA NOCTURNA (21:30 PM)
# ==============================================================================
def generar_imagen_auditoria(bg_path, pregunta_central, desafio, output_path):
    ancho, alto = 1080, 1350
    canvas = preparar_lienzo_base(bg_path, ancho, alto, oscuridad=0.88)
    draw = ImageDraw.Draw(canvas)

    # 1. Badge Superior
    f_badge = get_font("segoeuib.ttf", 26)
    badge_txt = "🌙  AUDITORÍA DE CIERRE DE DÍA  🌙"
    bbox_b = draw.textbbox((0, 0), badge_txt, font=f_badge)
    bw = bbox_b[2] - bbox_b[0]
    bx = (ancho - bw) // 2
    by = 180
    draw.rounded_rectangle([bx - 24, by - 10, bx + bw + 24, by + 40], radius=10, fill=(18, 22, 30, 240), outline=(212, 160, 23, 230), width=2)
    draw.text((bx, by), badge_txt, font=f_badge, fill=(245, 185, 45, 255))

    # 2. Gran Caja Central
    box_w = 920
    box_h = 580
    box_x = (ancho - box_w) // 2
    box_y = 350
    draw.rounded_rectangle([box_x, box_y, box_x + box_w, box_y + box_h], radius=20, fill=(15, 18, 24, 240), outline=(148, 163, 184, 100), width=2)

    # Icono o subcabecera
    f_sub = get_font("segoeuib.ttf", 24)
    sub_txt = "EL JUICIO FRENTE AL ESPEJO"
    bbox_s = draw.textbbox((0, 0), sub_txt, font=f_sub)
    draw.text(((ancho - (bbox_s[2] - bbox_s[0])) // 2, box_y + 40), sub_txt, font=f_sub, fill=(148, 163, 184, 255))

    # Pregunta en gran formato
    f_preg = get_font("ariblk.ttf", 46)
    palabras = pregunta_central.upper().split()
    lineas = []
    curr = []
    for p in palabras:
        curr.append(p)
        bbox = draw.textbbox((0, 0), " ".join(curr), font=f_preg)
        if (bbox[2] - bbox[0]) > 800:
            curr.pop()
            lineas.append(" ".join(curr))
            curr = [p]
    if curr:
        lineas.append(" ".join(curr))

    y_p = box_y + 120
    for l in lineas:
        bbox_l = draw.textbbox((0, 0), l, font=f_preg)
        lw = bbox_l[2] - bbox_l[0]
        draw.text(((ancho - lw) // 2, y_p), l, font=f_preg, fill=(255, 255, 255, 255))
        y_p += 65

    # Desafío / CTA
    f_des = get_font("georgiab.ttf", 28)
    bbox_d = draw.textbbox((0, 0), desafio, font=f_des)
    dw = bbox_d[2] - bbox_d[0]
    draw.text(((ancho - dw) // 2, box_y + box_h - 90), desafio, font=f_des, fill=(245, 185, 45, 255))

    # Pie
    f_com = get_font("segoeuib.ttf", 24)
    com_txt = "Responde con la verdad en los comentarios.  👇"
    bbox_c = draw.textbbox((0, 0), com_txt, font=f_com)
    draw.text(((ancho - (bbox_c[2] - bbox_c[0])) // 2, box_y + box_h + 60), com_txt, font=f_com, fill=(203, 213, 225, 255))

    f_brand = get_font("segoeuib.ttf", 20)
    brand_txt = "—  M E N T A L I D A D   D E   A C E R O  —"
    bbox_br = draw.textbbox((0, 0), brand_txt, font=f_brand)
    draw.text(((ancho - (bbox_br[2] - bbox_br[0])) // 2, alto - 80), brand_txt, font=f_brand, fill=(148, 163, 184, 220))

    canvas.convert("RGB").save(output_path, "JPEG", quality=95)
