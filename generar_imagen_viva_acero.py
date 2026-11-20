import os
import sys
import json
import random

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from disenador_acero_v2 import (
    generar_imagen_despertador,
    generar_imagen_contraste,
    generar_imagen_estrategia,
    generar_imagen_auditoria,
)

BG_DIR = os.path.join(BASE_DIR, "mentalidad_de_acero", "assets_diciembre")

BG_GROUPS = {
    "despertador": ["bg_statue_1.jpg", "bg_statue_2.jpg", "bg_roman_1.jpg", "bg_roman_2.jpg"],
    "contraste": ["bg_warrior_1.jpg", "bg_warrior_2.jpg", "bg_boxing_1.jpg", "bg_boxing_2.jpg"],
    "estrategia": ["bg_mountain_1.jpg", "bg_mountain_2.jpg", "bg_stormy_1.jpg", "bg_stormy_2.jpg"],
    "auditoria": ["bg_lion_1.jpg", "bg_lion_2.jpg", "bg_wolf_1.jpg", "bg_wolf_2.jpg"],
}

def elegir_fondo(estilo):
    candidatos = [os.path.join(BG_DIR, f) for f in BG_GROUPS.get(estilo, BG_GROUPS["despertador"])]
    existentes = [p for p in candidatos if os.path.exists(p)]
    if existentes:
        return random.choice(existentes)
    # Fallback a cualquier fondo disponible
    if os.path.exists(BG_DIR):
        todos = [os.path.join(BG_DIR, f) for f in os.listdir(BG_DIR) if f.lower().endswith(".jpg")]
        if todos:
            return random.choice(todos)
    return ""

def main():
    if len(sys.argv) < 3:
        print("Uso: python generar_imagen_viva_acero.py <datos.json> <salida.jpg>")
        sys.exit(1)

    json_input = sys.argv[1]
    output_path = sys.argv[2]

    with open(json_input, "r", encoding="utf-8") as f:
        data = json.load(f)

    estilo = data.get("estilo", "despertador")
    bg_path = elegir_fondo(estilo)
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    if estilo == "despertador":
        generar_imagen_despertador(
            bg_path=bg_path,
            numero_ley=int(data.get("numero", 1)),
            frase_principal=data.get("frase_principal", "LA DISCIPLINA TE HACE LIBRE"),
            frase_secundaria=data.get("frase_secundaria", "Actúa hoy sin negociar con tus excusas."),
            output_path=output_path,
        )
    elif estilo == "contraste":
        generar_imagen_contraste(
            bg_path=bg_path,
            arquetipo=data.get("arquetipo", "EL CONFORMISTA"),
            rasgos_debil=data.get("rasgos_debil", ["Busca excusas", "Se queja", "Huye del dolor", "Posterga", "Duda", "Se rinde"]),
            rasgos_acero=data.get("rasgos_acero", ["Asume el mando", "Resuelve", "Abraza el esfuerzo", "Actúa ya", "Decide firme", "Vence"]),
            sentencia=data.get("sentencia", "Tu carácter se demuestra cuando nadie te está mirando."),
            output_path=output_path,
        )
    elif estilo == "estrategia":
        principios_raw = data.get("principios", [])
        principios = []
        for item in principios_raw[:3]:
            if isinstance(item, dict):
                principios.append((item.get("titulo", "PRINCIPIO"), item.get("detalle", "Ejecuta con precisión.")))
            elif isinstance(item, (list, tuple)) and len(item) >= 2:
                principios.append((str(item[0]), str(item[1])))
        while len(principios) < 3:
            principios.append(("DISCIPLINA", "Mantén el enfoque incluso en la tormenta."))
        generar_imagen_estrategia(
            bg_path=bg_path,
            titulo_ley=data.get("titulo_ley", "LEY DE PODER"),
            regla_principal=data.get("regla_principal", "CONSTRUYE EN SILENCIO Y DEJA QUE EL ÉXITO HABLE"),
            tres_principios=principios,
            output_path=output_path,
        )
    else:
        generar_imagen_auditoria(
            bg_path=bg_path,
            pregunta_central=data.get("pregunta", "¿HOY CONQUISTASTE TU DÍA O VOLVISTE A PONER EXCUSAS?"),
            desafio=data.get("desafio", "Sé brutalmente honesto frente al espejo."),
            output_path=output_path,
        )

    print(f"✅ Imagen V2 generada ({estilo}): {output_path}")

if __name__ == "__main__":
    main()
