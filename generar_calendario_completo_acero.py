import os
import sys
import json
import time
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
        return f'"{frase1} {frase2}"\n\nEl éxito es para los que asumen el 100% de responsabilidad y no se rinden jamás.\n\n#MentalidadDeAcero #Disciplina'
    
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
    
    for intento in range(3):
        try:
            res = requests.post(url, json=payload, timeout=25).json()
            if 'candidates' in res and res['candidates']:
                return res['candidates'][0]['content']['parts'][0]['text']
        except Exception as e:
            time.sleep(2)
            
    return f'"{frase1} {frase2}"\n\nEl éxito es para los que asumen el 100% de responsabilidad y no se rinden jamás.\n\n#MentalidadDeAcero #Disciplina'

# Fondos rotativos locales
FONDOS = [
    "mentalidad_de_acero/assets/fondo_1.jpg",
    "mentalidad_de_acero/assets/fondo_2.jpg",
    "mentalidad_de_acero/assets/fondo_3.jpg"
]

NUEVAS_BATALLAS = [
    # Octubre 20 a 31
    {
        "id": 11, "fecha": "2026-10-20", "arquetipo": "EL BUSCADOR DE CULPABLES",
        "subtitulo": "EL BUSCADOR DE CULPABLES",
        "items_izq": ["SEÑALA A OTROS", "CULPA A LA SUERTE", "NUNCA SE EQUIVOCA", "ELUDE TODA CULPA", "ESPERA QUE OTROS ARREGLEN", "ETERNO INOCENTE"],
        "items_der": ["MIRA AL ESPEJO", "ASUME EL RESULTADO", "CORRIGE EN EL ACTO", "PROPIEDAD ABSOLUTA", "ARREGLA EL PROBLEMA", "LÍDER RESPONSABLE"],
        "frase1": "EL HOMBRE QUE SEÑALA CON EL DEDO A OTROS,",
        "frase2": "TIENE TRES DEDOS SEÑALÁNDOSE A SÍ MISMO."
    },
    {
        "id": 12, "fecha": "2026-10-21", "arquetipo": "EL DEPENDIENTE DEL ÁNIMO",
        "subtitulo": "EL DEPENDIENTE DEL ÁNIMO",
        "items_izq": ["SOLO ACTÚA CON GANAS", "ESCLAVO DEL CLIMA", "INCONSTANCIA PURA", "ABANDONA AL DESÁNIMO", "BUSCA MOTIVACIÓN FÁCIL", "FRÁGIL ANTE LA TRISTEZA"],
        "items_der": ["ACTÚA SIN IMPORTAR EL ÁNIMO", "DOMINA SU CLIMA INTERNO", "CONSTANCIA DE HIERRO", "EJECUTA EN EL DESÁNIMO", "DISCIPLINA INQUEBRANTABLE", "FUERTE EN LA TORMENTA"],
        "frase1": "SI SOLO ENTRENAS CUANDO TIENES GANAS,",
        "frase2": "TU VIDA SERÁ TAN INESTABLE COMO TUS EMOCIONES."
    },
    {
        "id": 13, "fecha": "2026-10-22", "arquetipo": "EL CAZADOR DE VALIDACIÓN",
        "subtitulo": "EL CAZADOR DE VALIDACIÓN",
        "items_izq": ["VIVE PARA LA FOTO", "MENDIGA UN LIKE", "CAMBIA PARA GUSTAR", "SE VENDE POR APLAUSOS", "TEME EL RECHAZO", "VACÍO EN PRIVADO"],
        "items_der": ["VIVE PARA SU PAZ", "CONSTRUYE EN SILENCIO", "FIEL A SUS PRINCIPIOS", "INDIFERENTE AL HALAGO", "CONFIADO EN SU VALOR", "LLENO EN LO PRIVADO"],
        "frase1": "NO CONSTRUYAS TU VIDA PARA LA FOTO,",
        "frase2": "CONSTRUYE TU VIDA PARA TU PAZ MENTAL."
    },
    {
        "id": 14, "fecha": "2026-10-23", "arquetipo": "EL PRISIONERO DE LA DUDA",
        "subtitulo": "EL PRISIONERO DE LA DUDA",
        "items_izq": ["SOBREPIENSA TODO", "TEME EQUIVOCARSE", "PARÁLISIS POR ANÁLISIS", "ESPERA CERTEZA TOTAL", "SE QUEDA EN TEORÍA", "DERROTADO POR EL MIEDO"],
        "items_der": ["TOMA DECISIONES YA", "APRENDE DEL ERROR", "ACCIÓN BRUTAL DIARIA", "AVANZA EN LA INCERTIDUMBRE", "EJECUTA EN EL CAMPO", "CONQUISTA EL TEMOR"],
        "frase1": "LA DUDA ASESINA MÁS SUEÑOS",
        "frase2": "QUE EL FRACASO MISMO JAMÁS LOGRARÍA."
    },
    {
        "id": 15, "fecha": "2026-10-24", "arquetipo": "EL NEGOCIADOR DE PEREZA",
        "subtitulo": "EL NEGOCIADOR DE PEREZA",
        "items_izq": ["PIDE CINCO MINUTOS MÁS", "SE CONVENCE DE PARAR", "JUSTIFICA EL DESCANSO", "SE PERDONA TODO", "AFRONTA A MEDIAS", "ESCLAVO DE LA CAMA"],
        "items_der": ["SALTA AL SONAR LA ALARMA", "APLASTA LA DUDA", "EL DESCANSO SE GANA", "ESTÁNDAR INNEGOCIABLE", "ENTREGA EL CIEN POR CIENTO", "DUEÑO DE SU DÍA"],
        "frase1": "CUANDO NEGOCIAS CON LA PEREZA,",
        "frase2": "SIEMPRE TERMINAS VENDIENDO TU PROPIO FUTURO."
    },
    {
        "id": 16, "fecha": "2026-10-25", "arquetipo": "EL DÉBIL ANTE LA CRÍTICA",
        "subtitulo": "EL DÉBIL ANTE LA CRÍTICA",
        "items_izq": ["SE DERRUMBA POR COMENTARIOS", "BUSCA AGRADAR A TODOS", "CAMBIA SU OPINIÓN", "GUARDA RESENTIMIENTO", "SE DETIENE POR BURLAS", "HERIDO POR EL QUÉ DIRÁN"],
        "items_der": ["IGNORA EL RUIDO MEDIOCRE", "SOLO IMPORTA SU MISIÓN", "CONVICCIÓN TOTAL", "FILTRA CON MADUREZ", "USA LA BURLA DE GASOLINA", "INTOCABLE POR OPINIONES"],
        "frase1": "NUNCA ACEPTES CRÍTICAS DE ALGUIEN",
        "frase2": "A QUIEN JAMÁS LE PEDIRÍAS UN CONSEJO."
    },
    {
        "id": 17, "fecha": "2026-10-26", "arquetipo": "EL REHÉN DEL TELÉFONO",
        "subtitulo": "EL REHÉN DEL TELÉFONO",
        "items_izq": ["HORAS EN EL SCROLL", "DOPAMINA BARATA", "ATENCIÓN FRAGMENTADA", "CONSUME VIDAS AJENAS", "POSTERGA POR LA PANTALLA", "MENTE ADORMECIDA"],
        "items_der": ["DOMINA LA TECNOLOGÍA", "ENFOQUE PROFUNDO", "CONCENTRACIÓN LÁSER", "CONSTRUYE SU VIDA", "PRIMERO EJECUTA", "MENTE DESPIERTA"],
        "frase1": "EL QUE CONSUME LA VIDA DE OTROS EN PANTALLA,",
        "frase2": "SE OLVIDA DE CONQUISTAR SU PROPIA REALIDAD."
    },
    {
        "id": 18, "fecha": "2026-10-27", "arquetipo": "EL ACUMULADOR DE TEORÍA",
        "subtitulo": "EL ACUMULADOR DE TEORÍA",
        "items_izq": ["LEE SIN APLICAR", "CURSOS SIN ACCIÓN", "SABE MUCHO, HACE NADA", "EXPERTO DE CAFÉ", "PLANIFICA ETERNAMENTE", "RESULTADOS CERO"],
        "items_der": ["APRENDE Y APLICA HOY", "EJECUTOR INCANSABLE", "SABE Y DEMUESTRA", "GUERRERO DE TRINCHERA", "PLANIFICA Y DISPARA", "RESULTADOS REALES"],
        "frase1": "UN GRAMO DE ACCIÓN BRUTAL",
        "frase2": "VALE MÁS QUE UNA TONELADA DE TEORÍA."
    },
    {
        "id": 19, "fecha": "2026-10-28", "arquetipo": "EL HUIDOR DEL DOLOR",
        "subtitulo": "EL HUIDOR DEL DOLOR",
        "items_izq": ["CORRE DE LA MOLESTIA", "BUSCA SALIDA SENCILLA", "SE ASUSTA AL QUEMAR", "ELUDE EL SACRIFICIO", "PREFIERE LA SEDA", "DÉBIL ANTE LA VIDA"],
        "items_der": ["ABRAZA LA FRICCIÓN", "PAGA EL PRECIO COMPLETO", "AMA EL RETO DURO", "EL SACRIFICIO LO FORJA", "PREFIERE EL HIERRO", "INDOMABLE ANTE EL DESTINO"],
        "frase1": "EL DOLOR QUE EVITAS HOY",
        "frase2": "ES LA DEBILIDAD QUE TE APLASTARÁ MAÑANA."
    },
    {
        "id": 20, "fecha": "2026-10-29", "arquetipo": "EL CONFORME TEMPRANO",
        "subtitulo": "EL CONFORME TEMPRANO",
        "items_izq": ["CELEBRA ANTES DE TIEMPO", "SE CONFORMA CON POCO", "PIERDE EL HAMBRE", "SE FRENA EN LA SUBIDA", "ACEPTA LO MEDIOCRE", "QUEDA A MEDIAS"],
        "items_der": ["HAMBRIENTO SIEMPRE", "SUBE SU PROPIA VARA", "ENFOQUE EN LA CIMA", "NO PARA TRAS GANAR", "BUSCA LA EXCELENCIA", "LLEGA HASTA EL FINAL"],
        "frase1": "EL PEOR ENEMIGO DE LA GRANDEZA",
        "frase2": "ES SENTIRSE CÓMODO CON LO ACEPTABLE."
    },
    {
        "id": 21, "fecha": "2026-10-30", "arquetipo": "EL HIPÓCRITA DE LA PALABRA",
        "subtitulo": "EL HIPÓCRITA DE LA PALABRA",
        "items_izq": ["DICE Y NO HACE", "CONSEJOS QUE NO SIGUE", "FACHADA SIN FONDO", "PROMESAS AL AIRE", "BUSCA ADMIRACIÓN", "DESENMASCARADO POR TIEMPO"],
        "items_der": ["HACE ANTES DE DECIR", "PREDICA CON HECHOS", "COHERENCIA BRUTAL", "PALABRA DE HIERRO", "INSPIRACIÓN CON CONDUCTA", "RESPETADO POR RESULTADOS"],
        "frase1": "TUS ACCIONES HABLAN TAN FUERTE",
        "frase2": "QUE NADIE PUEDE ESCUCHAR LO QUE DICES."
    },
    {
        "id": 22, "fecha": "2026-10-31", "arquetipo": "EL VENGATIVO RESENTIDO",
        "subtitulo": "EL VENGATIVO RESENTIDO",
        "items_izq": ["VIVE MASTICANDO ODIO", "PIERDE TIEMPO EN VENGANZA", "ENERGÍA EN EL ENEMIGO", "AMARGADO POR TRAICIONES", "DESEA MAL AJENO", "ENFERMO POR RENCOR"],
        "items_der": ["TRANSFORMA LA HERIDA", "INVIERTE EN SU PROGRESO", "ENERGÍA EN SU VISIÓN", "AGRADECIDO POR LA LECCIÓN", "CONQUISTA SU VICTORIA", "SANO POR DISCIPLINA"],
        "frase1": "LA MEJOR VENGANZA NO ES EL ODIO,",
        "frase2": "ES UN ÉXITO TAN MASIVO QUE RESUENE EN SILENCIO."
    },
    # Noviembre 01 a 30
    {
        "id": 23, "fecha": "2026-11-01", "arquetipo": "EL DÉBIL MATUTINO",
        "subtitulo": "EL DÉBIL MATUTINO",
        "items_izq": ["POSPONE TRES ALARMAS", "SE LEVANTA AL MEDIODÍA", "COMIENZA APURADO", "PIERDE LAS MAÑANAS", "CEREBRO ADORMILADO", "ESPECTADOR DEL DÍA"],
        "items_der": ["VENCE A LA ALMOHADA", "MADRUGA CON PROPÓSITO", "COMIENZA CON CONTROL", "DOMINA LA MAÑANA", "MENTE LÚCIDA Y FRÍA", "CONQUISTADOR DEL DÍA"],
        "frase1": "SI NO PUEDES VENCER A TU ALMOHADA,",
        "frase2": "¿CÓMO PIENSAS SALIR A CONQUISTAR EL MUNDO?"
    },
    {
        "id": 24, "fecha": "2026-11-02", "arquetipo": "EL ESPERADOR DE SUERTE",
        "subtitulo": "EL ESPERADOR DE SUERTE",
        "items_izq": ["JUEGA A LA LOTERÍA", "ESPERA OPORTUNIDAD MÁGICA", "SE QUEJA DE NO TENER 'CHANCE'", "ESPERA AL SALVADOR", "VIVE EN LA FANTASÍA", "PASIVO ANTE LA VIDA"],
        "items_der": ["CREA SU OPORTUNIDAD", "TRABAJA HASTA ATRAERLA", "AGRADECIDO POR LA PELEA", "SE RESCATA A SÍ MISMO", "VIVE EN LA REALIDAD", "ACTIVO EN LA BATALLA"],
        "frase1": "LA SUERTE ES EL PRETEXTO DEL MEDIOCRE;",
        "frase2": "EL ESFUERZO ES LA RELIGIÓN DEL GANADOR."
    },
    {
        "id": 25, "fecha": "2026-11-03", "arquetipo": "EL DISPERSO SIN ENFOQUE",
        "subtitulo": "EL DISPERSO SIN ENFOQUE",
        "items_izq": ["DIEZ METAS A LA VEZ", "NO TERMINA NADA", "CAMBIA POR MODA", "ENERGÍA DISPERSA", "CONFUSO EN SU RUMBO", "FRUSTRADO AL FINAL"],
        "items_der": ["UNA META OBSESIVA", "TERMINA LO QUE EMPIEZA", "PERSISTE POR AÑOS", "ENERGÍA CONCENTRADA", "CLARO EN SU CAMINO", "VICTORIOSO EN EL FIN"],
        "frase1": "EL HOMBRE QUE PERSIGUE DOS LIEBRES,",
        "frase2": "TERMINA QUEDÁNDOSE SIN NINGUNA."
    },
    {
        "id": 26, "fecha": "2026-11-04", "arquetipo": "EL TEMEROSO DEL JUICIO",
        "subtitulo": "EL TEMEROSO DEL JUICIO",
        "items_izq": ["ESCONDE SUS SUEÑOS", "VIVE CON VERGÜENZA", "BUSCA APROBACIÓN SOCIAL", "MODIFICA SU CONDUCTA", "TEME AL QUÉ DIRÁN", "SEPULTA SU TALENTO"],
        "items_der": ["EXPONE SU VISIÓN", "ORGULLOSO DEL TRABAJO", "SE MIDE CONSIGO MISMO", "CONDUCTA INTACTA", "LE DA IGUAL EL JUICIO", "EXPLOTA SU TALENTO"],
        "frase1": "EL MIEDO AL QUÉ DIRÁN ES LA TUMBA",
        "frase2": "DONDE MUEREN LOS HOMBRES SIN DESTINO."
    },
    {
        "id": 27, "fecha": "2026-11-05", "arquetipo": "EL IMPOSTOR MENTAL",
        "subtitulo": "EL IMPOSTOR MENTAL",
        "items_izq": ["SE CREE INCAPAZ", "SUBESTIMA SU VALOR", "COMPARA SU INICIO", "SE SIENTE FRAUDE", "PIENSA QUE NO MERECE", "AUTOBOICOT CONSTANTE"],
        "items_der": ["SABE QUE PUEDE APRENDER", "CONOCE SU POTENCIAL", "SOLO SE COMPARA AYER", "HONESTO CON SU SUDOR", "GANA SU LUGAR", "IMPULSO CONSTANTE"],
        "frase1": "NO TE CREAS MENOS QUE NADIE;",
        "frase2": "EL MUNDO ESTÁ LLENO DE VALIENTES QUE SE ATREVIERON."
    },
    {
        "id": 28, "fecha": "2026-11-06", "arquetipo": "EL REBELDE SIN CAUSA",
        "subtitulo": "EL REBELDE SIN CAUSA",
        "items_izq": ["QUEJA DEL SISTEMA", "PELEA BATALLAS INÚTILES", "RABIA SIN DIRECCIÓN", "RECHAZA TODA DISCIPLINA", "CONFUNDE REBELDÍA CON PEREZA", "DERROTADO EN LA ANARQUÍA"],
        "items_der": ["APRENDE LAS REGLAS", "GANA LAS BATALLAS CLAVE", "ENERGÍA EN SU IMPERIO", "DISCIPLINA RIGUROSA", "LIBERTAD MEDIANTE DOMINIO", "VICTORIOSO EN EL ORDEN"],
        "frase1": "QUEJARTE DE LAS REGLAS NO TE HACE FUERTE;",
        "frase2": "DOMINAR EL JUEGO Y GANARLO ES LO QUE IMPORTA."
    },
    {
        "id": 29, "fecha": "2026-11-07", "arquetipo": "EL DERROTADO POR LA PÉRDIDA",
        "subtitulo": "EL DERROTADO POR LA PÉRDIDA",
        "items_izq": ["LLORA LO QUE SE FUE", "ATASCADO EN EL LUTO", "SE RINDE TRAS CAER", "SE AMARGA LA VIDA", "CIERRA LAS PUERTAS", "VIVE EN EL DOLOR"],
        "items_der": ["HONRA Y CONTINÚA", "APRENDE DE LA CAÍDA", "SE LEVANTA CON FUEGO", "FORJA SU CARÁCTER", "ABRE NUEVAS PUERTAS", "VIVE CON PROPÓSITO"],
        "frase1": "A VECES SE GANA, A VECES SE APRENDE;",
        "frase2": "PERO UN HOMBRE DE ACERO NUNCA SE DECLARA DERROTADO."
    },
    {
        "id": 30, "fecha": "2026-11-08", "arquetipo": "EL ESCLAVO DEL PLACER BARATO",
        "subtitulo": "EL ESCLAVO DEL PLACER BARATO",
        "items_izq": ["COMIDA BASURA", "VICIO SIN CONTROL", "POSTERGA POR DIVERSIÓN", "NO TOLERA EL ABURRIMIENTO", "ESCLAVO DE IMPULSOS", "CUERPO Y MENTE ROTOS"],
        "items_der": ["NUTRICIÓN Y FUERZA", "TEMPLANZA ABSOLUTA", "TRABAJO ANTES DEL GOZO", "DOMINA EL SILENCIO", "SEÑOR DE SUS IMPULSOS", "CUERPO Y MENTE DE HIERRO"],
        "frase1": "EL PLACER INMEDIATO TE DESTRUYE;",
        "frase2": "LA RECOMPENSA TARDÍA TE TRANSFORMA."
    },
    {
        "id": 31, "fecha": "2026-11-09", "arquetipo": "EL FINGIDOR DE OCUPACIÓN",
        "subtitulo": "EL FINGIDOR DE OCUPACIÓN",
        "items_izq": ["MUCHAS TAREAS VACÍAS", "RESPONDE EMAILS SIN FIN", "CORRE SIN AVANZAR", "CANSA SIN LOGRAR", "CONFUNDE ACTIVIDAD CON IMPACTO", "AGOTADO Y MEDIOCRE"],
        "items_der": ["POCAS TAREAS CRUCIALES", "ATACA LO DIFÍCIL", "AVANZA CON PASO FIRME", "CONQUISTA Y CONSOLIDA", "ENFOCADO EN RESULTADOS", "FRESCO Y EFICAZ"],
        "frase1": "ESTAR OCUPADO NO ES ESTAR AVANZANDO;",
        "frase2": "EL MOVIMIENTO SIN IMPACTO ES SOLO ILUSIÓN."
    },
    {
        "id": 32, "fecha": "2026-11-10", "arquetipo": "EL TRAIDOR DE SUS PROMESAS",
        "subtitulo": "EL TRAIDOR DE SUS PROMESAS",
        "items_izq": ["DIJO QUE IBA A ENTRENAR", "SE EXCUSA A SÍ MISMO", "NEGOCIA EN PRIVADO", "PIERDE SU PALABRA", "AUTOESTIMA POR EL SUELO", "DESCONFIANZA PROPIA"],
        "items_der": ["CUMPLE LO QUE DIJO", "CERO EXCUSAS EN PRIVADO", "FIRME EN LA SOLEDAD", "PALABRA SAGRADA", "AUTOESTIMA BLINDADA", "CONFIANZA TOTAL"],
        "frase1": "SI TE ROMPES UNA PROMESA A TI MISMO,",
        "frase2": "YA PERDISTE EL RESPETO FRENTE AL ESPEJO."
    },
    {
        "id": 33, "fecha": "2026-11-11", "arquetipo": "EL AMANTE DE LA RUTINA CÓMODA",
        "subtitulo": "EL AMANTE DE LA RUTINA CÓMODA",
        "items_izq": ["HACE LO MISMO POR AÑOS", "TEME LO DESCONOCIDO", "SE ESTANCA SIN NOTARLO", "EVITA TODO DESAFÍO", "SE SIENTE SEGURO", "MUERE EN VIDA"],
        "items_der": ["INNOVA Y SE RETA", "ABRAZA EL RETO", "CRECE DÍA A DÍA", "BUSCA NUEVAS CUMBRES", "SABE QUE LA SEGURIDAD NO EXISTE", "VIVE AL MÁXIMO"],
        "frase1": "LA RUTINA SIN CRECIMIENTO",
        "frase2": "ES UNA PRISIÓN CON PUERTAS ABIERTAS."
    },
    {
        "id": 34, "fecha": "2026-11-12", "arquetipo": "EL RESENTIDO POR EL RECHAZO",
        "subtitulo": "EL RESENTIDO POR EL RECHAZO",
        "items_izq": ["SE OFENDE POR UN 'NO'", "TOMA TODO PERSONAL", "SE RETIRA HUMILLADO", "LLORA LA PUERTA CERRADA", "ABANDONA EL INTENTO", "DÉBIL ANTE EL RETO"],
        "items_der": ["USA EL 'NO' DE MOTOR", "ENTIENDE EL MERCADO", "VUELVE CON MÁS VALOR", "CONSTRUYE SU PROPIA PUERTA", "PERSISTE HASTA VENCER", "FUERTE EN LA BATALLA"],
        "frase1": "CADA PUERTA QUE TE CIERRAN EN LA CARA",
        "frase2": "ES UN MOTIVO MÁS PARA CONSTRUIR TU PROPIO CASTILLO."
    },
    {
        "id": 35, "fecha": "2026-11-13", "arquetipo": "EL REZAGADO POR INDECISIÓN",
        "subtitulo": "EL REZAGADO POR INDECISIÓN",
        "items_izq": ["MESES PARA ELEGIR", "PIERDE OPORTUNIDADES", "TEME AL CAMBIO", "DEJA QUE OTROS DECIDAN", "ESPECTADOR EN LA FILA", "LAMENTA EL TIEMPO"],
        "items_der": ["DECIDE CON RAPIDEZ", "CAPTURA LA OCASIÓN", "ENCABEZA EL CAMBIO", "DUEÑO DE SU TIMÓN", "LÍDER EN LA MARCHA", "DISFRUTA EL AVANCE"],
        "frase1": "LA INDECISIÓN ES EL LADRÓN SILENCIOSO",
        "frase2": "QUE TE ROBA LOS MEJORES AÑOS DE TU VIDA."
    },
    {
        "id": 36, "fecha": "2026-11-14", "arquetipo": "EL JUEZ DE LA VIDA AJENA",
        "subtitulo": "EL JUEZ DE LA VIDA AJENA",
        "items_izq": ["OPINA DE TODO EL MUNDO", "SE CREE SUPERIOR", "CRITICA AL QUE HACE", "CIEGO A SUS FALTAS", "DESPERDICIA SU MENTE", "MISERABLE EN SECRETO"],
        "items_der": ["ENFOCADO EN SU TRABAJO", "HUMILDE ANTE LA VIDA", "RESPETA AL QUE TRABAJA", "ANALIZA SUS FALLAS", "POTENCIA SU MENTE", "PLENO EN SU CONQUISTA"],
        "frase1": "CADA MINUTO QUE PASAS JUZGANDO A OTROS,",
        "frase2": "ES UN MINUTO MENOS EN TU PROPIO IMPERIO."
    },
    {
        "id": 37, "fecha": "2026-11-15", "arquetipo": "EL DEPENDIENTE DEL APLAUSO",
        "subtitulo": "EL DEPENDIENTE DEL APLAUSO",
        "items_izq": ["SI NO LE RECONOCEN, PARA", "SE DESINFLA EN EL SILENCIO", "TRABAJA POR LA MEDALLA", "FRÁGIL SIN PÚBLICO", "BUSCA PALMADAS", "INSEGURO EN SOLEDAD"],
        "items_der": ["TRABAJA EN EL ANONIMATO", "AMA EL SILENCIO DURO", "TRABAJA POR LA MISIÓN", "FUERTE EN LAS SOMBRAS", "LE BASTA SU CONCIENCIA", "SEGURO EN SOLEDAD"],
        "frase1": "SI DEPENDES DE QUE TE ALABEN PARA TRABAJAR,",
        "frase2": "TE MORIRÁS DE HAMBRE EN EL PRIMER SILENCIO."
    },
    {
        "id": 38, "fecha": "2026-11-16", "arquetipo": "EL TEMEROSO AL SACRIFICIO",
        "subtitulo": "EL TEMEROSO AL SACRIFICIO",
        "items_izq": ["QUIERE EL ÉXITO GRATIS", "NO QUIERE PERDER SUEÑO", "SE ASUSTA DE COBRAR EL PRECIO", "ESPERA DESCUENTOS", "NO ENTREGA NADA", "NO RECIBE NADA"],
        "items_der": ["PAGA TODO POR ADELANTADO", "DUERME LO JUSTO", "DISFRUTA EL SACRIFICIO", "CERO DESCUENTOS", "ENTREGA SU ALMA", "RECIBE LA CIMA"],
        "frase1": "TODO LO QUE QUIERES ESTÁ DEL OTRO LADO",
        "frase2": "DEL SACRIFICIO QUE HOY NO TE ATREVES A HACER."
    },
    {
        "id": 39, "fecha": "2026-11-17", "arquetipo": "EL MALDECIDOR DE SU DESTINO",
        "subtitulo": "EL MALDECIDOR DE SU DESTINO",
        "items_izq": ["MALDICE EL MAL TIEMPO", "SE QUEJA DEL PAÍS", "RENEGA DE SU SANGRE", "SE SIENTE MALDITO", "BAJA LOS BRAZOS", "VENCIDO POR LA SOMBRA"],
        "items_der": ["APRENDE A NAVEGAR LA TORMENTA", "CRECE DONDE LO PLANTAN", "HONRA SU LUCHA", "SE SABE FORJADO", "SUBE LA GUARDIA", "VENCEDOR EN LA SOMBRA"],
        "frase1": "NO MALDIGAS LA LLUVIA QUE TE MOJA;",
        "frase2": "APRENDE A PELEAR EN MEDIO DEL BARRO."
    },
    {
        "id": 40, "fecha": "2026-11-18", "arquetipo": "EL REHEN DIGITAL",
        "subtitulo": "EL REHÉN DIGITAL",
        "items_izq": ["SEIS HORAS DE PANTALLA", "NOTIFICACIÓN TRAS NOTIFICACIÓN", "CEREBRO QUEMADO", "ADICTO A ESTIMULACIÓN", "PIERDE EL CONTACTO", "DESCONECTADO DE SUS METAS"],
        "items_der": ["PANTALLAS EN SILENCIO", "TRABAJO PROFUNDO", "CEREBRO REGENERADO", "CONECTADO A SU VISIÓN", "CONTACTO CON LA REALIDAD", "DUEÑO DE SU TIEMPO"],
        "frase1": "EL SCROLL INFINITO TE ANESTESIA LA MENTE",
        "frase2": "MIENTRAS TU COMPETENCIA CONQUISTA EL TERRENO."
    },
    {
        "id": 41, "fecha": "2026-11-19", "arquetipo": "EL TRAIDOR DE SU CÍRCULO",
        "subtitulo": "EL TRAIDOR DE SU CÍRCULO",
        "items_izq": ["HABLA A ESPALDAS", "ENVÍDIA AL HERMANO", "SE SALVA SOLO", "ROMPEDOR DE PACTOS", "DESLEAL POR BENEFICIO", "MUERE EN SOLEDAD"],
        "items_der": ["DEFIENDE DE FRENTE", "CELEBRA AL HERMANO", "LLEVA A TODOS AL ÉXITO", "FIEL A SU PALABRA", "LEALTAD INNEGOCIABLE", "RODEADO DE LEONES"],
        "frase1": "EL HOMBRE QUE TRAICIONA A SU CÍRCULO,",
        "frase2": "TERMINA MURIENDO DE FRÍO EN LA SOLEDAD."
    },
    {
        "id": 42, "fecha": "2026-11-20", "arquetipo": "EL ARROGANTE PREMATURO",
        "subtitulo": "EL ARROGANTE PREMATURO",
        "items_izq": ["GANÓ UNA Y SE CREE DIOS", "MIRA CON DESPRECIO", "DEJA DE ENTRENAR", "SE DUERME EN SU GLORIA", "CELEBRA ANTES DEL FINAL", "DERRUMBADO POR SOBERBIA"],
        "items_der": ["GANA Y SE REINICIA", "TRATA CON RESPETO", "ENTRENA EL DOBLE", "TIENE HAMBRE DE MÁS", "CELEBRA AL CORONAR", "LEVANTADO POR HUMILDAD"],
        "frase1": "LA HUMILDAD EN LA CONQUISTA ES PODER;",
        "frase2": "LA ARROGANCIA TEMPRANA ES EL PRELUDIO DE LA CAÍDA."
    },
    {
        "id": 43, "fecha": "2026-11-21", "arquetipo": "EL APAGAFUEGOS REACTIVO",
        "subtitulo": "EL APAGAFUEGOS REACTIVO",
        "items_izq": ["VIVE AL DÍA", "RESUELVE EMERGENCIAS", "NUNCA PLANIFICA", "VICTIMA DE IMPREVISTOS", "ESTRESADO CONSTANTE", "SIN ESTRATEGIA"],
        "items_der": ["PREVÉ EL ESCENARIO", "ANTICIPA LA JUGADA", "ESTRATEGIA AÑOS ADELANTE", "DOMINA EL IMPREVISTO", "CALMO Y CALCULADOR", "ESTRATEGA MAESTRO"],
        "frase1": "NO VIVAS REACCIONANDO A LO QUE PASA;",
        "frase2": "SÉ EL HOMBRE QUE CAUSA LO QUE TIENE QUE PASAR."
    },
    {
        "id": 44, "fecha": "2026-11-22", "arquetipo": "EL PEREZOSO DE FIN DE SEMANA",
        "subtitulo": "EL PEREZOSO DE FIN DE SEMANA",
        "items_izq": ["VIVE PARA EL VIERNES", "DESTRUYE LO CONSTRUIDO", "LUNES EN RESACA", "CINCO DÍAS BIEN, DOS MAL", "ESCLAVO DEL CALENDARIO", "RETROCEDE SEMANALMENTE"],
        "items_der": ["VIVE PARA SU MISIÓN", "CUIDA SU TEMPLO SIEMPRE", "LUNES CON PODER", "SIETE DÍAS DE EXCELENCIA", "DUEÑO DE SU CALENDARIO", "AVANZA IMPARABLE"],
        "frase1": "TUS METAS NO SE TOMAN DÍAS LIBRES;",
        "frase2": "SI DESCANSAS DE MÁS, TU SUEÑO SE DESVANECE."
    },
    {
        "id": 45, "fecha": "2026-11-23", "arquetipo": "EL AVALADOR DE SUS MENTIRAS",
        "subtitulo": "EL AVALADOR DE SUS MENTIRAS",
        "items_izq": ["SE DICE 'ESTOY BIEN'", "DISFRAZA LA COBARDÍA", "JUSTIFICA SU BARRIGA", "MAQUILLA LA QUIEBRA", "VIVE EN LA MENTIRA", "DESPERTAR DESTROZADO"],
        "items_der": ["HONESTIDAD BRUTAL", "ADMITE LA DEBILIDAD", "ENTRENA HASTA CAMBIAR", "TRABAJA HASTA CRECER", "VIVE EN LA VERDAD", "DESPERTAR CONQUISTADOR"],
        "frase1": "PUEDES ENGAÑAR A TODO EL MUNDO,",
        "frase2": "PERO NO PUEDES ENGAÑAR A TUS PROPIOS RESULTADOS."
    },
    {
        "id": 46, "fecha": "2026-11-24", "arquetipo": "EL TIMORATO ANTE EL RIESGO",
        "subtitulo": "EL TIMORATO ANTE EL RIESGO",
        "items_izq": ["TODO LO QUIERE 'SEGURO'", "TEME PERDER LO POCO", "VIDA PEQUEÑA Y GRIS", "ESPECTADOR EN LA ORILLA", "NUNCA SE LANZA", "ARREPENTIMIENTO VIEJO"],
        "items_der": ["ARRIESGA CALCULADO", "APUESTA POR SÍ MISMO", "VIDA INTENSA Y GRANDE", "GLADIADOR EN LA ARENA", "SE LANZA Y CONQUISTA", "ORGULLO EN LA VEJEZ"],
        "frase1": "EL RIESGO MÁS GRANDE EN ESTA VIDA",
        "frase2": "ES PASARLA SIN HABER ARRIESGADO NADA."
    },
    {
        "id": 47, "fecha": "2026-11-25", "arquetipo": "EL QUEBRADO POR LA PRESIÓN",
        "subtitulo": "EL QUEBRADO POR LA PRESIÓN",
        "items_izq": ["EXPLOTA CON EL ESTRÉS", "LLORA ANTE LA CARGA", "SUELTA LA BARRA", "SE RINDE ANTE LA CRISIS", "PIDE MENOS PESO", "DESTRUIDO POR EL PESO"],
        "items_der": ["SE CALMA EN EL CAOS", "SONRÍE ANTE LA CARGA", "APRIETA LA BARRA", "CRECE EN LA CRISIS", "PIDE ESPALDAS MÁS ANCHAS", "TRANSFORMADO EN DIAMANTE"],
        "frase1": "LOS CARBONES SE DESINTEGRAN BAJO PRESIÓN;",
        "frase2": "LOS DIAMANTES SE FORJAN EN ELLA."
    },
    {
        "id": 48, "fecha": "2026-11-26", "arquetipo": "EL RECLAMADOR DE DERECHOS",
        "subtitulo": "EL RECLAMADOR DE DERECHOS",
        "items_izq": ["EXIGE RESPETO SIN GANARLO", "PIDE PRIVILEGIOS", "LLORA 'INJUSTICIA'", "ESPERA TRATO ESPECIAL", "MENDIGA HONORES", "DESPRECIADO POR VACÍO"],
        "items_der": ["GANA RESPETO CON ACTOS", "FORJA SUS PRIVILEGIOS", "CREA SU PROPIA JUSTICIA", "NO PIDE NADA A NADIE", "CONQUISTA SUS HONORES", "RESPETADO POR PODER"],
        "frase1": "NO PIDAS RESPETO POR HABER NACIDO;",
        "frase2": "GÁNATE EL RESPETO CON TU CONDUCTA Y TU SUDOR."
    },
    {
        "id": 49, "fecha": "2026-11-27", "arquetipo": "EL DORMIDO EN SUS LAURELES",
        "subtitulo": "EL DORMIDO EN SUS LAURELES",
        "items_izq": ["HABLA DE SU PASADO", "VIVE DEL TROFEO VIEJO", "CREE QUE YA LLEGÓ", "PIERDE LA VELOCIDAD", "REBASADO POR NUEVOS", "OLVIDADO EN EL TIEMPO"],
        "items_der": ["EL PASADO NO IMPORTA", "BUSCA EL TROFEO NUEVO", "SABE QUE NUNCA TERMINA", "AUMENTA LA VELOCIDAD", "LIDERA LA MANADA", "RECORDADO POR INDOMABLE"],
        "frase1": "EL ÉXITO DE AYER NO TE DA DE COMER HOY;",
        "frase2": "CADA AMANECER COMIENZAS DESDE CERO."
    },
    {
        "id": 50, "fecha": "2026-11-28", "arquetipo": "EL PESIMISTA PROFESIONAL",
        "subtitulo": "EL PESIMISTA PROFESIONAL",
        "items_izq": ["VE EL PROBLEMA EN TODO", "INFECTA DE DESÁNIMO", "PARALIZA AL EQUIPO", "ENCUENTRA LA FALLA", "SE REGOCIJA EN LA DERROTA", "VIVE EN LA OSCURIDAD"],
        "items_der": ["VE LA SOLUCIÓN EN TODO", "INSPIRA CON ACCIÓN", "LEVANTA AL EQUIPO", "CREA LA SALIDA", "CONVIERTE DERROTA EN GLORIA", "ES LA LUZ EN LA SOMBRA"],
        "frase1": "EL PESIMISTA VE EL PROBLEMA EN CADA OPORTUNIDAD;",
        "frase2": "EL HOMBRE DE ACERO VE LA VICTORIA EN EL CAOS."
    },
    {
        "id": 51, "fecha": "2026-11-29", "arquetipo": "EL RENUNCIANTE A MEDIO CAMINO",
        "subtitulo": "EL RENUNCIANTE A MEDIO CAMINO",
        "items_izq": ["SE RINDE AL CANSANCIO", "SUELTA A UN PASO", "NO AGUANTA EL TRAMO FINAL", "LAMENTA EL DOLOR", "VUELVE A LA COMODIDAD", "ARREPENTIMIENTO ETERNO"],
        "items_der": ["APRIETA AL CANSARSE", "AGUANTA EL TRAMO FINAL", "CRUZA LA META DESTROZADO", "AGRADECE EL DOLOR", "CONQUISTA LA CIMA", "ORGULLO ETERNO"],
        "frase1": "LO MÁS TRISTE NO ES NO LLEGAR;",
        "frase2": "ES RENUNCIAR CUANDO FALTABAN DIEZ METROS PARA LA CIMA."
    },
    {
        "id": 52, "fecha": "2026-11-30", "arquetipo": "EL HOMBRE SIN PROPÓSITO",
        "subtitulo": "EL HOMBRE SIN PROPÓSITO",
        "items_izq": ["VIVE SIN NORTE", "ARRASADO POR LAS OLAS", "CUALQUIER DESTINO DA IGUAL", "CAMINA CIEGO", "VACÍO EN EL PECHO", "HISTORIA OLVIDADA"],
        "items_der": ["MISIÓN DE VIDA CLARA", "PARTE LAS OLAS", "CONSTRUYE SU PROPIO PUERTO", "OJOS EN LA ESTRELLA", "FUEGO EN EL PECHO", "LEYENDA GRABADA EN ROCA"],
        "frase1": "UN HOMBRE SIN MISIÓN ES UNA HOJA AL VIENTO;",
        "frase2": "UN HOMBRE DE ACERO ES LA ROCA QUE PARTE LA OLA."
    }
]

def main():
    img_dir = os.path.join("mentalidad_de_acero", "imagenes")
    os.makedirs(img_dir, exist_ok=True)

    json_path = os.path.join("mentalidad_de_acero", "publicaciones.json")
    posts = []
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            posts = json.load(f)

    # Identificar IDs ya existentes
    ids_existentes = {p["id"] for p in posts}

    print(f"📊 Posts actuales en JSON: {len(posts)}")
    print(f"⚡ Generando {len(NUEVAS_BATALLAS)} nuevas publicaciones (Posts 11 al 52)...")

    for i, b in enumerate(NUEVAS_BATALLAS):
        b_id = b["id"]
        if b_id in ids_existentes:
            print(f"⏩ Post #{b_id} ya existe. Omitiendo.")
            continue

        slug = b['arquetipo'].lower().replace(' ', '_').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
        img_filename = f"post_{b_id}_{slug}.jpg"
        img_out_path = os.path.join(img_dir, img_filename)

        fondo_idx = i % len(FONDOS)
        fondo_path = FONDOS[fondo_idx]

        print(f"\n[{i+1}/{len(NUEVAS_BATALLAS)}] 🎨 Componiendo #{b_id} ({b['fecha']}): {b['arquetipo']}...")
        if not os.path.exists(img_out_path):
            componer_infografia_mentalidad(
                imagen_base_path=fondo_path,
                titulo_superior="MENTALIDAD ERRÓNEA",
                subtitulo_superior=b["subtitulo"],
                items_izquierda=b["items_izq"],
                items_derecha=b["items_der"],
                frase_linea1=b["frase1"],
                frase_linea2=b["frase2"],
                output_path=img_out_path
            )

        print(f"  ✍️ Redactando copy con Gemini...")
        copy_text = redactar_copy_con_gemini(b["arquetipo"], b["frase1"], b["frase2"])

        post_obj = {
            "id": b_id,
            "fecha": b["fecha"],
            "hora": "19:00",
            "arquetipo": b["arquetipo"],
            "titulo": f"Mentalidad Errónea: {b['arquetipo']} vs Mentalidad de Acero",
            "texto": copy_text,
            "imagen": f"mentalidad_de_acero/imagenes/{img_filename}",
            "estado": "pendiente"
        }

        posts.append(post_obj)

        # Guardar progreso tras cada post
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(posts, f, ensure_ascii=False, indent=2)

        time.sleep(1.2) # Pausa amigable para respetar cuota de Gemini

    print("\n" + "="*70)
    print(f"🎉 ¡BATERÍA COMPLETA GENERADA! Total posts en Metalidad de Acero: {len(posts)}")
    print("="*70)

if __name__ == "__main__":
    main()
