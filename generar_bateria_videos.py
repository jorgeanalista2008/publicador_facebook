# ============================================================
# GENERADOR EN BATERÍA DE VIDEOS VIRALES (TIKTOK / REELS / SHORTS)
# ------------------------------------------------------------
# Procesa las publicaciones y genera videos verticales 9:16 
# con locución en off de IA y zoom cinematográfico en HD.
# ============================================================

import os
import sys
import json
import subprocess
import imageio_ffmpeg
from PIL import Image, ImageFilter, ImageDraw, ImageFont
from gtts import gTTS

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

def preparar_lienzo_vertical(imagen_origen_path, salida_canvas_path, titulo_superior="• MENTALIDAD DE ACERO •"):
    img_orig = Image.open(imagen_origen_path).convert("RGB")
    ancho_orig, alto_orig = img_orig.size

    canvas_w = 1080
    canvas_h = 1920

    # Fondo desenfocado
    ratio = max(canvas_w / ancho_orig, canvas_h / alto_orig)
    bg_w = int(ancho_orig * ratio)
    bg_h = int(alto_orig * ratio)
    bg = img_orig.resize((bg_w, bg_h), Image.Resampling.LANCZOS)
    left = (bg_w - canvas_w) // 2
    top = (bg_h - canvas_h) // 2
    bg = bg.crop((left, top, left + canvas_w, top + canvas_h))
    bg = bg.filter(ImageFilter.GaussianBlur(radius=25))

    darkener = Image.new("RGB", (canvas_w, canvas_h), (0, 0, 0))
    bg = Image.blend(bg, darkener, alpha=0.55)

    # Imagen central centrada
    target_w = 1000
    target_h = int(alto_orig * (target_w / ancho_orig))
    if target_h > 1450:
        target_h = 1450
        target_w = int(ancho_orig * (target_h / alto_orig))

    img_central = img_orig.resize((target_w, target_h), Image.Resampling.LANCZOS)
    pos_x = (canvas_w - target_w) // 2
    pos_y = (canvas_h - target_h) // 2 + 30
    bg.paste(img_central, (pos_x, pos_y))

    # Textos superior e inferior
    draw = ImageDraw.Draw(bg)
    font_path = "C:\\Windows\\Fonts\\impact.ttf" if os.path.exists("C:\\Windows\\Fonts\\impact.ttf") else "C:\\Windows\\Fonts\\arialbd.ttf"
    try:
        font_header = ImageFont.truetype(font_path, 46)
        font_sub = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 26)
    except:
        font_header = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    # Badge superior
    badge_text = titulo_superior
    bbox = draw.textbbox((0, 0), badge_text, font=font_header)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    bx = (canvas_w - tw) // 2
    by = pos_y - 120

    pad_x, pad_y = 35, 12
    draw.rounded_rectangle([bx - pad_x, by - pad_y, bx + tw + pad_x, by + th + pad_y], radius=20, fill=(15, 23, 42), outline=(234, 179, 8), width=3)
    draw.text((bx, by), badge_text, fill=(255, 255, 255), font=font_header)

    # Indicador inferior
    footer_text = "TOCA DOS VECES SI ASUMES EL RETO"
    bbox_f = draw.textbbox((0, 0), footer_text, font=font_sub)
    fw = bbox_f[2] - bbox_f[0]
    draw.text(((canvas_w - fw) // 2, pos_y + target_h + 40), footer_text, fill=(203, 213, 225), font=font_sub)

    bg.save(salida_canvas_path, quality=95)

def generar_audio_locucion(texto_guion, salida_audio_path):
    tts = gTTS(text=texto_guion, lang='es', tld='com.mx')
    tts.save(salida_audio_path)

def obtener_duracion_audio(audio_path):
    cmd = [FFMPEG_EXE, '-i', audio_path]
    res = subprocess.run(cmd, capture_output=True, text=True)
    for line in res.stderr.split('\n'):
        if 'Duration:' in line:
            parts = line.split('Duration:')[1].split(',')[0].strip()
            h, m, s = parts.split(':')
            return float(h)*3600 + float(m)*60 + float(s)
    return 25.0

def renderizar_video_reel(canvas_path, audio_path, salida_video_path):
    duracion = obtener_duracion_audio(audio_path) + 0.8
    fps = 30
    total_frames = int(duracion * fps)

    cmd = [
        FFMPEG_EXE, '-y',
        '-loop', '1',
        '-i', canvas_path,
        '-i', audio_path,
        '-filter_complex',
        f"[0:v]scale=1080:1920,zoompan=z='min(zoom+0.0003,1.06)':d={total_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps={fps}[v]",
        '-map', '[v]',
        '-map', '1:a',
        '-c:v', 'libx264',
        '-preset', 'fast',
        '-crf', '20',
        '-pix_fmt', 'yuv420p',
        '-c:a', 'aac',
        '-b:a', '192k',
        '-t', str(duracion),
        salida_video_path
    ]

    subprocess.run(cmd, capture_output=True, text=True)
    return os.path.exists(salida_video_path) and os.path.getsize(salida_video_path) > 1000

# Guiones optimizados para formato TikTok (30-40 segundos dinámicos)
GUIONES_ACERO = {
    2: (
        "¡Despierta! Mañana es el día favorito del que nunca logra nada. "
        "El procrastinador es un cobarde que vive negociando con su propia mediocridad. "
        "El éxito se construye hoy o no se construye nunca. "
        "Aplica la regla de la ejecución inmediata: si tienes que hacerlo, no lo pienses, actúa. "
        "Borra la palabra mañana de tu vocabulario y cumple la promesa que te hiciste frente al espejo. "
        "Toca dos veces la pantalla si hoy tomas el control de tu destino."
    ),
    3: (
        "¡Despierta! Quien no controla sus emociones, será siempre el esclavo de quien sepa provocarlo. "
        "El frágil emocional se ofende por todo y vive mendigando aprobación ajena. "
        "Esa debilidad te destruye. Al mundo no le importa cómo te sientes hoy, al mundo le importan tus resultados. "
        "El Hombre de Acero no reacciona por impulso; domina su mente y ejecuta con frialdad. "
        "Forja una voluntad inquebrantable. Comenta un 'acero' si hoy blindas tu mente contra todo."
    ),
    4: (
        "¡Despierta! Los atajos en la vida casi siempre conducen a los callejones sin salida de la mediocridad. "
        "Dejá de buscar el truco fácil. La caballería no viene a salvarte, eres tú contra ti mismo. "
        "El dolor es el peaje obligatorio hacia la grandeza. "
        "Abraza la incomodidad, ejecuta sin pedirle permiso a tus emociones y paga el precio completo por adelantado. "
        "Toca dos veces y comparte este video con quien necesite despertar hoy."
    ),
    5: (
        "¡Despierta! El que edifica su valor sobre el aplauso ajeno, se derrumba en cuanto llega el silencio. "
        "Deja de mendigar la aprobación de gente a la que no le importas. "
        "El Hombre de Acero no busca aplausos, busca resultados. "
        "Construye tu imperio en la oscuridad, en la soledad de la madrugada, donde nadie está mirando. "
        "Deja que tus hechos hablen por ti. Si estás listo para trabajar en silencio, deja tu like."
    ),
    6: (
        "¡Despierta! El fracaso no es lo contrario al éxito, el fracaso es la materia prima con la que se forja la victoria. "
        "Deja de llorar por tus caídas. Cada error es solo información para volver a atacar con más fuerza. "
        "Asume el cien por ciento de la responsabilidad y acostúmbrate al fuego de la dificultad. "
        "La motivación es para débiles; la disciplina es levantarte y hacer el trabajo te guste o no. "
        "Toca dos veces si no te rindes jamás."
    ),
    7: (
        "¡Despierta! La envidia es el tributo involuntario que la mediocridad le rinde al talento y al trabajo. "
        "Mientras tú te quejas del éxito de otros, alguien más está entrenando en silencio y durmiendo menos. "
        "Muta el resentimiento en trabajo duro. Tu cuerpo, tu dinero y tu mente son el resultado directo de tus decisiones. "
        "Elige tu bando: espectador mediocre o conquistador de tu destino."
    ),
    8: (
        "¡Despierta! El confort es una prisión silenciosa que asesina más sueños que cualquier fracaso. "
        "Estás vendiendo tu grandeza por la miseria de un sofá cómodo y una rutina blanda. "
        "El dolor del esfuerzo es temporal, pero el peso del arrepentimiento dura toda la vida. "
        "Abraza la incomodidad todos los días como si tu vida dependiera de ello. Porque así es. "
        "Toca dos veces si hoy sales de tu zona cómoda."
    ),
    9: (
        "¡Despierta! No le cuentes a nadie lo que vas a hacer, deja que el ruido de tus resultados hable por ti. "
        "El mundo está lleno de tipos que inflan el pecho contando sus planes y a las dos semanas no hicieron nada. "
        "Calla la boca, trágate tus palabras y ejecuta en silencio. "
        "Que cuando salgas a la luz, la contundencia de tus actos retumbe tan fuerte que nadie pueda dudar. "
        "Comenta 'acero' si trabajas sin hacer ruido."
    ),
    10: (
        "¡Despierta! A nadie le importa cuánto dolió tu pasado si hoy sigues usándolo como excusa para fracasar. "
        "Tu pasado fue tu campo de entrenamiento, no la condena perpetua de tu destino. "
        "Quema el traje de víctima. Si ya probaste el barro, nada que la vida te tire encima hoy puede intimidarte. "
        "Mata a tu viejo yo y forja al Hombre de Acero. Guarda este video para cuando flaquees."
    )
}

def main():
    os.makedirs("videos_reels", exist_ok=True)
    json_path = "mentalidad_de_acero/publicaciones.json"

    if not os.path.exists(json_path):
        print("❌ No existe publicaciones.json")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        posts = json.load(f)

    index_videos = []
    index_file = "videos_reels/videos_index.json"
    if os.path.exists(index_file):
        with open(index_file, "r", encoding="utf-8") as f:
            index_videos = json.load(f)

    print("="*65)
    print("🎬 GENERADOR EN BATERÍA DE REELS / TIKTOKS (POSTS 2 AL 10)")
    print("="*65)

    exitosos = 0
    for p in posts:
        pid = p["id"]
        if pid < 2 or pid > 10:
            continue

        img_path = p.get("imagen")
        if not img_path or not os.path.exists(img_path):
            print(f"⚠️ Imagen no encontrada para post #{pid}: {img_path}")
            continue

        slug = p.get("arquetipo", f"post_{pid}").lower().replace(" ", "_")
        canvas_path = f"videos_reels/canvas_post_{pid}.jpg"
        audio_path = f"videos_reels/audio_post_{pid}.mp3"
        video_path = f"videos_reels/reel_post_{pid}_{slug}.mp4"

        print(f"\n[Procesando Post #{pid}] ⚔️ {p.get('arquetipo')}...")

        # 1. Canvas 9:16
        if not os.path.exists(canvas_path):
            print("  🎨 Creando lienzo 9:16...")
            preparar_lienzo_vertical(img_path, canvas_path, titulo_superior="• MENTALIDAD DE ACERO •")

        # 2. Audio locución
        guion = GUIONES_ACERO.get(pid, p.get("texto", "")[:350])
        if not os.path.exists(audio_path):
            print("  🎙️ Generando locución en off...")
            generar_audio_locucion(guion, audio_path)

        # 3. Render video
        if not os.path.exists(video_path):
            print("  🎬 Renderizando video MP4 con FFmpeg...")
            ok = renderizar_video_reel(canvas_path, audio_path, video_path)
            if ok:
                mb = os.path.getsize(video_path) / 1024 / 1024
                print(f"  ✅ ¡Video #{pid} listo! ({mb:.2f} MB)")
                exitosos += 1
                index_videos.append({
                    "id": pid,
                    "arquetipo": p.get("arquetipo"),
                    "archivo_video": video_path,
                    "archivo_audio": audio_path,
                    "tamano_mb": round(mb, 2),
                    "guion": guion
                })
                with open(index_file, "w", encoding="utf-8") as f:
                    json.dump(index_videos, f, ensure_ascii=False, indent=2)
        else:
            print(f"  ⏩ Video ya existe: {video_path}")

    print("\n" + "="*65)
    print(f"🎉 FINALIZADO: {exitosos} nuevos videos generados para TikTok / Reels.")
    print(f"📁 Consulta el índice en: {index_file}")
    print("="*65)

if __name__ == "__main__":
    main()
