# ============================================================
# GENERADOR AUTOMÁTICO DE REELS PARA "HUELLAS CON PROPÓSITO"
# ------------------------------------------------------------
# Convierte historias reales de perritos en videos verticales 9:16
# con locución emotiva, movimiento cinemático y formato listo para
# Instagram Reels y TikTok.
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
OUTPUT_DIR = "videos_reels_perritos"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def preparar_lienzo_perrito(imagen_origen_path, salida_canvas_path, titulo_perrito="• HUELLAS CON PROPÓSITO •"):
    """
    Crea un lienzo vertical 9:16 (1080x1920) cinematográfico para historias de perritos.
    """
    if not os.path.exists(imagen_origen_path):
        raise FileNotFoundError(f"No existe la imagen: {imagen_origen_path}")

    img_orig = Image.open(imagen_origen_path).convert("RGB")
    ancho_orig, alto_orig = img_orig.size

    canvas_w = 1080
    canvas_h = 1920

    # 1. Fondo difuminado de alta calidad
    ratio = max(canvas_w / ancho_orig, canvas_h / alto_orig)
    bg_w = int(ancho_orig * ratio)
    bg_h = int(alto_orig * ratio)
    bg = img_orig.resize((bg_w, bg_h), Image.Resampling.LANCZOS)
    left = (bg_w - canvas_w) // 2
    top = (bg_h - canvas_h) // 2
    bg = bg.crop((left, top, left + canvas_w, top + canvas_h))
    bg = bg.filter(ImageFilter.GaussianBlur(radius=30))

    # Oscurecer fondo sutilmente para contraste
    darkener = Image.new("RGB", (canvas_w, canvas_h), (10, 15, 29))
    bg = Image.blend(bg, darkener, alpha=0.6)

    # 2. Imagen central del perrito
    target_w = 1000
    target_h = int(alto_orig * (target_w / ancho_orig))
    if target_h > 1350:
        target_h = 1350
        target_w = int(ancho_orig * (target_h / alto_orig))

    img_central = img_orig.resize((target_w, target_h), Image.Resampling.LANCZOS)
    pos_x = (canvas_w - target_w) // 2
    pos_y = (canvas_h - target_h) // 2 + 10

    # Pegar imagen principal
    bg.paste(img_central, (pos_x, pos_y))

    # 3. Dibujar elementos gráficos
    draw = ImageDraw.Draw(bg)
    font_header_path = "C:\\Windows\\Fonts\\arialbd.ttf" if os.path.exists("C:\\Windows\\Fonts\\arialbd.ttf") else None
    font_sub_path = "C:\\Windows\\Fonts\\arial.ttf" if os.path.exists("C:\\Windows\\Fonts\\arial.ttf") else None

    try:
        font_header = ImageFont.truetype(font_header_path, 40) if font_header_path else ImageFont.load_default()
        font_sub = ImageFont.truetype(font_sub_path, 28) if font_sub_path else ImageFont.load_default()
    except:
        font_header = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    # Badge superior de Huellas con Propósito
    badge_text = titulo_perrito
    bbox = draw.textbbox((0, 0), badge_text, font=font_header)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    bx = (canvas_w - tw) // 2
    by = pos_y - 110

    pad_x, pad_y = 35, 12
    draw.rounded_rectangle([bx - pad_x, by - pad_y, bx + tw + pad_x, by + th + pad_y], radius=20, fill=(15, 23, 42), outline=(52, 211, 153), width=3)
    draw.text((bx, by), badge_text, fill=(255, 255, 255), font=font_header)

    # Indicador inferior emocional
    footer_text = "🐾 TOCA DOS VECES POR ESTA SEGUNDA OPORTUNIDAD ❤️"
    bbox_f = draw.textbbox((0, 0), footer_text, font=font_sub)
    fw = bbox_f[2] - bbox_f[0]
    draw.text(((canvas_w - fw) // 2, pos_y + target_h + 40), footer_text, fill=(241, 245, 249), font=font_sub)

    bg.save(salida_canvas_path, quality=95)
    return salida_canvas_path

def generar_audio_perrito(texto_guion, salida_audio_path):
    """
    Genera voz en off con tono cálido en español latinoamericano.
    """
    tts = gTTS(text=texto_guion, lang='es', tld='com.mx')
    tts.save(salida_audio_path)
    return salida_audio_path

def obtener_duracion_audio(audio_path):
    cmd = [
        FFMPEG_EXE, "-i", audio_path
    ]
    p = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    for line in p.stderr.splitlines():
        if "Duration" in line:
            part = line.split("Duration:")[1].split(",")[0].strip()
            h, m, s = part.split(":")
            return float(h)*3600 + float(m)*60 + float(s)
    return 30.0

def compilar_video_reel(canvas_path, audio_path, salida_mp4_path):
    """
    Crea el video MP4 1080x1920 a 30 fps con zoom cinemático lento.
    """
    duracion = obtener_duracion_audio(audio_path) + 1.5
    total_frames = int(duracion * 30)

    vf_filter = (
        f"zoompan=z='min(zoom+0.0003,1.06)':d={total_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30,"
        f"format=yuv420p"
    )

    cmd = [
        FFMPEG_EXE, "-y",
        "-loop", "1",
        "-i", canvas_path,
        "-i", audio_path,
        "-vf", vf_filter,
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "22",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        "-movflags", "+faststart",
        salida_mp4_path
    ]

    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    return salida_mp4_path

HISTORIAS_PERRITOS = [
    {
        "id": 1,
        "nombre_perrito": "Tinaco",
        "imagen": "noviembre/perritos/nov_002_2026-11-01_perrito_1230.jpg",
        "guion": (
            "Lo dejaron atado con un cable en la azotea de una casa vacía, bajo el sol ardiente. "
            "Durante días, los vecinos le pasaron comida y agua con un tubo, hasta que llegaron los bomberos a rescatarlo. "
            "Pesaba apenas siete kilos y temblaba de miedo, pero en cuanto le cortaron el cable, le lamió las manos a su salvador. "
            "Hoy vive feliz, corre bajo la sombra de un jardín y duerme en una cama calientita. "
            "El sol nunca más volverá a lastimarlo. Síguenos en Huellas con Propósito si crees en las segundas oportunidades."
        ),
        "caption": (
            "🐾 HISTORIA REAL: Lo dejaron en la azotea el día que entregaron las llaves.\n\n"
            "Doña Beatriz escuchó un llanto seco en la azotea de enfrente. Al asomarse, vio a este perrito atado a la pata de un tinaco bajo el sol del mediodía.\n\n"
            "Los vecinos se unieron para alimentarlo con un tubo de PVC hasta que los bomberos y la patrulla de vigilancia animal cortaron el cable que tenía incrustado en el cuello.\n\n"
            "Hoy vive con una familia que lo ama con locura. Su nombre es Tinaco de cariño, y el sol ya nunca más le quemará la espalda. ❤️\n\n"
            "🐕 Súmate a @huellasconproposito26 y comparte esta historia para salvar más vidas.\n\n"
            "#HuellasConPropósito #PerrosDeBarrio #RescateAnimal #HistoriasReales #AdoptaNoCompres #AmorAnimal"
        )
    },
    {
        "id": 2,
        "nombre_perrito": "Manchas",
        "imagen": "noviembre/perritos/nov_004_2026-11-01_perrito_2030.jpg",
        "guion": (
            "Cerraron la maderería para siempre y al guardia de seguridad le pagaron su sueldo, pero a Manchas lo dejaron encerrado detrás del portón. "
            "Pasó cinco días haciendo guardia frente a un negocio que ya no existía, esperando que alguien viniera a abrirle. "
            "Don Aurelio, un zapatero del barrio, no pudo soportar su mirada y rompió el candado para darle de comer. "
            "Hoy Manchas duerme sobre una alfombra en la zapatería, y cada cliente que entra recibe un lengüetazo de gratitud. "
            "La lealtad no se compra, se cuida. Deja un corazón si crees en el amor perruno."
        ),
        "caption": (
            "🐾 HISTORIA REAL: El vigilante nocturno que despidieron sin liquidación.\n\n"
            "Cerraron la maderería con cinta de clausura. Al personal le pagaron, pero a Manchas lo dejaron adentro como si fuera parte del inventario abandonado.\n\n"
            "Don Aurelio, el zapatero de la esquina, escuchó sus aullidos y lo rescató. Hoy Manchas es el nuevo guardián de la zapatería y no le falta amor ni comida. ❤️\n\n"
            "🐕 Súmate a @huellasconproposito26 para más historias reales que dejan huella.\n\n"
            "#HuellasConPropósito #PerrosDeBarrio #RescateAnimal #HistoriasReales #AdoptaNoCompres"
        )
    },
    {
        "id": 3,
        "nombre_perrito": "Pelusa",
        "imagen": "noviembre/perritos/nov_006_2026-11-02_perrito_1230.jpg",
        "guion": (
            "El camión de mudanza arrancó a toda velocidad. Minutos después, una cachorrita blanca salió corriendo del patio hacia la banqueta persiguiendo las llantas. "
            "Los vecinos pensaron que se les había escapado, pero pasaron las horas y nadie volvió por ella. "
            "Doña Carmela la recogió temblando en una esquina, sucia y con el corazón roto. "
            "Le tomó tres semanas volver a confiar en las caricias. Hoy es la reina consentida de la casa y nunca más volverá a correr detrás de un auto que la abandona. "
            "Toca dos veces la pantalla por Pelusa."
        ),
        "caption": (
            "🐾 HISTORIA REAL: Dijeron que se les olvidó subirla a la mudanza.\n\n"
            "Una cachorrita blanca persiguió desesperada el camión de sus dueños por dos cuadras antes de cansarse y quedarse en la banqueta llorando.\n\n"
            "Doña Carmela la cobijó, la llevó al veterinario y le devolvió las ganas de jugar. Los animales no son cosas que se desechan en una mudanza. ❤️\n\n"
            "🐕 Síguenos en @huellasconproposito26 si amas a los animales.\n\n"
            "#HuellasConPropósito #RescateAnimal #AdoptaNoCompres #HistoriasReales"
        )
    }
]

def renderizar_bateria():
    index_videos = []
    index_file = os.path.join(OUTPUT_DIR, "reels_perritos_index.json")

    for h in HISTORIAS_PERRITOS:
        vid_id = h["id"]
        nombre = h["nombre_perrito"].lower()
        canvas_path = os.path.join(OUTPUT_DIR, f"canvas_perrito_{vid_id}_{nombre}.jpg")
        audio_path = os.path.join(OUTPUT_DIR, f"audio_perrito_{vid_id}.mp3")
        video_path = os.path.join(OUTPUT_DIR, f"reel_perrito_{vid_id}_{nombre}.mp4")

        print(f"\n🐶 Generando Reel #{vid_id}: {h['nombre_perrito']}...")
        preparar_lienzo_perrito(h["imagen"], canvas_path, "• HUELLAS CON PROPÓSITO •")
        generar_audio_perrito(h["guion"], audio_path)
        compilar_video_reel(canvas_path, audio_path, video_path)

        size_mb = round(os.path.getsize(video_path) / (1024 * 1024), 2)
        print(f"🎬 Video generado con éxito: {video_path} ({size_mb} MB)")

        index_videos.append({
            "id": vid_id,
            "nombre_perrito": h["nombre_perrito"],
            "archivo_video": video_path.replace("\\", "/"),
            "tamano_mb": size_mb,
            "guion": h["guion"],
            "caption": h["caption"],
            "publicado_instagram": False
        })

    with open(index_file, "w", encoding="utf-8") as f:
        json.dump(index_videos, f, indent=2, ensure_ascii=False)
    print(f"\n🎉 ¡Batería de Reels de Perritos completada! Índice guardado en: {index_file}")

if __name__ == "__main__":
    renderizar_bateria()
