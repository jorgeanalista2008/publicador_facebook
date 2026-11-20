/**
 * PUBLICADOR EN VIVO AL MURO — METALIDAD DE ACERO (v2 — Optimizado por Datos Reales)
 * ----------------------------------------------------------------------------------
 * Publica contenido fresco y original DIRECTAMENTE EN EL MURO
 * (published: true — SIN planificar ni usar el programador de Meta).
 *
 * Estrategia basada en el rendimiento real de la página:
 * - 40% Anécdotas reales de Sabios y Estrategas Antiguos (Confucio, Diógenes,
 *   Sócrates, Sun Tzu, Marco Aurelio, Séneca, Maquiavelo, Musashi).
 * - 40% Psicología Humana, Estrategia y Lectura de Personas (Carl Jung,
 *   hipocresía, límites, respeto, silencio estratégico).
 * - 20% Verdades Incómodas sobre la Sociedad Actual.
 *
 * Conversión de vistas a seguidores integrada en cada post:
 * - Formato de Serie Numerada (efecto bucle abierto).
 * - Pregunta polarizadora de respuesta rápida (SÍ/NO o 1/2/3) para activar comentarios.
 * - Llamado directo a seguir la página con identidad y promesa de valor.
 *
 * Uso:
 *   node publicador_muro_acero.js                (automático alternado foto <-> texto)
 *   node publicador_muro_acero.js --modo=texto   (forzar solo texto)
 *   node publicador_muro_acero.js --modo=foto    (forzar foto V2 + texto)
 *   node publicador_muro_acero.js --simular      (prueba sin publicar en Meta)
 */

import fs from 'fs';
import os from 'os';
import path from 'path';
import { execFileSync } from 'child_process';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const CONFIG_PATH = path.join(__dirname, 'config.json');
const HISTORIAL_PATH = path.join(__dirname, 'mentalidad_de_acero', 'historial_muro_vivo.json');
const PYTHON_IMG_SCRIPT = path.join(__dirname, 'generar_imagen_viva_acero.py');

// Distribución 40% Sabios Antiguos | 40% Psicología y Estrategia | 20% Verdades Actuales
const PILARES = [
  {
    clave: 'sabios_antiguos',
    nombreSerie: 'Lecciones de Sabios Antiguos',
    peso: 40,
    estilosFoto: ['despertador', 'estrategia'],
    semillas: [
      'Diógenes y su respuesta brutal a Alejandro Magno sobre el verdadero poder',
      'Confucio y por qué el hombre superior habla lento pero actúa rápido',
      'Sócrates y el filtro de los 3 tamices contra el chisme y la hipocresía',
      'Sun Tzu y cómo ganar una batalla antes de dar el primer golpe',
      'Marco Aurelio gobernando un imperio mientras dominaba su propia ira',
      'Séneca sobre cómo el miedo a sufrir nos hace sufrir dos veces',
      'Epicteto, el esclavo que fue más libre que los emperadores de Roma',
      'Miyamoto Musashi y la calma letal en medio del caos',
      'Baltasar Gracián sobre no mostrar todas tus cartas ni depender de nadie',
      'Maquiavelo sobre por qué es más seguro leer las acciones que las promesas',
      'Arthur Schopenhauer sobre el precio de pensar diferente a la multitud',
      'Aristóteles sobre cómo el carácter se revela en lo que repites en silencio'
    ]
  },
  {
    clave: 'psicologia_estrategia',
    nombreSerie: 'Psicología & Estrategia',
    peso: 40,
    estilosFoto: ['estrategia', 'contraste'],
    semillas: [
      'Carl Jung sobre integrar tu sombra: ser inofensivo no es ser bueno',
      'Cómo detectar a quien te adula de frente pero te envidia por la espalda',
      'Tu problema no es que seas buena persona, es que no tienes estrategia ni límites',
      'Por qué el silencio incómodo obliga a los manipuladores a revelar sus intenciones',
      '3 señales psicológicas de que alguien te respeta de verdad (y no solo te utiliza)',
      'Quien no se adapta se rompe: la flexibilidad estratégica del hombre sabio',
      'Cómo reaccionar con frialdad cuando alguien intenta provocarte para hacerte quedar mal',
      'Por qué contar tus planes antes de tiempo sabotea tu mente y despierta envidias',
      'La diferencia entre ser amable por valor y ser complaciente por miedo al rechazo',
      'Señales silenciosas de inteligencia emocional superior en medio de un conflicto',
      'Por qué alejarte sin dar explicaciones es a veces la respuesta más poderosa',
      'Cómo poner un límite firme en una sola frase sin perder la elegancia'
    ]
  },
  {
    clave: 'verdades_actuales',
    nombreSerie: 'Verdades Incómodas',
    peso: 20,
    estilosFoto: ['auditoria', 'despertador'],
    semillas: [
      'Vivimos en una época donde la gente consume miles de videos pero ya no lee ni analiza',
      'Todos quieren lealtad de película, pero nadie está dispuesto a ser leal cuando incomoda',
      'La mayoría no quiere mejorar su vida, solo quiere distraerse lo suficiente para no sentirla',
      'Hoy se premia aparentar éxito en redes más que construir paz y patrimonio en silencio',
      'La gente confunde estar ocupado todo el día con estar avanzando hacia algo real',
      'Nos enseñaron a evitar cualquier incomodidad y terminamos creando mentes frágiles'
    ]
  }
];

const CTAS_SEGUIMIENTO = [
  'Si valoras la psicología real y la sabiduría antigua sin adornos, sigue a Metalidad de Acero para recibir una lección diaria que te abra los ojos.',
  'Guarda este post para releerlo cuando lo necesites y sigue a Metalidad de Acero si prefieres la verdad cruda antes que las frases vacías.',
  'Cada día compartimos historias de sabios y estrategias de psicología humana. Sigue a Metalidad de Acero para no perderte la siguiente parte de la serie.',
  'Si eres de los pocos que eligen pensar con estrategia y profundidad, sigue a Metalidad de Acero — nos leemos en la próxima lección.'
];

const FALLBACK_SOLO_TEXTO = [
  {
    pilar: 'sabios_antiguos',
    tema: 'Diógenes y el verdadero poder',
    texto: `Lecciones de Sabios Antiguos #01 🏛️\n\nAlejandro Magno, el hombre más poderoso del mundo, viajó a conocer a Diógenes y le dijo: «Pídeme lo que quieras».\n\nDiógenes, sentado en el suelo sin una sola moneda, lo miró tranquilo y le respondió: «Apártate, que me tapas el sol».\n\nLos generales se burlaron, pero Alejandro guardó silencio y dijo: «Si yo no fuera Alejandro, querría ser Diógenes».\n\n¿Por qué un conquistador admiró a un hombre que no tenía nada?\n\nPorque el hombre más peligroso e invencible no es el que más posee, sino aquel a quien nadie puede comprar ni intimidar.\n\n¿Qué pesa más en tu vida hoy: la libertad o la aprobación de otros? Responde en 1 palabra abajo. 👇\n\nSi valoras la sabiduría antigua sin adornos, sigue a Metalidad de Acero para no perderte la siguiente lección diaria.\n\n#MentalidadDeAcero #Filosofia #Diogenes #Estoicismo #PsicologiaHumana`
  },
  {
    pilar: 'psicologia_estrategia',
    tema: 'Detectar la adulación falsa',
    texto: `Psicología & Estrategia #01 ♟️\n\nDesconfía más de quien te aplaude todo sin criterio que de quien te dice una verdad incómoda de frente.\n\nLa adulación exagerada rara vez nace de la admiración. Casi siempre es una herramienta para bajar tu guardia y obtener algo de ti.\n\n3 señales de que alguien te adula por interés:\n1. Te elogia en público, pero desaparece cuando necesitas ayuda real.\n2. Cambia de opinión según quién esté en la habitación.\n3. Se incomoda en silencio cuando realmente te va mejor que a él.\n\n¿Alguna vez te traicionó alguien que te adulaba de frente? Responde SÍ o NO abajo. 👇\n\nSi te gusta aprender a leer a las personas con claridad, sigue a Metalidad de Acero para recibir la próxima entrega de la serie.\n\n#MentalidadDeAcero #PsicologiaHumana #Estrategia #InteligenciaEmocional #Sabiduria`
  }
];

const FALLBACK_FOTO = [
  {
    pilar: 'psicologia_estrategia',
    tema: 'Estrategia sobre ingenuidad',
    estilo: 'estrategia',
    titulo_ley: 'PSICOLOGÍA & ESTRATEGIA',
    regla_principal: 'TU PROBLEMA NO ES SER BUENO, ES NO TENER ESTRATEGIA',
    principios: [
      { titulo: 'OBSERVA HECHOS', detalle: 'Las promesas no cuestan nada; los actos revelan todo.' },
      { titulo: 'PON LÍMITES', detalle: 'Sin límites claros, tu bondad será usada en tu contra.' },
      { titulo: 'CALLA TUS PLANES', detalle: 'El silencio protege tus movimientos de la envidia.' }
    ],
    texto: `Psicología & Estrategia #01 ♟️\n\nSer buena persona sin límites ni estrategia no es virtud: es dejarte a merced de quien no tiene escrúpulos.\n\nCarl Jung advertía que una persona incapaz de defenderse no es «buena», simplemente es inofensiva. La verdadera nobleza consiste en tener fuerza, criterio y estrategia, y elegir usarlos con justicia.\n\n3 reglas para proteger tu paz:\n1. Observa patrones repetidos, no disculpas bonitas.\n2. Di NO a tiempo sin sentir culpa.\n3. Protege tus planes en silencio hasta que sean hechos.\n\n¿Cuál de estas 3 reglas te costó más aprender? Escribe 1, 2 o 3 abajo. 👇\n\nGuarda este post y sigue a Metalidad de Acero para no perderte la siguiente entrega de la serie.\n\n#MentalidadDeAcero #PsicologiaHumana #CarlJung #Estrategia #Estoicismo`
  }
];

function cargarCredenciales() {
  let cfg = {};
  if (fs.existsSync(CONFIG_PATH)) {
    try {
      cfg = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf-8'));
    } catch (e) {
      console.warn(`Aviso leyendo config.json: ${e.message}`);
    }
  }

  const pageId =
    process.env.PAGE_ID_ACERO ||
    cfg.PAGINAS?.mentalidad_de_acero?.id ||
    '1375923958937880';

  const token =
    process.env.META_ACCESS_TOKEN_ACERO ||
    cfg.PAGINAS?.mentalidad_de_acero?.token;

  const geminiKey =
    process.env.GEMINI_API_KEY ||
    cfg.GEMINI_API_KEY;

  return { pageId, token, geminiKey };
}

function cargarHistorial() {
  if (!fs.existsSync(HISTORIAL_PATH)) {
    return [];
  }
  try {
    return JSON.parse(fs.readFileSync(HISTORIAL_PATH, 'utf-8'));
  } catch {
    return [];
  }
}

function guardarHistorial(historial) {
  fs.mkdirSync(path.dirname(HISTORIAL_PATH), { recursive: true });
  fs.writeFileSync(HISTORIAL_PATH, JSON.stringify(historial, null, 2), 'utf-8');
}

function decidirTipoPublicacion(modoArg, historial) {
  if (modoArg === 'foto' || modoArg === 'texto') {
    return modoArg;
  }
  if (historial.length === 0) {
    return 'foto';
  }
  const ultimoTipo = historial[historial.length - 1].tipo;
  return ultimoTipo === 'foto' ? 'texto' : 'foto';
}

function elegirPilar(historial) {
  // Rotación ponderada determinista: 40% sabios, 40% psicologia, 20% verdades
  // Patron de 5: sabios, psicologia, sabios, psicologia, verdades
  const secuencia = ['sabios_antiguos', 'psicologia_estrategia', 'sabios_antiguos', 'psicologia_estrategia', 'verdades_actuales'];
  const clave = secuencia[historial.length % secuencia.length];
  return PILARES.find(p => p.clave === clave) || PILARES[0];
}

function numeroSeriePilar(pilarClave, historial) {
  return historial.filter(h => h.pilar === pilarClave).length + 1;
}

function elegirEstiloFoto(pilar, historial) {
  const fotosEnPilar = historial.filter(h => h.tipo === 'foto' && h.pilar === pilar.clave).length;
  return pilar.estilosFoto[fotosEnPilar % pilar.estilosFoto.length];
}

async function llamarGeminiJSON(prompt, apiKey) {
  if (!apiKey) return null;

  const modelos = ['gemini-3.5-flash', 'gemini-3.1-flash-lite', 'gemini-flash-latest'];
  for (const modelo of modelos) {
    const url = `https://generativelanguage.googleapis.com/v1beta/models/${modelo}:generateContent?key=${apiKey}`;
    try {
      const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          contents: [{ role: 'user', parts: [{ text: prompt }] }],
          generationConfig: {
            temperature: 0.9,
            maxOutputTokens: 4096,
            responseMimeType: 'application/json'
          }
        })
      });

      if (!res.ok) continue;
      const data = await res.json();
      const raw = data?.candidates?.[0]?.content?.parts?.[0]?.text;
      if (!raw) continue;

      const cleaned = raw.replace(/^```json\s*/i, '').replace(/```\s*$/i, '').trim();
      return JSON.parse(cleaned);
    } catch (err) {
      console.warn(`⚠️ Modelo ${modelo} falló: ${err.message}`);
    }
  }
  return null;
}

async function generarContenidoSoloTexto(pilar, numSerie, historial, apiKey) {
  const temasRecientes = historial.slice(-18).map(h => h.tema).filter(Boolean);
  const semilla = pilar.semillas[Math.floor(Math.random() * pilar.semillas.length)];
  const ctaSeguir = CTAS_SEGUIMIENTO[historial.length % CTAS_SEGUIMIENTO.length];
  const etiquetaSerie = `${pilar.nombreSerie} #${String(numSerie).padStart(2, '0')}`;

  const prompt = `Eres el estratega editorial de la página de Facebook "Metalidad de Acero" (filosofía práctica, sabios antiguos, psicología humana y estrategia vital).
Tu estilo es inteligente, narrativo, sereno pero afilado — NUNCA uses gritos cliché tipo "¡DESPIERTA!" ni motivación barata.

Redacta una publicación DIRECTA DE SOLO TEXTO para publicar en vivo en el muro de Facebook (sin imagen).

Serie y número obligatorio en la primera línea: "${etiquetaSerie}"
Pilar editorial: ${pilar.clave}
Semilla / inspiración: ${semilla}
Evita repetir estos temas recientes: ${temasRecientes.join(', ') || 'ninguno'}.

Reglas obligatorias para maximizar alcance Y convertir lectores en SEGUIDORES:
1. Primera línea: "${etiquetaSerie}" seguido de un emoji sobrio (🏛️, ♟️ o 🧠).
2. Gancho narrativo en la segunda línea: si es sabios_antiguos, abre directo con la anécdota histórica real y un giro sorprendente; si es psicologia_estrategia o verdades_actuales, abre con una verdad psicológica aguda que detenga el scroll.
3. Desarrollo limpio en párrafos cortos de 1 a 2 líneas (entre 100 y 170 palabras en total), fácil de leer en móvil.
4. Incluye una PREGUNTA POLARIZADORA DE RESPUESTA RÁPIDA al final (que se pueda responder con SÍ/NO, 1 palabra, o eligiendo 1, 2 o 3) para provocar comentarios.
5. Justo antes de los hashtags, incluye este llamado a seguir adaptado de forma natural: "${ctaSeguir}"
6. Cierra con 4 o 5 hashtags precisos (#MentalidadDeAcero #PsicologiaHumana #Estoicismo ...).

Devuelve EXCLUSIVAMENTE un objeto JSON válido:
{
  "tema": "resumen del tema en 3-5 palabras",
  "texto": "texto completo listo para publicar en Facebook"
}`;

  const generado = await llamarGeminiJSON(prompt, apiKey);
  if (generado?.texto) {
    return { ...generado, pilar: pilar.clave, serie: etiquetaSerie };
  }

  const fb = FALLBACK_SOLO_TEXTO[historial.length % FALLBACK_SOLO_TEXTO.length];
  return { ...fb, serie: etiquetaSerie };
}

async function generarContenidoConFoto(pilar, numSerie, estilo, historial, apiKey) {
  const temasRecientes = historial.slice(-18).map(h => h.tema).filter(Boolean);
  const semilla = pilar.semillas[Math.floor(Math.random() * pilar.semillas.length)];
  const ctaSeguir = CTAS_SEGUIMIENTO[historial.length % CTAS_SEGUIMIENTO.length];
  const etiquetaSerie = `${pilar.nombreSerie} #${String(numSerie).padStart(2, '0')}`;

  let estructuraEspecifica = '';
  if (estilo === 'despertador') {
    estructuraEspecifica = `{
  "tema": "resumen en 3-5 palabras",
  "frase_principal": "FRASE CORTA E INTELIGENTE DE MAXIMO 9 PALABRAS EN MAYUSCULAS",
  "frase_secundaria": "Subtítulo reflexivo de máximo 10 palabras",
  "texto": "Copy completo (120-180 palabras): abre con '${etiquetaSerie}', cuenta la historia/lección psicológica con profundidad, cierra con pregunta rápida (SÍ/NO o 1/2/3), incluye '${ctaSeguir}' y 5 hashtags"
}`;
  } else if (estilo === 'contraste') {
    estructuraEspecifica = `{
  "tema": "resumen en 3-5 palabras",
  "arquetipo": "NOMBRE CORTO DEL CONTRASTE (MAX 4 PALABRAS, SIN EMOJIS)",
  "rasgos_debil": ["6 frases cortas max 3 palabras c/u sobre la ingenuidad/mentalidad débil"],
  "rasgos_acero": ["6 frases cortas max 3 palabras c/u sobre la estrategia/mentalidad sabia"],
  "sentencia": "Frase sentencia final de máximo 13 palabras",
  "texto": "Copy completo (120-180 palabras): abre con '${etiquetaSerie}', desarrolla la lección psicológica, pregunta rápida (SÍ/NO o 1/2/3), incluye '${ctaSeguir}' y 5 hashtags"
}`;
  } else if (estilo === 'estrategia') {
    estructuraEspecifica = `{
  "tema": "resumen en 3-5 palabras",
  "titulo_ley": "TITULO CORTO DE LA SERIE O LEY (MAX 4 PALABRAS, SIN EMOJIS)",
  "regla_principal": "IDEA CENTRAL DE MAXIMO 10 PALABRAS EN MAYUSCULAS",
  "principios": [
    {"titulo": "TITULO 1 (2-3 palabras)", "detalle": "Explicación breve max 9 palabras"},
    {"titulo": "TITULO 2 (2-3 palabras)", "detalle": "Explicación breve max 9 palabras"},
    {"titulo": "TITULO 3 (2-3 palabras)", "detalle": "Explicación breve max 9 palabras"}
  ],
  "texto": "Copy completo (120-180 palabras): abre con '${etiquetaSerie}', desarrolla la anécdota o principio psicológico, cierra con pregunta rápida (1, 2 o 3), incluye '${ctaSeguir}' y 5 hashtags"
}`;
  } else {
    estructuraEspecifica = `{
  "tema": "resumen en 3-5 palabras",
  "pregunta": "¿PREGUNTA INCOMODA Y PROFUNDA DE MAXIMO 14 PALABRAS?",
  "desafio": "Frase corta de reflexión (máximo 8 palabras)",
  "texto": "Copy completo (110-160 palabras): abre con '${etiquetaSerie}', reflexiona con agudeza sobre la sociedad actual, pregunta directa de respuesta corta, incluye '${ctaSeguir}' y 5 hashtags"
}`;
  }

  const prompt = `Eres el director creativo de la página de Facebook "Metalidad de Acero" (sabios antiguos, psicología humana, estrategia y verdades incómodas).
Tu tono es culto, afilado, psicológico y narrativo — evita gritos cliché tipo "¡DESPIERTA!".

Crea una publicación NUEVA e INÉDITA con diseño gráfico "${estilo}" para publicar en vivo en el muro.
Serie: "${etiquetaSerie}"
Pilar editorial: ${pilar.clave}
Semilla / inspiración: ${semilla}
NO repitas estos temas recientes: ${temasRecientes.join(', ') || 'ninguno'}.
IMPORTANTE: En los campos que van DENTRO de la imagen (frase_principal, arquetipo, titulo_ley, pregunta, etc.) NO pongas emojis.

Devuelve EXCLUSIVAMENTE un JSON válido con exactamente esta estructura:
${estructuraEspecifica}`;

  const generado = await llamarGeminiJSON(prompt, apiKey);
  if (generado?.texto) {
    return { ...generado, estilo, numero: numSerie, pilar: pilar.clave, serie: etiquetaSerie };
  }

  return { ...FALLBACK_FOTO[0], numero: numSerie, serie: etiquetaSerie };
}

function renderizarImagenV2(datosImagen, outputPath) {
  const tmpJson = path.join(os.tmpdir(), `acero_live_${Date.now()}.json`);
  fs.writeFileSync(tmpJson, JSON.stringify(datosImagen, null, 2), 'utf-8');

  const pythonCmd = process.platform === 'win32' ? 'python' : 'python3';
  try {
    const out = execFileSync(pythonCmd, [PYTHON_IMG_SCRIPT, tmpJson, outputPath], {
      encoding: 'utf-8',
      stdio: 'pipe'
    });
    if (out) console.log(out.trim());
  } finally {
    if (fs.existsSync(tmpJson)) fs.unlinkSync(tmpJson);
  }
}

async function publicarSoloTextoEnVivo(pageId, token, mensaje) {
  const url = `https://graph.facebook.com/v19.0/${pageId}/feed`;
  const params = new URLSearchParams();
  params.append('message', mensaje);
  params.append('published', 'true');
  params.append('access_token', token);

  const res = await fetch(url, {
    method: 'POST',
    body: params
  });
  return { ok: res.ok, status: res.status, data: await res.json() };
}

async function publicarFotoEnVivo(pageId, token, caption, imgPath) {
  const url = `https://graph.facebook.com/v19.0/${pageId}/photos`;
  const formData = new FormData();
  formData.append('caption', caption);
  formData.append('published', 'true');
  formData.append('access_token', token);

  const fileBuffer = fs.readFileSync(imgPath);
  const blob = new Blob([fileBuffer], { type: 'image/jpeg' });
  formData.append('source', blob, path.basename(imgPath));

  const res = await fetch(url, {
    method: 'POST',
    body: formData
  });
  return { ok: res.ok, status: res.status, data: await res.json() };
}

async function main() {
  const args = process.argv.slice(2);
  const simular = args.includes('--simular');
  const modoArg =
    args.find(a => a.startsWith('--modo='))?.split('=')[1] ||
    (args.includes('--solo-texto') ? 'texto' : args.includes('--con-foto') ? 'foto' : 'auto');

  console.log('='.repeat(70));
  console.log('⚡ PUBLICADOR EN VIVO AL MURO v2 — METALIDAD DE ACERO');
  console.log(`   Modo solicitado: ${modoArg} | Simulación: ${simular ? 'SÍ' : 'NO'}`);
  console.log('='.repeat(70));

  const { pageId, token, geminiKey } = cargarCredenciales();
  if (!token || !pageId) {
    console.error('❌ Error: Falta META_ACCESS_TOKEN_ACERO o PAGE_ID_ACERO.');
    process.exit(1);
  }

  const historial = cargarHistorial();
  const tipo = decidirTipoPublicacion(modoArg, historial);
  const pilar = elegirPilar(historial);
  const numSerie = numeroSeriePilar(pilar.clave, historial);

  console.log(`📌 Formato: ${tipo.toUpperCase()} | Pilar: ${pilar.nombreSerie} #${String(numSerie).padStart(2, '0')}`);

  let resultado = null;
  let registro = null;

  if (tipo === 'texto') {
    const contenido = await generarContenidoSoloTexto(pilar, numSerie, historial, geminiKey);
    console.log(`\n📝 Tema: ${contenido.tema}`);
    console.log(`--- VISTA PREVIA TEXTO ---\n${contenido.texto}\n--------------------------`);

    if (simular) {
      console.log('\n🧪 [SIMULACIÓN] No se envió a Facebook.');
      return;
    }

    console.log('\n🚀 Publicando EN VIVO en el muro (/feed, published=true)...');
    resultado = await publicarSoloTextoEnVivo(pageId, token, contenido.texto.trim());

    if (resultado.ok && resultado.data?.id) {
      const postId = resultado.data.id;
      registro = {
        id: historial.length + 1,
        fecha_utc: new Date().toISOString(),
        tipo: 'texto',
        pilar: pilar.clave,
        serie: contenido.serie,
        estilo: 'solo_texto',
        tema: contenido.tema,
        texto_preview: contenido.texto.substring(0, 140),
        meta_post_id: postId,
        url: `https://www.facebook.com/${postId}`
      };
    }
  } else {
    const estilo = elegirEstiloFoto(pilar, historial);
    console.log(`🎨 Estilo gráfico V2 elegido: ${estilo.toUpperCase()}`);
    const contenido = await generarContenidoConFoto(pilar, numSerie, estilo, historial, geminiKey);

    const tmpImgPath = path.join(os.tmpdir(), `muro_acero_${Date.now()}.jpg`);
    renderizarImagenV2(contenido, tmpImgPath);

    console.log(`\n📝 Tema: ${contenido.tema}`);
    console.log(`--- VISTA PREVIA COPY ---\n${contenido.texto}\n-------------------------`);

    if (simular) {
      console.log(`\n🧪 [SIMULACIÓN] Imagen generada en: ${tmpImgPath}`);
      console.log('🧪 [SIMULACIÓN] No se envió a Facebook.');
      return;
    }

    try {
      console.log('\n🚀 Publicando FOTO EN VIVO en el muro (/photos, published=true)...');
      resultado = await publicarFotoEnVivo(pageId, token, contenido.texto.trim(), tmpImgPath);
    } finally {
      if (fs.existsSync(tmpImgPath)) fs.unlinkSync(tmpImgPath);
    }

    if (resultado.ok && (resultado.data?.post_id || resultado.data?.id)) {
      const postId = resultado.data.post_id || resultado.data.id;
      registro = {
        id: historial.length + 1,
        fecha_utc: new Date().toISOString(),
        tipo: 'foto',
        pilar: pilar.clave,
        serie: contenido.serie,
        estilo,
        tema: contenido.tema,
        texto_preview: contenido.texto.substring(0, 140),
        meta_post_id: postId,
        url: `https://www.facebook.com/${postId}`
      };
    }
  }

  if (registro) {
    historial.push(registro);
    guardarHistorial(historial);
    console.log(`\n✅ ¡PUBLICADO EN VIVO CON ÉXITO!`);
    console.log(`   🆔 Meta Post ID: ${registro.meta_post_id}`);
    console.log(`   🔗 Enlace directo: ${registro.url}`);
    console.log(`   📚 Total histórico en muro en vivo: ${historial.length}`);
  } else {
    console.error('❌ Error publicando en Meta:', JSON.stringify(resultado?.data || resultado, null, 2));
    process.exit(1);
  }
}

main().catch(err => {
  console.error('❌ Error fatal:', err);
  process.exit(1);
});
