/**
 * PUBLICADOR EN VIVO AL MURO — METALIDAD DE ACERO
 * -----------------------------------------------------------
 * Publica contenido fresco y original DIRECTAMENTE EN EL MURO
 * (published: true — SIN planificar ni usar el programador de Meta).
 *
 * Características:
 * - Modo Mixto automático: alterna Foto con diseño V2 + Texto viral
 *   y publicaciones directas de Solo Texto de alto impacto.
 * - Impulsado por Google Gemini (con banco de respaldo integrado).
 * - Historial anti-repetición en mentalidad_de_acero/historial_muro_vivo.json.
 *
 * Uso:
 *   node publicador_muro_acero.js                (automático alternado)
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

const TEMAS_SEMILLA = [
  'el precio invisible de la disciplina diaria',
  'por qué callar tus planes te hace invencible',
  'la trampa de esperar motivación para actuar',
  'cómo el entorno mediocre te apaga sin que lo notes',
  'respeto propio: cumplir lo que te prometes a solas',
  'dominar tu mente cuando nadie te aplaude',
  'dejar de ser víctima de tus circunstancias',
  'el poder de entrenar el cuerpo para blindar la mente',
  'decir NO sin culpa para proteger tu misión',
  'por qué el confort es el enemigo silencioso del éxito',
  'transformar el rechazo y las derrotas en combustible',
  'vivir con estándares altos aunque te quedes solo',
  'la diferencia entre estar ocupado y avanzar de verdad',
  'cortar distracciones y dopamina barata',
  'paciencia estratégica y constancia implacable',
  'liderar con el ejemplo y no con discursos vacíos',
  'control emocional bajo máxima presión',
  'cerrar ciclos del pasado para conquistar el futuro'
];

const FALLBACK_SOLO_TEXTO = [
  {
    tema: 'disciplina en silencio',
    texto: `Nadie va a venir a salvarte.\n\nNo va a llegar un golpe de suerte, ni el momento perfecto, ni la motivación mágica un lunes por la mañana.\n\nLo único que cambia tu vida es cumplir lo que prometiste hacer, exactamente el día en que menos ganas tienes.\n\nLa disciplina en silencio construye lo que las excusas destruyen en voz alta.\n\n¿Qué acción difícil vas a completar hoy sin poner un solo pretexto? Te leo abajo. ⚔️\n\n#MentalidadDeAcero #Disciplina #SinExcusas #CrecimientoPersonal #Enfoque`
  },
  {
    tema: 'respeto propio',
    texto: `El respeto de los demás empieza el día en que dejas de negociar contigo mismo.\n\nCada vez que pospones la alarma, cada vez que rompes tu palabra en privado, tu mente registra que no eres de fiar.\n\nCumple una promesa pequeña hoy. Luego otra mañana. Así se forja una confianza que nadie puede quebrar.\n\nComenta un 🛡️ si hoy tu palabra se cumple sí o sí.\n\n#MentalidadDeAcero #Autodisciplina #FuerzaMental #HabitosDeAcero #Superacion`
  }
];

const FALLBACK_FOTO = [
  {
    tema: 'estándares innegociables',
    estilo: 'despertador',
    frase_principal: 'NO NEGOCIES CON LA MEDIOCRIDAD EN TU CABEZA',
    frase_secundaria: 'Tu estándar diario decide tu destino.',
    texto: `⚔️ "NO NEGOCIES CON LA MEDIOCRIDAD EN TU CABEZA" ⚔️\n\n¡DESPIERTA!\n\nEl hombre común negocia con su cansancio, negocia con la alarma y negocia con sus excusas. Al final del año se pregunta por qué su vida sigue exactamente igual.\n\nEl Hombre de Acero no discute con su pereza: la ejecuta a golpe de acción diaria.\n\n🔥 3 REGLAS PARA HOY:\n1. Haz primero lo que más estás evitando.\n2. Habla menos de tus metas y demuéstralas con hechos.\n3. No termines el día sin haber ganado al menos una batalla difícil.\n\nGuarda este post y comenta un ⚔️ si hoy vas por todo.\n\n#MentalidadDeAcero #Disciplina #SinExcusas #Enfoque #HombresDeAcero`
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

function elegirEstiloFoto(historial) {
  const estilos = ['despertador', 'contraste', 'estrategia', 'auditoria'];
  const fotosPrevias = historial.filter(h => h.tipo === 'foto');
  return estilos[fotosPrevias.length % estilos.length];
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

async function generarContenidoSoloTexto(historial, apiKey) {
  const temasRecientes = historial.slice(-15).map(h => h.tema).filter(Boolean);
  const semilla = TEMAS_SEMILLA[Math.floor(Math.random() * TEMAS_SEMILLA.length)];

  const prompt = `Eres el redactor principal de la página de Facebook "Metalidad de Acero" (disciplina, estoicismo moderno, superación personal, carácter implacable).

Redacta una publicación DIRECTA DE SOLO TEXTO para publicar en vivo en el muro de Facebook (sin imagen).
Debe ser magnética, fácil de leer en móvil, con párrafos de 1 a 2 líneas, tono firme, directo y inspirador (sin groserías ni odio, enfocado en responsabilidad personal y fuerza mental).

Tema sugerido: ${semilla}
Evita repetir estos temas recientes: ${temasRecientes.join(', ') || 'ninguno'}.

Reglas del texto:
- Empieza con una primera frase brutal que detenga el scroll.
- Desarrollo corto y contundente (entre 80 y 150 palabras).
- Cierra con una pregunta directa que invite a comentar.
- Agrega al final 4 o 5 hashtags relevantes (#MentalidadDeAcero #Disciplina ...).

Devuelve EXCLUSIVAMENTE un objeto JSON válido con estas claves:
{
  "tema": "resumen del tema en 3-5 palabras",
  "texto": "texto completo listo para publicar en Facebook"
}`;

  const generado = await llamarGeminiJSON(prompt, apiKey);
  if (generado?.texto) {
    return generado;
  }

  return FALLBACK_SOLO_TEXTO[historial.length % FALLBACK_SOLO_TEXTO.length];
}

async function generarContenidoConFoto(estilo, historial, apiKey) {
  const temasRecientes = historial.slice(-15).map(h => h.tema).filter(Boolean);
  const semilla = TEMAS_SEMILLA[Math.floor(Math.random() * TEMAS_SEMILLA.length)];
  const numeroLey = historial.filter(h => h.tipo === 'foto').length + 1;

  let estructuraEspecifica = '';
  if (estilo === 'despertador') {
    estructuraEspecifica = `{
  "tema": "resumen en 3-5 palabras",
  "frase_principal": "FRASE CORTA DE MAXIMO 9 PALABRAS EN MAYUSCULAS",
  "frase_secundaria": "Frase secundaria de máximo 10 palabras",
  "texto": "Copy viral completo para Facebook (120-180 palabras, gancho, 3 reglas numeradas con 🔥, CTA para comentar ⚔️ y 5 hashtags)"
}`;
  } else if (estilo === 'contraste') {
    estructuraEspecifica = `{
  "tema": "resumen en 3-5 palabras",
  "arquetipo": "EL [NOMBRE CORTO DEL ARQUETIPO DEBIL, MAX 4 PALABRAS]",
  "rasgos_debil": ["6 frases cortas max 3 palabras c/u"],
  "rasgos_acero": ["6 frases cortas max 3 palabras c/u"],
  "sentencia": "Frase sentencia final de máximo 14 palabras",
  "texto": "Copy viral completo para Facebook contrastando ambas mentalidades, CTA para comentar 🛡️ y 5 hashtags"
}`;
  } else if (estilo === 'estrategia') {
    estructuraEspecifica = `{
  "tema": "resumen en 3-5 palabras",
  "titulo_ley": "LEY DE [MAX 4 PALABRAS]",
  "regla_principal": "REGLA CONTUNDENTE DE MAXIMO 10 PALABRAS",
  "principios": [
    {"titulo": "TITULO 1 (2-3 palabras)", "detalle": "Explicación breve max 9 palabras"},
    {"titulo": "TITULO 2 (2-3 palabras)", "detalle": "Explicación breve max 9 palabras"},
    {"titulo": "TITULO 3 (2-3 palabras)", "detalle": "Explicación breve max 9 palabras"}
  ],
  "texto": "Copy viral completo para Facebook explicando estos 3 principios, CTA para comentar 🏛️ y 5 hashtags"
}`;
  } else {
    estructuraEspecifica = `{
  "tema": "resumen en 3-5 palabras",
  "pregunta": "¿PREGUNTA DIRECTA DE CONFRONTACION DE MAXIMO 14 PALABRAS?",
  "desafio": "Frase corta de reto (máximo 8 palabras)",
  "texto": "Copy viral nocturno/reflexivo para Facebook invitando a una autoevaluación honesta en comentarios y 5 hashtags"
}`;
  }

  const prompt = `Eres el director creativo de la página de Facebook "Metalidad de Acero" (disciplina, estoicismo moderno, superación personal).
Crea una publicación NUEVA e INÉDITA con imagen estilo "${estilo}" para publicar en vivo en el muro.

Tema sugerido: ${semilla}
NO repitas estos temas recientes: ${temasRecientes.join(', ') || 'ninguno'}.

Devuelve EXCLUSIVAMENTE un JSON válido con exactamente esta estructura:
${estructuraEspecifica}`;

  const generado = await llamarGeminiJSON(prompt, apiKey);
  if (generado?.texto) {
    return { ...generado, estilo, numero: numeroLey };
  }

  return { ...FALLBACK_FOTO[0], numero: numeroLey };
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

  console.log('='.repeat(68));
  console.log('⚡ PUBLICADOR EN VIVO AL MURO — METALIDAD DE ACERO');
  console.log(`   Modo solicitado: ${modoArg} | Simulación: ${simular ? 'SÍ' : 'NO'}`);
  console.log('='.repeat(68));

  const { pageId, token, geminiKey } = cargarCredenciales();
  if (!token || !pageId) {
    console.error('❌ Error: Falta META_ACCESS_TOKEN_ACERO o PAGE_ID_ACERO.');
    process.exit(1);
  }

  const historial = cargarHistorial();
  const tipo = decidirTipoPublicacion(modoArg, historial);
  console.log(`📌 Formato seleccionado para esta publicación en vivo: ${tipo.toUpperCase()}`);

  let resultado = null;
  let registro = null;

  if (tipo === 'texto') {
    const contenido = await generarContenidoSoloTexto(historial, geminiKey);
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
        estilo: 'solo_texto',
        tema: contenido.tema,
        texto_preview: contenido.texto.substring(0, 140),
        meta_post_id: postId,
        url: `https://www.facebook.com/${postId}`
      };
    }
  } else {
    const estilo = elegirEstiloFoto(historial);
    console.log(`🎨 Estilo gráfico V2 elegido: ${estilo.toUpperCase()}`);
    const contenido = await generarContenidoConFoto(estilo, historial, geminiKey);

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
