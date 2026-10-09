import os
import sys
import json
import requests
from PIL import Image, ImageDraw, ImageFont
import io

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

def obtener_api_key():
    if "GEMINI_API_KEY" in os.environ:
        return os.environ["GEMINI_API_KEY"]
    if os.path.exists("config.json"):
        with open("config.json", "r", encoding="utf-8") as f:
            cfg = json.load(f)
            return cfg.get("GEMINI_API_KEY", "")
    return ""

API_KEY = obtener_api_key()

def llamar_gemini(prompt_sistema, prompt_usuario):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={API_KEY}"
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": f"{prompt_sistema}\n\n{prompt_usuario}"}]
            }
        ],
        "generationConfig": {
            "temperature": 0.85,
            "topP": 0.95,
            "maxOutputTokens": 2048
        }
    }
    res = requests.post(url, json=payload).json()
    return res['candidates'][0]['content']['parts'][0]['text']

def crear_imagen_estilo_carlos_arias(filosofo, subtitulo, frase, output_path):
    # Dimensiones estándar para Facebook: 1080 x 1350 (formato vertical 4:5 de alto impacto)
    total_w, total_h = 1080, 1350
    border_w = 120 # Ancho de las barras laterales de color
    inner_w = total_w - (border_w * 2) # 840px de ancho central
    inner_h = total_h

    # 1. Color de las barras laterales (Naranja terracota cálido estilo Carlos Arias)
    bg_color = (235, 94, 20) # Naranja cálido potente
    img = Image.new("RGB", (total_w, total_h), color=bg_color)
    draw = ImageDraw.Draw(img)

    # 2. Descargar o generar arte alegórico central dramático (caminante en el fuego / tormenta)
    art_url = "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=900&auto=format&fit=crop&q=85"
    try:
        r = requests.get(art_url, timeout=10)
        art_img = Image.open(io.BytesIO(r.content)).convert("RGB")
        art_img = art_img.resize((inner_w, inner_h), Image.Resampling.LANCZOS)
    except Exception:
        # Fallback degradado dramático si no hay red
        art_img = Image.new("RGB", (inner_w, inner_h), color=(30, 20, 25))

    # Pegar arte en el centro entre las barras
    img.paste(art_img, (border_w, 0))

    # 3. Aplicar viñeta oscura en la parte superior para que el texto resalte con elegancia
    vignette = Image.new("RGBA", (inner_w, 420), color=(0, 0, 0, 0))
    v_draw = ImageDraw.Draw(vignette)
    for y in range(420):
        # Gradiente suave de negro a transparente
        alpha = int(220 * (1 - (y / 420)))
        v_draw.line([(0, y), (inner_w, y)], fill=(10, 10, 15, alpha))
    img.paste(vignette, (border_w, 0), vignette)

    # 4. Tipografía clásica
    font_default = ImageFont.load_default()
    
    # Intentar cargar fuentes del sistema (Times New Roman / Georgia / Garamond)
    font_filosofo = font_default
    font_sub = font_default
    font_frase = font_default

    fonts_to_try = [
        r"C:\Windows\Fonts\timesbd.ttf", # Times New Roman Bold
        r"C:\Windows\Fonts\georgiab.ttf", # Georgia Bold
        r"C:\Windows\Fonts\garabd.ttf"   # Garamond Bold
    ]
    for fp in fonts_to_try:
        if os.path.exists(fp):
            try:
                font_filosofo = ImageFont.truetype(fp, 52)
                font_sub = ImageFont.truetype(fp.replace("bd.ttf", ".ttf").replace("b.ttf", ".ttf"), 30)
                font_frase = ImageFont.truetype(fp, 44)
                break
            except Exception:
                pass

    # Dibujar textos centrados en la parte superior del arte central
    center_x = total_w // 2

    # Línea 1: Nombre del filósofo (MAYÚSCULAS BLANCO)
    bbox1 = draw.textbbox((0, 0), filosofo.upper(), font=font_filosofo)
    w1 = bbox1[2] - bbox1[0]
    draw.text((center_x - (w1 // 2), 120), filosofo.upper(), fill=(255, 255, 255), font=font_filosofo)

    # Línea 2: Subtítulo (blanco suave)
    bbox2 = draw.textbbox((0, 0), subtitulo, font=font_sub)
    w2 = bbox2[2] - bbox2[0]
    draw.text((center_x - (w2 // 2), 190), subtitulo, fill=(240, 240, 245), font=font_sub)

    # Línea 3: Frase entre comillas (DORADO CÁLIDO)
    frase_formateada = f'"{frase}"'
    bbox3 = draw.textbbox((0, 0), frase_formateada, font=font_frase)
    w3 = bbox3[2] - bbox3[0]
    
    # Si la frase es larga, dividirla en 2 líneas
    if w3 > (inner_w - 60):
        palabras = frase.split()
        mitad = len(palabras) // 2
        l1 = f'"{ " ".join(palabras[:mitad]) }'
        l2 = f'{ " ".join(palabras[mitad:]) }"'
        bb_a = draw.textbbox((0, 0), l1, font=font_frase)
        bb_b = draw.textbbox((0, 0), l2, font=font_frase)
        draw.text((center_x - ((bb_a[2] - bb_a[0]) // 2), 260), l1, fill=(245, 190, 60), font=font_frase)
        draw.text((center_x - ((bb_b[2] - bb_b[0]) // 2), 320), l2, fill=(245, 190, 60), font=font_frase)
    else:
        draw.text((center_x - (w3 // 2), 260), frase_formateada, fill=(245, 190, 60), font=font_frase)

    img.save(output_path, quality=95)
    print(f"✅ Imagen estilo Carlos Arias generada en: {output_path}")

def main():
    print("=" * 60)
    print("🧠 PRUEBA EN VIVO: CEREBRO IA (REDACCIÓN + DISEÑO GRÁFICO)")
    print("=" * 60)

    # 1. GENERAR TEXTO CON GEMINI
    print("\n⏳ 1. Consultando al Cerebro IA (Gemini Flash)...")
    prompt_sistema = """Eres un filósofo y escritor estoico al estilo de Carlos Arias para Facebook.
Escribe un post de alto impacto en español.
Estructura:
Párrafo 1: Contexto histórico y humano crudo del dolor de Marco Aurelio (la peste Antonina, guerras y traiciones).
Párrafo 2: La frase contundente ("Mientras respires, sigue luchando") y qué significaba para él.
Párrafo 3: Aplicación a la vida moderna: cómo superar la queja y el cansancio hoy.
Hashtags: #Estoicismo #MarcoAurelio #FilosofiaDeVida #MentalidadFuerte #CarlosArias"""

    texto_generado = llamar_gemini(prompt_sistema, "Escribe el post completo listo para Facebook.")

    print("\n📝 TEXTO GENERADO POR EL CEREBRO IA:\n")
    print("-" * 60)
    print(texto_generado)
    print("-" * 60)

    # 2. GENERAR IMAGEN ESTILO CARLOS ARIAS
    print("\n🎨 2. Diseñando la imagen con franjas laterales y tipografía clásica...")
    img_out = r"D:\github\publicador_facebook\prueba_estilo_carlos_arias.jpg"
    crear_imagen_estilo_carlos_arias(
        filosofo="Marco Aurelio",
        subtitulo="(Emperador romano y filósofo estoico)",
        frase="Mientras respires, sigue luchando",
        output_path=img_out
    )

    # Abrir la imagen en el visor de Windows para que Jorge la vea
    print(f"\n🖼️ Abriendo la imagen generada en tu pantalla...")
    os.system(f'start "" "{img_out}"')

if __name__ == "__main__":
    main()
