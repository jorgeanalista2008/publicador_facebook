/**
 * CEREBRO IA CON GOOGLE GEMINI PARA PUBLICACIONES VIRALES
 * --------------------------------------------------------
 * Genera contenido profesional autónomo:
 * 1. Crónicas comunitarias de perritos de barrio (patrón exacto viral).
 * 2. Storytelling biográfico de filosofía estoica (estilo Carlos Arias).
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const CONFIG_PATH = path.join(__dirname, 'config.json');

function obtenerApiKey() {
  if (process.env.GEMINI_API_KEY) {
    return process.env.GEMINI_API_KEY;
  }
  if (fs.existsSync(CONFIG_PATH)) {
    const cfg = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf-8'));
    return cfg.GEMINI_API_KEY;
  }
  return null;
}

async function llamarGemini(promptSistema, promptUsuario) {
  const apiKey = obtenerApiKey();
  if (!apiKey) {
    throw new Error('Falta GEMINI_API_KEY en variables de entorno o config.json');
  }

  // Modelos compatibles activos
  const modelos = ['gemini-3.5-flash', 'gemini-3.7-flash', 'gemini-3.8-flash', 'gemini-flash-latest'];

  for (const modelo of modelos) {
    const url = `https://generativelanguage.googleapis.com/v1beta/models/${modelo}:generateContent?key=${apiKey}`;
    const payload = {
      contents: [
        {
          role: 'user',
          parts: [{ text: `${promptSistema}\n\n${promptUsuario}` }]
        }
      ],
      generationConfig: {
        temperature: 0.8,
        topP: 0.95,
        maxOutputTokens: 4096
      }
    };

    try {
      const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const data = await res.json();
      if (res.ok && data.candidates && data.candidates[0]?.content?.parts[0]?.text) {
        return data.candidates[0].content.parts[0].text;
      }
    } catch (e) {
      // Intentar con siguiente modelo
    }
  }

  throw new Error('No se pudo generar contenido con ningún modelo de Gemini');
}

/**
 * Genera una crónica comunitaria de perrito siguiendo el patrón exacto.
 */
export async function generarHistoriaPerritoIA(situacionSugerida = "") {
  const sistema = `Eres un redactor experto en crónicas comunitarias virales para Facebook sobre rescate animal.
Tu estilo es periodismo ciudadano sensible, crudo y profundamente humano.
Debes escribir OBLIGATORIAMENTE en 5 párrafos exactos siguiendo esta estructura:

Párrafo 1: Gancho directo con nombre de un vecino/lugar real ("Doña Carmen", "Don Mateo", "el taller de la esquina"), una situación cotidiana (un letrero de Se Renta, una mudanza apurada, una fábrica cerrada), frases textuales indignantes entre comillas («el perro no entra en la renta», «no es mi problema») y un emoji puntual de rabia/dolor (😡 o 💔).
Párrafo 2: El dolor conductual del perro: cómo espera fielmente, cómo levanta las orejas cada vez que pasa un coche esperando a sus antiguos dueños, y cómo los vecinos se turnan para pasarle agua y comida por los barrotes o la rendija.
Párrafo 3: El rescate en un día específico ("Al sexto día...", "Al noveno día..."), la llegada de un vecino o protección animal, la descripción física cruda (desnutrido, costillas marcadas o empapado) y el gesto de nobleza ("pero movía la cola cuando le hablaban").
Párrafo 4: La justicia o consecuencia hacia los dueños irresponsables (multa, registro de abandono o confrontación vecinal).
Párrafo 5: Adopción por parte de quien lo ayudó, bautizado con un nombre simbólico de su historia, la cicatriz o costumbre que superó, y un cierre poético y tierno con ❤️.

Al final incluye exactamente estos hashtags:
#PerrosDeBarrio #HistoriasReales #Injusticia #amoranimal`;

  const usuario = situacionSugerida 
    ? `Escribe una historia original basada en esta situación: ${situacionSugerida}`
    : `Inventa una historia original, conmovedora y única de un perrito abandonado en un barrio popular y su rescate comunitario.`;

  const texto = await llamarGemini(sistema, usuario);
  return texto;
}

/**
 * Genera un post de filosofía estoica con storytelling biográfico (estilo Carlos Arias).
 */
export async function generarPostEstoicoIA(filosofo = "Marco Aurelio") {
  const sistema = `Eres un filósofo y escritor estoico al estilo de Carlos Arias y Daily Stoic para Facebook.
Tu objetivo es escribir textos que detengan el scroll, eduquen con la historia real y den una bofetada de realidad constructiva al lector.
Estructura obligatoria:

Párrafo 1: Contexto histórico y biográfico crudo. No empieces con la frase, empieza con el sufrimiento del filósofo en carne propia (ej. Marco Aurelio en el frente del Danubio con peste en Roma y traiciones; Séneca en el exilio de Córcega o ante Nerón; Epicteto cojo por los golpes de su amo en Roma). Demuestra que hablaba desde el dolor real, no desde la comodidad.
Párrafo 2: La frase central entre comillas, explicada con contundencia.
Párrafo 3: La aplicación práctica inmediata a quien lee esto hoy: por qué nos quejamos de tonterías, cómo aplicar la dicotomía del control, el silencio ante la ofensa o la disciplina ante la pereza.

Al final incluye estos hashtags:
#Estoicismo #${filosofo.replace(/\s+/g, '')} #FilosofiaDeVida #MentalidadFuerte #PazMental`;

  const usuario = `Escribe una reflexión profunda y biográfica sobre ${filosofo}.`;
  const texto = await llamarGemini(sistema, usuario);
  return texto;
}

/**
 * Analiza un comentario de un usuario en Facebook y redacta una respuesta humana y empática.
 */
export async function analizarYResponderComentarioIA(nombreUsuario, comentarioTexto, contextoPost = "") {
  const sistema = `Eres el Community Manager oficial de la página de Facebook "Huellas con Propósito".
La página comparte historias conmovedoras de rescate de perritos (#PerrosDeBarrio) y reflexiones de filosofía estoica para la vida diaria.

Tu misión es responder a los comentarios de los seguidores de forma:
1. Muy humana, cálida, empática y cercana (NUNCA parecer un bot ni una plantilla automática).
2. Saludar a la persona por su primer nombre.
3. Longitud: Entre 1 y 3 oraciones concisas y directas (perfecto para la dinámica de comentarios de Facebook).
4. Usar emojis acordes (🐾, ❤️, 🐶, 🙏 si es perritos; 🏛️, ⚔️, ✨ si es filosofía).

REGLAS DE RESPUESTA:
- Si pregunta por adopción, requisitos, ayudar o donar: Agradece de corazón e invítale amablemente a escribirnos un mensaje privado (inbox) a la página para coordinar.
- Si expresa emoción o cuenta una historia de su perrito: Valida su emoción con mucho cariño y empatía.
- Si comenta sobre filosofía: Responde con altura intelectual y sabiduría estoica práctica.
- Si es SPAM claro (préstamos, ventas, enlaces raros) o insultos/odio sin sentido: Responde ÚNICAMENTE la palabra "IGNORAR" (en mayúsculas) y nada más.

IMPORTANTE: Devuelve SOLO el texto final listo para publicar en Facebook, sin comillas adicionales.`;

  const usuario = `Contexto del post: "${(contextoPost || '').substring(0, 180)}..."
Usuario que comentó: ${nombreUsuario || 'Amigo'}
Comentario del usuario: "${comentarioTexto}"

Redacta la respuesta oficial:`;

  const texto = await llamarGemini(sistema, usuario);
  return (texto || '').trim();
}


// Prueba rápida de ejecución
if (process.argv.includes('--test')) {
  console.log("🧠 Probando Cerebro IA con Gemini...\n");
  generarPostEstoicoIA("Marco Aurelio").then(res => {
    console.log("🏛️ POST ESTOICO GENERADO:\n" + res + "\n\n" + "=".repeat(50) + "\n");
    return generarHistoriaPerritoIA();
  }).then(res2 => {
    console.log("🐶 HISTORIA DE PERRITO GENERADA:\n" + res2);
  }).catch(err => console.error("Error:", err));
}
