import os
import sys
import json
import requests
from componer_mentalidad_acero import componer_infografia_mentalidad

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Cargar API Key
API_KEY = ""
if os.path.exists("config.json"):
    with open("config.json", "r", encoding="utf-8") as f:
        cfg = json.load(f)
        API_KEY = cfg.get("GEMINI_API_KEY", "")

def redactar_copy_con_gemini(arquetipo, frase1, frase2):
    if not API_KEY:
        return "Texto motivacional para " + arquetipo
    
    sistema = """Eres el redactor jefe de la página de Facebook 'Metalidad de Acero'.
Tu estilo es implacable, inspirador, contundente y directo a la yugular (estilo David Goggins y Jocko Willink).
No toleras el victimismo ni la pereza. Tu objetivo es obligar al lector a tomar el control absoluto de su destino.

Estructura obligatoria:
1. Gancho inicial potente entre comillas con la frase central.
2. Un llamado de alerta sin anestesia ("¡DESPIERTA!").
3. El peligro del arquetipo débil y por qué arruina tu vida.
4. El despertar del Hombre de Acero (nadie te debe nada, la disciplina te hace libre).
5. 4 Reglas de Acero numeradas con emojis ⚔️ o 🔥.
6. Cierre motivacional agresivo.
7. Llamado a la acción: guardar el post, compartirlo y comentar un ⚔️.
8. Hashtags: #MentalidadDeAcero #Disciplina #CrecimientoPersonal #SinExcusas #Enfoque #HombresDeAcero #Superacion"""

    usuario = f"""Tema del post: Contraste entre la MENTALIDAD ERRÓNEA: {arquetipo} vs MENTALIDAD DE ACERO.
Frase clave: "{frase1} {frase2}"

Escribe el texto completo, con párrafos cortos y máxima contundencia:"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={API_KEY}"
    payload = {
        "contents": [{"role": "user", "parts": [{"text": sistema + "\n\n" + usuario}]}],
        "generationConfig": {"temperature": 0.85, "maxOutputTokens": 2048}
    }
    try:
        res = requests.post(url, json=payload).json()
        return res['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        print("Error en Gemini:", e)
        return f'"{frase1} {frase2}"\n\nEl éxito es para los que no se rinden jamás.\n\n#MentalidadDeAcero #Disciplina'

# Las 10 Batallas Mentales
BATALLAS = [
    {
        "id": 1,
        "arquetipo": "EL POBRECITO",
        "subtitulo": "EL POBRECITO",
        "base_img": "C:\\Users\\JMSOLUTIONS8825\\.gemini\\antigravity\\brain\\89115b35-5a7e-4589-b341-10e2a7da7397\\mentalidad_de_acero_1791642856974.jpg",
        "items_izq": ["ES CULPA DE OTROS", "SIEMPRE SE QUEJA", "TODO LE SALE MAL", "VIVE EN EXCUSAS", "BUSCA LÁSTIMA", "SE SIENTE VÍCTIMA"],
        "items_der": ["ASUME RESPONSABILIDAD", "BUSCA SOLUCIONES", "APRENDE DE DIFICULTADES", "TRABAJA DURO", "NO BUSCA LÁSTIMA", "SE LEVANTA Y SIGUE"],
        "frase1": "LA POBREZA PUEDE SER UNA CIRCUNSTANCIA,",
        "frase2": "PERO LA MENTALIDAD DE VÍCTIMA PUEDE SER UNA PRISIÓN.",
        "ya_publicado": True
    },
    {
        "id": 2,
        "arquetipo": "EL PROCRASTINADOR",
        "subtitulo": "EL PROCRASTINADOR",
        "base_img": "C:\\Users\\JMSOLUTIONS8825\\.gemini\\antigravity\\brain\\89115b35-5a7e-4589-b341-10e2a7da7397\\contraste_disciplina_entrenamiento_1791643213855.jpg",
        "items_izq": ["LO DEJA PARA MAÑANA", "ESPERA ESTAR INSPIRADO", "ADEPTO A LAS REDES", "VIVE EN INTENCIONES", "PLANEA SIN EJECUTAR", "LLENO DE PROMESAS"],
        "items_der": ["EMPIEZA AHORA MISMO", "NO ESPERA MOTIVACIÓN", "CERO DISTRACCIONES", "VIVE EN ACCIONES", "EJECUTA EN SILENCIO", "LLENO DE RESULTADOS"],
        "frase1": "MAÑANA ES EL DÍA FAVORITO DEL QUE NUNCA LOGRA NADA.",
        "frase2": "EL ÉXITO SE CONSTRUYE HOY O NO SE CONSTRUYE NUNCA.",
        "ya_publicado": False
    },
    {
        "id": 3,
        "arquetipo": "EL FRÁGIL EMOCIONAL",
        "subtitulo": "EL FRÁGIL EMOCIONAL",
        "base_img": "C:\\Users\\JMSOLUTIONS8825\\.gemini\\antigravity\\brain\\89115b35-5a7e-4589-b341-10e2a7da7397\\mentalidad_de_acero_1791642856974.jpg",
        "items_izq": ["EXPLOTA POR TODO", "OFENDIDO CONSTANTE", "ESCLAVO DEL ÁNIMO", "DEPENDE DE OPINIONES", "REACCIONA AL INSTANTE", "MENTALIDAD DE CRISTAL"],
        "items_der": ["DOMINA SUS IMPULSOS", "INMUTABLE ANTE CRÍTICAS", "DISCIPLINA SOBRE ÁNIMO", "SEGURO DE SU MISIÓN", "RESPONDE CON CALMA", "MENTALIDAD BLINDADA"],
        "frase1": "QUIEN NO CONTROLA SUS PROPIAS EMOCIONES,",
        "frase2": "SERÁ SIEMPRE EL ESCLAVO DE QUIEN SEPA PROVOCARLO.",
        "ya_publicado": False
    },
    {
        "id": 4,
        "arquetipo": "EL BUSCADOR DE ATAJOS",
        "subtitulo": "EL BUSCADOR DE ATAJOS",
        "base_img": "C:\\Users\\JMSOLUTIONS8825\\.gemini\\antigravity\\brain\\89115b35-5a7e-4589-b341-10e2a7da7397\\contraste_cima_montana_fog_1791643241851.jpg",
        "items_izq": ["BUSCA DINERO FÁCIL", "HUYE DE LA DISCIPLINA", "CAMBIA CADA SEMANA", "QUIERE RESULTADOS YA", "NO PAGA EL PRECIO", "ESPERA UN MILAGRO"],
        "items_der": ["CONSTRUYE PASO A PASO", "ABRAZA EL PROCESO", "CONSTANTE POR AÑOS", "VALORA EL ESFUERZO", "PAGA EL PRECIO DIARIO", "ES SU PROPIO MILAGRO"],
        "frase1": "LOS ATAJOS EN LA VIDA CASI SIEMPRE CONDUCEN",
        "frase2": "A LOS CALLEJONES SIN SALIDA DE LA MEDIOCRIDAD.",
        "ya_publicado": False
    },
    {
        "id": 5,
        "arquetipo": "EL ADICTO A VALIDACIÓN",
        "subtitulo": "EL ADICTO A VALIDACIÓN",
        "base_img": "C:\\Users\\JMSOLUTIONS8825\\.gemini\\antigravity\\brain\\89115b35-5a7e-4589-b341-10e2a7da7397\\mentalidad_de_acero_1791642856974.jpg",
        "items_izq": ["VIVE PARA APARENTAR", "BUSCA EL APLAUSO", "TEME NO ENCAJAR", "COMPRA LO QUE NO PUEDE", "PIDE PERMISO AL MUNDO", "VACÍO POR DENTRO"],
        "items_der": ["VIVE PARA TRASCENDER", "BUSCA SU RESPETO", "NO TEME ESTAR SOLO", "INVIERTE EN SU MENTE", "AVANZA SIN MIRAR ATRÁS", "FORJADO POR DENTRO"],
        "frase1": "EL QUE EDIFICA SU VALOR SOBRE EL APLAUSO AJENO,",
        "frase2": "SE DERRUMBA EN EL MOMENTO EN QUE LLEGA EL SILENCIO.",
        "ya_publicado": False
    },
    {
        "id": 6,
        "arquetipo": "EL ENEMIGO DEL FRACASO",
        "subtitulo": "EL ENEMIGO DEL FRACASO",
        "base_img": "C:\\Users\\JMSOLUTIONS8825\\.gemini\\antigravity\\brain\\89115b35-5a7e-4589-b341-10e2a7da7397\\contraste_disciplina_entrenamiento_1791643213855.jpg",
        "items_izq": ["SE RINDE AL PRIMER GOLPE", "VE EL ERROR COMO FIN", "OCULTA SUS CAÍDAS", "TEME VOLVER A INTENTAR", "SE CREE DERROTADO", "QUEDA PARALIZADO"],
        "items_der": ["SE LEVANTA MÁS FUERTE", "VE EL ERROR COMO GUÍA", "APRENDE DE LA CAÍDA", "INTENTA CON MÁS FURIA", "SABE QUE EL FALLO EDUCA", "AVANZA SIN FRENO"],
        "frase1": "EL FRACASO NO ES LO CONTRARIO AL ÉXITO,",
        "frase2": "EL FRACASO ES LA MATERIA PRIMA CON LA QUE SE FORJA.",
        "ya_publicado": False
    },
    {
        "id": 7,
        "arquetipo": "EL ENVIDIOSO PASIVO",
        "subtitulo": "EL ENVIDIOSO PASIVO",
        "base_img": "C:\\Users\\JMSOLUTIONS8825\\.gemini\\antigravity\\brain\\89115b35-5a7e-4589-b341-10e2a7da7397\\mentalidad_de_acero_1791642856974.jpg",
        "items_izq": ["CRITICA EL ÉXITO AJENO", "HABLA DE OTRAS VIDAS", "COMPITE CON EL VECINO", "LLENO DE AMARGURA", "JUSTIFICA SU PEREZA", "DESEA QUE OTROS CAIGAN"],
        "items_der": ["APLAUDE AL QUE TRABAJA", "SOLO HABLA DE SU META", "COMPITE CONSIGO MISMO", "LLENO DE PROPÓSITO", "ELIMINA TODA EXCUSA", "CONCENTRADO EN CRECER"],
        "frase1": "LA ENVIDIA ES EL TRIBUTO INVOLUNTARIO",
        "frase2": "QUE LA MEDIOCRIDAD LE PAGA AL TALENTO Y AL TRABAJO.",
        "ya_publicado": False
    },
    {
        "id": 8,
        "arquetipo": "EL AMANTE DEL CONFORT",
        "subtitulo": "EL AMANTE DEL CONFORT",
        "base_img": "C:\\Users\\JMSOLUTIONS8825\\.gemini\\antigravity\\brain\\89115b35-5a7e-4589-b341-10e2a7da7397\\contraste_cima_montana_fog_1791643241851.jpg",
        "items_izq": ["HUYE DEL ESFUERZO", "PREFIERE LA CAMA", "CONFORME CON LO POCO", "TEME A LA PRESIÓN", "SE QUEJA DEL SUDOR", "SE OXIDA EN REPOSO"],
        "items_der": ["BUSCA LA DIFICULTAD", "DISCIPLINA TEMPRANA", "HAMBRIENTO DE CRECER", "CRECE BAJO PRESIÓN", "AMA EL SUDOR DIARIO", "SE FORJA EN EL FUEGO"],
        "frase1": "EL CONFORT ES UNA PRISIÓN SILENCIOSA",
        "frase2": "QUE ASESINA MÁS SUEÑOS QUE CUALQUIER FRACASO.",
        "ya_publicado": False
    },
    {
        "id": 9,
        "arquetipo": "EL HABLADOR DE PLANES",
        "subtitulo": "EL HABLADOR DE PLANES",
        "base_img": "C:\\Users\\JMSOLUTIONS8825\\.gemini\\antigravity\\brain\\89115b35-5a7e-4589-b341-10e2a7da7397\\contraste_disciplina_entrenamiento_1791643213855.jpg",
        "items_izq": ["MUCHO RUIDO Y NADA", "CUENTA TODO ANTES", "VIVE EN LA ILUSIÓN", "PROMETE Y NO CUMPLE", "BUSCA FELICITACIÓN", "CERO RESULTADOS"],
        "items_der": ["SILENCIO Y ACCIÓN", "MUESTRA RESULTADOS", "VIVE EN LA REALIDAD", "HACE MÁS DE LO QUE DICE", "CUMPLE SU PALABRA", "RESULTADOS REALES"],
        "frase1": "NO LE CUENTES A NADIE LO QUE VAS A HACER,",
        "frase2": "DEJA QUE EL RUIDO DE TUS RESULTADOS HABLE POR TI.",
        "ya_publicado": False
    },
    {
        "id": 10,
        "arquetipo": "EL ESCLAVO DEL PASADO",
        "subtitulo": "EL ESCLAVO DEL PASADO",
        "base_img": "C:\\Users\\JMSOLUTIONS8825\\.gemini\\antigravity\\brain\\89115b35-5a7e-4589-b341-10e2a7da7397\\mentalidad_de_acero_1791642856974.jpg",
        "items_izq": ["CULPA A SU INFANCIA", "USA EL DOLOR DE EXCUSA", "VIVE RESENTIDO", "NO SUPERA LA HERIDA", "SE CREE VÍCTIMA", "ATADO AL AYER"],
        "items_der": ["FORJA SU PRESENTE", "USA EL DOLOR DE ESCUDO", "TRANSFORMA EL RENCOR", "CICATRIZA Y GUERREA", "SE VE COMO GUERRERO", "DUEÑO DE SU MAÑANA"],
        "frase1": "TU PASADO FUE TU CAMPO DE ENTRENAMIENTO,",
        "frase2": "NO LA CONDENA PERPETUA DE TU DESTINO.",
        "ya_publicado": False
    }
]

def generar_todo():
    img_dir = os.path.join("mentalidad_de_acero", "imagenes")
    os.makedirs(img_dir, exist_ok=True)

    json_path = os.path.join("mentalidad_de_acero", "publicaciones.json")
    posts_existentes = []
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            posts_existentes = json.load(f)

    posts_finales = []

    for b in BATALLAS:
        b_id = b["id"]
        img_filename = f"post_{b_id}_{b['arquetipo'].lower().replace(' ', '_')}.jpg"
        img_out_path = os.path.join(img_dir, img_filename)

        print(f"\n⚡ Procesando Batalla #{b_id}: {b['arquetipo']}...")

        # 1. Componer Infografía si no existe
        if not os.path.exists(img_out_path):
            print(f"  🎨 Componiendo imagen vertical: {img_filename}...")
            componer_infografia_mentalidad(
                imagen_base_path=b["base_img"],
                titulo_superior="MENTALIDAD ERRÓNEA",
                subtitulo_superior=b["subtitulo"],
                items_izquierda=b["items_izq"],
                items_derecha=b["items_der"],
                frase_linea1=b["frase1"],
                frase_linea2=b["frase2"],
                output_path=img_out_path
            )
        else:
            print(f"  ✅ Imagen ya existe: {img_filename}")

        # 2. Generar Copy si no existe en posts previos
        existente = next((p for p in posts_existentes if p.get("id") == b_id), None)
        if existente and existente.get("texto"):
            print(f"  ✅ Copy ya existente para #{b_id}")
            post_obj = existente
        else:
            print(f"  ✍️ Redactando copy con Gemini para #{b_id}...")
            texto_copy = redactar_copy_con_gemini(b["arquetipo"], b["frase1"], b["frase2"])
            # Fecha programada: 1 post cada día (a partir de hoy + id)
            dia = 10 + b_id - 1
            fecha_str = f"2026-10-{dia:02d}"
            post_obj = {
                "id": b_id,
                "fecha": fecha_str,
                "hora": "19:00",
                "arquetipo": b["arquetipo"],
                "titulo": f"Mentalidad Errónea: {b['arquetipo']} vs Mentalidad de Acero",
                "texto": texto_copy,
                "imagen": f"mentalidad_de_acero/imagenes/{img_filename}",
                "estado": "publicado" if b["ya_publicado"] else "pendiente"
            }

        posts_finales.append(post_obj)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(posts_finales, f, ensure_ascii=False, indent=2)

    print(f"\n🎉 ¡Batería completa de 10 publicaciones generada con éxito en {json_path}!")

if __name__ == "__main__":
    generar_todo()
