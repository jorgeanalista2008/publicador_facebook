# ============================================================
# GENERADOR AUTOMÁTICO DE REELS / TIKTOK EN PYTHON + FFMPEG
# ------------------------------------------------------------
# 1. Convierte publicaciones (fotos/infografías) en formato vertical 9:16 (1080x1920).
# 2. Genera locución con IA (voz en off) usando gTTS.
# 3. Añade efectos de movimiento (Ken Burns zoom lento).
# 4. Exporta video MP4 en H.264 / AAC listo para TikTok, Instagram Reels y YouTube Shorts.
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

def preparar_lienzo_vertical(imagen_origen_path, salida_canvas_path, titulo_superior="⚔️ MENTALIDAD DE ACERO"):
    """
    Toma una imagen (4:5 o cualquier proporción) y la monta en un lienzo 9:16 (1080x1920)
    con fondo desenfocado cinematográfico y barra superior elegante.
    """
    img_orig = Image.open(imagen_origen_path).convert("RGB")
    ancho_orig, alto_orig = img_orig.size

    canvas_w = 1080
    canvas_h = 1920

    # 1. Fondo: Escalar y desenfocar para rellenar todo el 9:16
    ratio = max(canvas_w / ancho_orig, canvas_h / alto_orig)
    bg_w = int(ancho_orig * ratio)
    bg_h = int(alto_orig * ratio)
    bg = img_orig.resize((bg_w, bg_h), Image.Resampling.LANCZOS)
    left = (bg_w - canvas_w) // 2
    top = (bg_h - canvas_h) // 2
    bg = bg.crop((left, top, left + canvas_w, top + canvas_h))
    bg = bg.filter(ImageFilter.GaussianBlur(radius=25))

    # Oscurecer fondo para contraste cinematográfico
    darkener = Image.new("RGB", (canvas_w, canvas_h), (0, 0, 0))
    bg = Image.blend(bg, darkener, alpha=0.55)

    # 2. Imagen central: Escalar para que quepa perfectamente centrada (ancho 1000px aprox)
    target_w = 1000
    target_h = int(alto_orig * (target_w / ancho_orig))
    if target_h > 1450:
        target_h = 1450
        target_w = int(ancho_orig * (target_h / alto_orig))

    img_central = img_orig.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    # Sombra elegante alrededor de la imagen central
    pos_x = (canvas_w - target_w) // 2
    pos_y = (canvas_h - target_h) // 2 + 30

    # Pegar imagen principal
    bg.paste(img_central, (pos_x, pos_y))

    # 3. Dibujar barra de título superior
    draw = ImageDraw.Draw(bg)
    font_path = "C:\\Windows\\Fonts\\impact.ttf" if os.path.exists("C:\\Windows\\Fonts\\impact.ttf") else "C:\\Windows\\Fonts\\arialbd.ttf"
    try:
        font_header = ImageFont.truetype(font_path, 46)
        font_sub = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 26)
    except:
        font_header = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    # Badge superior
    badge_text = titulo_superior.replace("⚔️", "•").replace("🐾", "•")
    bbox = draw.textbbox((0, 0), badge_text, font=font_header)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    bx = (canvas_w - tw) // 2
    by = pos_y - 120

    # Fondo redondeado para el badge
    pad_x, pad_y = 35, 12
    draw.rounded_rectangle([bx - pad_x, by - pad_y, bx + tw + pad_x, by + th + pad_y], radius=20, fill=(15, 23, 42), outline=(234, 179, 8), width=3)
    draw.text((bx, by), badge_text, fill=(255, 255, 255), font=font_header)

    # Indicador inferior
    footer_text = "TOCA DOS VECES SI ASUMES EL RETO"
    bbox_f = draw.textbbox((0, 0), footer_text, font=font_sub)
    fw = bbox_f[2] - bbox_f[0]
    draw.text(((canvas_w - fw) // 2, pos_y + target_h + 40), footer_text, fill=(203, 213, 225), font=font_sub)

    bg.save(salida_canvas_path, quality=95)
    print(f"✅ Lienzo vertical 9:16 generado en: {salida_canvas_path}")

def generar_audio_locucion(texto_guion, salida_audio_path):
    """
    Genera la locución en audio mp3 con voz en español natural.
    """
    print("🎙️ Generando locución de audio con IA...")
    tts = gTTS(text=texto_guion, lang='es', tld='com.mx')
    tts.save(salida_audio_path)
    print(f"✅ Audio generado con éxito en: {salida_audio_path}")

def obtener_duracion_audio(audio_path):
    """
    Obtiene la duración en segundos del audio usando ffmpeg.
    """
    cmd = [
        FFMPEG_EXE, '-i', audio_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    for line in res.stderr.split('\n'):
        if 'Duration:' in line:
            parts = line.split('Duration:')[1].split(',')[0].strip()
            h, m, s = parts.split(':')
            return float(h)*3600 + float(m)*60 + float(s)
    return 15.0

def renderizar_video_reel(canvas_path, audio_path, salida_video_path):
    """
    Combina la imagen con zoom sutil cinematográfico y el audio usando FFmpeg.
    """
    duracion = obtener_duracion_audio(audio_path) + 1.0 # 1 segundo extra de gracia
    print(f"🎬 Renderizando video TikTok/Reel (Duración: {duracion:.1f}s)...")

    # Filtro zoom sutil: zoom lento de 1.0 a 1.06
    # y merge con el audio
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

    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(salida_video_path) and os.path.getsize(salida_video_path) > 1000:
        print(f"🎉 ¡VIDEO GENERADO EXITOSAMENTE!\n📁 Archivo: {salida_video_path}\n📊 Tamaño: {os.path.getsize(salida_video_path)/1024/1024:.2f} MB")
        return True
    else:
        print("❌ Error en FFmpeg:", res.stderr[-500:])
        return False

def main():
    os.makedirs("videos_reels", exist_ok=True)

    # Ejemplo de prueba con Metalidad de Acero
    imagen_ejemplo = "mentalidad_de_acero/imagenes/post_1_el_pobrecito.jpg"
    canvas_salida = "videos_reels/canvas_post_1.jpg"
    audio_salida = "videos_reels/audio_post_1.mp3"
    video_salida = "videos_reels/reel_post_1_el_pobrecito.mp4"

    guion_locucion = (
        "¡Despierta! La pobreza puede ser una circunstancia, pero la mentalidad de víctima es una prisión. "
        "A nadie le importan tus excusas. Cada vez que te quejas, le entregas el control de tu vida a tus circunstancias. "
        "Escúchame bien: Nadie vendrá a salvarte. "
        "El dolor es inevitable, pero el Hombre de Acero lo usa como combustible. "
        "Mata la queja en seco, asume el cien por ciento de la responsabilidad y sal a conquistar tu destino. "
        "Deja un 'acero' en los comentarios si hoy rompes tus cadenas."
    )

    print("="*65)
    print("🚀 GENERADOR AUTOMÁTICO DE VIDEO VIRAL PARA TIKTOK / REELS")
    print("="*65)

    preparar_lienzo_vertical(imagen_ejemplo, canvas_salida, titulo_superior="⚔️ MENTALIDAD DE ACERO")
    generar_audio_locucion(guion_locucion, audio_salida)
    renderizar_video_reel(canvas_salida, audio_salida, video_salida)

if __name__ == "__main__":
    main()
