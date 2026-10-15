# ============================================================
# GENERADOR DE REELS CINEMÁTICOS MULTI-ESCENA (PERRITOS)
# ------------------------------------------------------------
# 1. 4 tomas de cámara cinemáticas (push-in, pan-up, pull-out, pan-side).
# 2. Música emotiva de piano de fondo mezclada en estéreo.
# 3. Subtítulos dinámicos de alto impacto visual con diseño redondeado.
# 4. Formato vertical 1080x1920 (9:16) H.264 / AAC listo para Reels y TikTok.
# ============================================================

import os
import sys
import json
import subprocess
import requests
import imageio_ffmpeg
from PIL import Image, ImageFilter, ImageDraw, ImageFont
from gtts import gTTS

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()
OUTPUT_DIR = "videos_reels_cinematicos"
CACHE_DIR = "clips_cache"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(CACHE_DIR, exist_ok=True)

CONFIG_PATH = "config.json"
BG_MUSIC_PATH = "assets_musica/piano_emotivo.mp3"

def cargar_keys():
    pexels_key = os.getenv("PEXELS_API_KEY", "")
    pixabay_key = os.getenv("PIXABAY_API_KEY", "")
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                pexels_key = pexels_key or cfg.get("PEXELS_API_KEY", "")
                pixabay_key = pixabay_key or cfg.get("PIXABAY_API_KEY", "")
        except:
            pass
    return pexels_key, pixabay_key

def descargar_clip_pexels(query, salida_path, api_key):
    """
    Descarga un clip de video vertical HD de Pexels automáticamente.
    """
    if not api_key:
        return None
    try:
        url = f"https://api.pexels.com/videos/search?query={requests.utils.quote(query)}&orientation=portrait&per_page=8"
        headers = {"Authorization": api_key, "User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=12).json()
        videos = res.get("videos", [])
        for v in videos:
            files = v.get("video_files", [])
            for f in files:
                if f.get("file_type") == "video/mp4" and f.get("height", 0) >= f.get("width", 0):
                    link = f.get("link")
                    if link:
                        r = requests.get(link, stream=True, timeout=25)
                        with open(salida_path, "wb") as out:
                            for chunk in r.iter_content(chunk_size=1024*1024):
                                out.write(chunk)
                        return salida_path
    except Exception as e:
        print(f"   [Pexels API] Aviso al descargar '{query}': {e}")
    return None

def descargar_clip_pixabay(query, salida_path, api_key, clip_index=0):
    """
    Descarga un clip de video de Pixabay automáticamente.
    """
    if not api_key:
        return None
    try:
        url = f"https://pixabay.com/api/videos/?key={api_key}&q={requests.utils.quote(query)}&per_page=15"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=12).json()
        hits = res.get("hits", [])
        if hits:
            # Reordenar para seleccionar según clip_index
            h_sel = hits[clip_index % len(hits)]
            videos = h_sel.get("videos", {})
            v_obj = videos.get("large") or videos.get("medium") or videos.get("small")
            if v_obj and v_obj.get("url"):
                r = requests.get(v_obj["url"], headers=headers, stream=True, timeout=25)
                with open(salida_path, "wb") as out:
                    for chunk in r.iter_content(chunk_size=1024*1024):
                        out.write(chunk)
                return salida_path
    except Exception as e:
        print(f"   [Pixabay API] Aviso al descargar '{query}': {e}")
    return None

def generar_audio_locucion(texto, salida_audio):
    tts = gTTS(text=texto, lang='es', tld='com.mx')
    tts.save(salida_audio)
    return salida_audio

def obtener_duracion(media_path):
    cmd = [FFMPEG_EXE, "-i", media_path]
    p = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    for line in p.stderr.splitlines():
        if "Duration" in line:
            part = line.split("Duration:")[1].split(",")[0].strip()
            h, m, s = part.split(":")
            return float(h)*3600 + float(m)*60 + float(s)
    return 30.0

def generar_toma_dinamica(imagen_path, salida_toma_path, tipo_movimiento, duracion=7.0):
    img_orig = Image.open(imagen_path).convert("RGB")
    ancho_orig, alto_orig = img_orig.size

    canvas_w = 1080
    canvas_h = 1920

    # Fondo difuminado de alta calidad
    ratio = max(canvas_w / ancho_orig, canvas_h / alto_orig)
    bg_w = int(ancho_orig * ratio)
    bg_h = int(alto_orig * ratio)
    bg = img_orig.resize((bg_w, bg_h), Image.Resampling.LANCZOS)
    left = (bg_w - canvas_w) // 2
    top = (bg_h - canvas_h) // 2
    bg = bg.crop((left, top, left + canvas_w, top + canvas_h))
    bg = bg.filter(ImageFilter.GaussianBlur(radius=28))
    darkener = Image.new("RGB", (canvas_w, canvas_h), (5, 10, 20))
    bg = Image.blend(bg, darkener, alpha=0.55)

    # Imagen central enfocada
    target_w = 1020
    target_h = int(alto_orig * (target_w / ancho_orig))
    if target_h > 1400:
        target_h = 1400
        target_w = int(ancho_orig * (target_h / alto_orig))

    img_central = img_orig.resize((target_w, target_h), Image.Resampling.LANCZOS)
    pos_x = (canvas_w - target_w) // 2
    pos_y = (canvas_h - target_h) // 2
    bg.paste(img_central, (pos_x, pos_y))

    temp_canvas = salida_toma_path + ".jpg"
    bg.save(temp_canvas, quality=95)

    frames = int(duracion * 30)

    if tipo_movimiento == 'push_in':
        vf = f"zoompan=z='min(zoom+0.0006,1.15)':d={frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30,format=yuv420p"
    elif tipo_movimiento == 'pull_out':
        vf = f"zoompan=z='if(lte(zoom,1.0),1.15,max(1.0,zoom-0.0006))':d={frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30,format=yuv420p"
    elif tipo_movimiento == 'pan_up':
        vf = f"zoompan=z=1.08:d={frames}:x='iw/2-(iw/zoom/2)':y='(ih/2-(ih/zoom/2))*(1-on/{frames})':s=1080x1920:fps=30,format=yuv420p"
    else:
        vf = f"zoompan=z=1.08:d={frames}:x='(iw/2-(iw/zoom/2))*(on/{frames})':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30,format=yuv420p"

    cmd = [
        FFMPEG_EXE, "-y",
        "-loop", "1",
        "-i", temp_canvas,
        "-vf", vf,
        "-t", str(duracion),
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "20",
        salida_toma_path
    ]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    if os.path.exists(temp_canvas):
        os.remove(temp_canvas)

    return salida_toma_path

def crear_overlay_subtitulo(texto, badge_superior, salida_png, canvas_w=1080, canvas_h=1920):
    """
    Crea una capa PNG transparente con diseño profesional de subtítulos estilo CapCut.
    """
    img = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    font_path_bold = "C:\\Windows\\Fonts\\arialbd.ttf"
    font_path_regular = "C:\\Windows\\Fonts\\arial.ttf"

    font_badge = ImageFont.truetype(font_path_bold, 36)
    font_sub = ImageFont.truetype(font_path_bold, 44)
    font_foot = ImageFont.truetype(font_path_bold, 28)

    # 1. Badge superior
    bbox_b = draw.textbbox((0, 0), badge_superior, font=font_badge)
    bw = bbox_b[2] - bbox_b[0]
    bh = bbox_b[3] - bbox_b[1]
    bx = (canvas_w - bw) // 2
    by = 160
    draw.rounded_rectangle([bx - 32, by - 14, bx + bw + 32, by + bh + 14], radius=18, fill=(15, 23, 42, 230), outline=(52, 211, 153, 255), width=3)
    draw.text((bx, by), badge_superior, fill=(255, 255, 255, 255), font=font_badge)

    # 2. Caja de subtítulos centrada
    lineas = texto.strip().split("\n")
    line_h = 56
    total_h = len(lineas) * line_h
    max_w = 0
    for l in lineas:
        b = draw.textbbox((0, 0), l, font=font_sub)
        max_w = max(max_w, b[2] - b[0])

    cx = (canvas_w - max_w) // 2
    cy = canvas_h - 430
    draw.rounded_rectangle([cx - 36, cy - 20, cx + max_w + 36, cy + total_h + 18], radius=24, fill=(2, 6, 23, 225), outline=(250, 204, 21, 255), width=3)

    for i, l in enumerate(lineas):
        b = draw.textbbox((0, 0), l, font=font_sub)
        lw = b[2] - b[0]
        lx = (canvas_w - lw) // 2
        ly = cy + i * line_h
        color = (253, 224, 71, 255) if i == 0 else (255, 255, 255, 255)
        draw.text((lx, ly), l, fill=color, font=font_sub)

    # 3. Footer emocional
    foot_text = "TOCA DOS VECES POR ESTA SEGUNDA OPORTUNIDAD"
    bbox_f = draw.textbbox((0, 0), foot_text, font=font_foot)
    fw = bbox_f[2] - bbox_f[0]
    fx = (canvas_w - fw) // 2
    fy = canvas_h - 220
    draw.rounded_rectangle([fx - 28, fy - 10, fx + fw + 28, fy + 42], radius=14, fill=(5, 150, 105, 235))
    draw.text((fx, fy), foot_text, fill=(255, 255, 255, 255), font=font_foot)

    img.save(salida_png, "PNG")
    return salida_png

def generar_reel_cinematico(datos_historia):
    id_historia = datos_historia["id"]
    nombre = datos_historia["nombre_perrito"]
    print(f"\n🎬 [INICIANDO REEL CINEMÁTICO] #{id_historia} - {nombre}")

    # 1. Generar audio
    audio_voz_path = os.path.join(CACHE_DIR, f"voz_cinematica_{id_historia}.mp3")
    generar_audio_locucion(datos_historia["guion"], audio_voz_path)
    duracion = obtener_duracion(audio_voz_path) + 1.0
    print(f"   🎙️ Locución generada. Duración: {duracion:.1f} segundos.")

    # 2. Mezclar música de piano
    audio_mix_path = os.path.join(CACHE_DIR, f"audio_mix_{id_historia}.mp3")
    if os.path.exists(BG_MUSIC_PATH):
        cmd_audio = [
            FFMPEG_EXE, "-y",
            "-i", audio_voz_path,
            "-i", BG_MUSIC_PATH,
            "-filter_complex",
            f"[1:a]volume=0.18,afade=t=in:st=0:d=1.5,afade=t=out:st={duracion-2.0:.1f}:d=2[bg];[0:a][bg]amix=inputs=2:duration=first[aout]",
            "-map", "[aout]",
            "-b:a", "192k",
            audio_mix_path
        ]
        subprocess.run(cmd_audio, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        print(f"   🎵 Música de piano emotiva mezclada con la voz.")
    else:
        audio_mix_path = audio_voz_path

    # 3. Generar las 4 tomas de cámara (reales o cinemáticas dinámicas)
    dur_toma = duracion / 4.0
    tomas = []
    movimientos = ['push_in', 'pan_up', 'pull_out', 'pan_side']
    queries = ["abandoned sad dog", "dog rescue hand", "happy dog playing", "dog looking at camera"]
    pexels_key, pixabay_key = cargar_keys()

    for idx, mov in enumerate(movimientos):
        toma_path = os.path.join(CACHE_DIR, f"toma_{id_historia}_{idx+1}.mp4")
        clip_real = None
        if pexels_key:
            clip_real = descargar_clip_pexels(queries[idx], toma_path, pexels_key)
        elif pixabay_key:
            clip_real = descargar_clip_pixabay(queries[idx], toma_path, pixabay_key, clip_index=id_historia + idx)

        if clip_real and os.path.exists(clip_real) and os.path.getsize(clip_real) > 10000:
            print(f"   🎥 Clip real de video #{idx+1} descargado ({queries[idx]}).")
            toma_ajustada = os.path.join(CACHE_DIR, f"toma_ajustada_{id_historia}_{idx+1}.mp4")
            cmd_clip = [
                FFMPEG_EXE, "-y",
                "-stream_loop", "-1",
                "-i", clip_real,
                "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1",
                "-t", str(dur_toma),
                "-r", "30",
                "-pix_fmt", "yuv420p",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                toma_ajustada
            ]
            subprocess.run(cmd_clip, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            tomas.append(toma_ajustada if os.path.exists(toma_ajustada) else clip_real)
        else:
            print(f"   🎥 Renderizando Toma Cinemática #{idx+1}/4 ({mov}) de {dur_toma:.1f}s...")
            generar_toma_dinamica(datos_historia["imagen"], toma_path, mov, duracion=dur_toma)
            tomas.append(toma_path)

    # 4. Concatenar tomas
    concat_list_path = os.path.join(CACHE_DIR, f"concat_{id_historia}.txt")
    with open(concat_list_path, "w", encoding="utf-8") as f:
        for t in tomas:
            f.write(f"file '{os.path.abspath(t).replace(chr(92), '/')}'\n")

    video_concatenado = os.path.join(CACHE_DIR, f"video_concat_{id_historia}.mp4")
    cmd_concat = [
        FFMPEG_EXE, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_list_path,
        "-c", "copy",
        video_concatenado
    ]
    subprocess.run(cmd_concat, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

    # 5. Generar overlays PNG de subtítulos para cada frase
    frases = datos_historia["frases_subtitulos"]
    num_frases = len(frases)
    tiempo_por_frase = duracion / max(num_frases, 1)

    overlays = []
    for idx_f, f_txt in enumerate(frases):
        overlay_png = os.path.join(CACHE_DIR, f"sub_{id_historia}_{idx_f+1}.png")
        crear_overlay_subtitulo(f_txt, "• HUELLAS CON PROPÓSITO •", overlay_png)
        overlays.append((overlay_png, idx_f * tiempo_por_frase, (idx_f + 1) * tiempo_por_frase))

    # 6. Componer overlays con ffmpeg
    filter_chains = []
    current_input = "[0:v]"

    cmd_final = [FFMPEG_EXE, "-y", "-i", video_concatenado]
    for idx_f, (png_path, t_in, t_out) in enumerate(overlays):
        cmd_final.extend(["-i", png_path])
        input_idx = idx_f + 1
        output_label = f"[v{input_idx}]" if idx_f < len(overlays) - 1 else "[vfinal]"
        filter_chains.append(f"{current_input}[{input_idx}:v]overlay=enable='between(t,{t_in:.2f},{t_out:.2f})'{output_label}")
        current_input = f"[v{input_idx}]"

    cmd_final.extend(["-i", audio_mix_path])
    audio_idx = len(overlays) + 1

    salida_final_mp4 = os.path.join(OUTPUT_DIR, f"reel_cinematico_{id_historia}_{nombre.lower()}.mp4")

    cmd_final.extend([
        "-filter_complex", ";".join(filter_chains),
        "-map", "[vfinal]",
        "-map", f"{audio_idx}:a",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "21",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        "-movflags", "+faststart",
        salida_final_mp4
    ])

    print(f"   ✨ Ensamblando Reel cinematográfico con música y subtítulos dinámicos...")
    subprocess.run(cmd_final, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

    tamano_mb = round(os.path.getsize(salida_final_mp4) / (1024 * 1024), 2)
    print(f"   🎉 ¡REEL CINEMÁTICO COMPLETADO!: {salida_final_mp4} ({tamano_mb} MB)\n")

    return salida_final_mp4

HISTORIA_EJEMPLO = {
    "id": 1,
    "nombre_perrito": "Tinaco",
    "imagen": "noviembre/perritos/nov_002_2026-11-01_perrito_1230.jpg",
    "guion": (
        "Lo dejaron atado con un cable en la azotea bajo el sol ardiente. "
        "Durante tres días enteros, los vecinos le pasaron agua con un tubo para mantenerlo con vida. "
        "Cuando llegaron los bomberos, temblaba de dolor pero les lamió las manos con infinita gratitud. "
        "Hoy Tinaco corre en la sombra de un jardín y duerme en una cama calientita. "
        "El sol nunca más volverá a quemarlo. Síguenos para salvar más vidas."
    ),
    "frases_subtitulos": [
        "LO DEJARON ATADO EN LA AZOTEA\nBAJO EL SOL ARDIENTE",
        "LOS VECINOS LE PASABAN AGUA\nCON UN TUBO PARA SALVARLO",
        "LOS BOMBEROS CORTARON EL CABLE\nQUE LO LASTIMABA",
        "PESABA APENAS 7 KILOS\nPERO NO DEJABA DE AGRADECER",
        "HOY DUERME FELIZ\nEN SU NUEVO HOGAR"
    ]
}

if __name__ == "__main__":
    generar_reel_cinematico(HISTORIA_EJEMPLO)
