/**
 * PUBLICADOR AUTOMÁTICO EXCLUSIVO DE PERRITOS PARA INSTAGRAM
 * -----------------------------------------------------------
 * Publica HISTORIAS REALES DE PERRITOS (Fotos y Reels verticales 9:16)
 * en la cuenta oficial @huellasconproposito26 usando la Meta Graph API v19.0.
 * 
 * Modos de uso:
 *   node publicador_instagram_perritos.js --foto      (Publica una foto con historia)
 *   node publicador_instagram_perritos.js --reel      (Publica un Reel en video con locución)
 *   node publicador_instagram_perritos.js --auto      (Publica la siguiente entrega pendiente)
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const CONFIG_PATH = path.join(__dirname, 'config.json');
const HISTORIAL_PATH = path.join(__dirname, 'instagram_perritos_historial.json');
const REELS_INDEX_PATH = path.join(__dirname, 'videos_reels_perritos', 'reels_perritos_index.json');
const POSTS_PATH = path.join(__dirname, 'noviembre', 'publicaciones.json');

const GITHUB_RAW_BASE = 'https://raw.githubusercontent.com/jorgeanalista2008/publicador_facebook/main/';
const GITHUB_PAGES_BASE = 'https://jorgeanalista2008.github.io/publicador_facebook/';

function cargarCredenciales() {
  let cfg = {};
  if (fs.existsSync(CONFIG_PATH)) {
    cfg = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf-8'));
  }

  const token = process.env.META_ACCESS_TOKEN || cfg.PAGINAS?.huellas_con_proposito?.token || cfg.ACCESS_TOKEN;
  const igUserId = process.env.IG_USER_ID || cfg.PAGINAS?.huellas_con_proposito?.instagram?.id;

  return { token, igUserId };
}

function cargarHistorial() {
  if (fs.existsSync(HISTORIAL_PATH)) {
    try {
      return JSON.parse(fs.readFileSync(HISTORIAL_PATH, 'utf-8'));
    } catch (e) {}
  }
  return { publicaciones: [], ultimo_tipo: 'reel' };
}

function guardarHistorial(historial) {
  fs.writeFileSync(HISTORIAL_PATH, JSON.stringify(historial, null, 2), 'utf-8');
}

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

/**
 * Espera a que Meta procese el contenedor de video de Reel
 */
async function esperarProcesamientoReel(creationId, token, maxIntentos = 25) {
  for (let i = 1; i <= maxIntentos; i++) {
    process.stdout.write(`   ⏳ Verificando procesamiento Meta (intento ${i}/${maxIntentos})... `);
    try {
      const res = await fetch(`https://graph.facebook.com/v19.0/${creationId}?fields=status_code,status&access_token=${token}`);
      const data = await res.json();
      const code = data.status_code;

      if (code === 'FINISHED') {
        console.log('✅ ¡PROCESADO LISTO!');
        return true;
      } else if (code === 'IN_PROGRESS') {
        console.log('en progreso...');
        await sleep(5000);
      } else if (code === 'ERROR') {
        console.log('❌ Error en el video:', data);
        return false;
      } else {
        console.log(`estado: ${code || JSON.stringify(data)}`);
        await sleep(5000);
      }
    } catch (e) {
      console.log('error de red, reintentando...');
      await sleep(5000);
    }
  }
  return false;
}

/**
 * Publica una Foto con historia en Instagram Feed
 */
async function publicarFotoPerrito(token, igUserId) {
  console.log('\n🐾 [FOTO PERRITO] Iniciando publicación en @huellasconproposito26...');

  if (!fs.existsSync(POSTS_PATH)) {
    console.error('❌ No se encontró publicaciones.json');
    return null;
  }

  const posts = JSON.parse(fs.readFileSync(POSTS_PATH, 'utf-8'));
  const perritos = posts.filter(p => p.tipo === 'perrito');
  const historial = cargarHistorial();
  const publicadosIds = new Set(historial.publicaciones.filter(p => p.tipo === 'foto').map(p => p.post_id));

  // Buscar el siguiente perrito pendiente
  let candidato = perritos.find(p => !publicadosIds.has(p.id));
  if (!candidato) {
    candidato = perritos[0]; // Si ya se publicaron todos, reiniciar ciclo
  }

  const imageUrl = `${GITHUB_RAW_BASE}${candidato.ruta_imagen}`;
  const caption = `🐾 ${candidato.titulo}\n\n${candidato.texto}\n\n${candidato.hashtags || ''}`.trim();

  console.log(`   Perrito: ${candidato.titulo}`);
  console.log(`   Imagen URL: ${imageUrl}`);

  // 1. Crear contenedor de imagen
  const params1 = new URLSearchParams();
  params1.append('image_url', imageUrl);
  params1.append('caption', caption);
  params1.append('access_token', token);

  const res1 = await fetch(`https://graph.facebook.com/v19.0/${igUserId}/media`, {
    method: 'POST',
    body: params1
  });

  const data1 = await res1.json();
  if (!res1.ok || !data1.id) {
    console.error('❌ Error creando contenedor de foto:', data1);
    return null;
  }

  const creationId = data1.id;
  console.log(`   ✅ Contenedor creado. ID: ${creationId}. Esperando 5s para publicar...`);
  await sleep(5000);

  // 2. Publicar contenedor
  const params2 = new URLSearchParams();
  params2.append('creation_id', creationId);
  params2.append('access_token', token);

  const res2 = await fetch(`https://graph.facebook.com/v19.0/${igUserId}/media_publish`, {
    method: 'POST',
    body: params2
  });

  const data2 = await res2.json();
  if (res2.ok && data2.id) {
    const mediaId = data2.id;
    console.log(`   🎉 ¡FOTO DE PERRITO PUBLICADA EN INSTAGRAM! Media ID: ${mediaId}`);

    // Obtener permalink
    const permRes = await fetch(`https://graph.facebook.com/v19.0/${mediaId}?fields=permalink&access_token=${token}`);
    const permData = await permRes.json();
    const permalink = permData.permalink || `https://www.instagram.com/p/${mediaId}/`;
    console.log(`   🔗 Enlace en vivo: ${permalink}`);

    historial.publicaciones.push({
      tipo: 'foto',
      post_id: candidato.id,
      titulo: candidato.titulo,
      media_id: mediaId,
      permalink: permalink,
      fecha: new Date().toISOString()
    });
    historial.ultimo_tipo = 'foto';
    guardarHistorial(historial);

    return { mediaId, permalink };
  } else {
    console.error('❌ Error al publicar foto:', data2);
    return null;
  }
}

/**
 * Publica un Reel en video vertical 9:16 en Instagram Reels
 */
async function publicarReelPerrito(token, igUserId) {
  console.log('\n🎬 [REEL PERRITO] Iniciando publicación de Reel en @huellasconproposito26...');

  if (!fs.existsSync(REELS_INDEX_PATH)) {
    console.error('❌ No se encontró reels_perritos_index.json. Ejecuta primero generador_reels_perritos.py');
    return null;
  }

  const reels = JSON.parse(fs.readFileSync(REELS_INDEX_PATH, 'utf-8'));
  const historial = cargarHistorial();
  const publicadosReels = new Set(historial.publicaciones.filter(p => p.tipo === 'reel').map(p => p.reel_id));

  let candidato = reels.find(r => !r.publicado_instagram && !publicadosReels.has(r.id));
  if (!candidato) {
    candidato = reels[0];
  }

  const videoUrl = `${GITHUB_PAGES_BASE}${candidato.archivo_video}`;
  const caption = candidato.caption || `🐾 Historia real de rescate. Síguenos en @huellasconproposito26 ❤️`;

  console.log(`   Reel: #${candidato.id} - ${candidato.nombre_perrito}`);
  console.log(`   Video URL: ${videoUrl}`);

  // 1. Crear contenedor de Reel
  const body1 = new URLSearchParams();
  body1.append('media_type', 'REELS');
  body1.append('video_url', videoUrl);
  body1.append('caption', caption);
  body1.append('share_to_feed', 'true');
  body1.append('access_token', token);

  const res1 = await fetch(`https://graph.facebook.com/v19.0/${igUserId}/media`, {
    method: 'POST',
    body: body1
  });

  const data1 = await res1.json();
  if (!res1.ok || !data1.id) {
    console.error('❌ Error creando contenedor de Reel:', data1);
    return null;
  }

  const creationId = data1.id;
  console.log(`   ✅ Contenedor de Reel creado. ID: ${creationId}`);

  // 2. Esperar procesamiento de Meta
  const listo = await esperarProcesamientoReel(creationId, token);
  if (!listo) {
    console.error('❌ Meta no pudo procesar el video a tiempo.');
    return null;
  }

  // 3. Publicar Reel
  const body2 = new URLSearchParams();
  body2.append('creation_id', creationId);
  body2.append('access_token', token);

  const res2 = await fetch(`https://graph.facebook.com/v19.0/${igUserId}/media_publish`, {
    method: 'POST',
    body: body2
  });

  const data2 = await res2.json();
  if (res2.ok && data2.id) {
    const mediaId = data2.id;
    console.log(`   🎉 ¡REEL DE PERRITO PUBLICADO EN INSTAGRAM! Media ID: ${mediaId}`);

    await sleep(2000);
    const permRes = await fetch(`https://graph.facebook.com/v19.0/${mediaId}?fields=permalink&access_token=${token}`);
    const permData = await permRes.json();
    const permalink = permData.permalink || `https://www.instagram.com/reel/${mediaId}/`;
    console.log(`   🔗 Enlace en vivo: ${permalink}`);

    candidato.publicado_instagram = true;
    candidato.ig_media_id = mediaId;
    candidato.permalink = permalink;
    fs.writeFileSync(REELS_INDEX_PATH, JSON.stringify(reels, null, 2), 'utf-8');

    historial.publicaciones.push({
      tipo: 'reel',
      reel_id: candidato.id,
      nombre_perrito: candidato.nombre_perrito,
      media_id: mediaId,
      permalink: permalink,
      fecha: new Date().toISOString()
    });
    historial.ultimo_tipo = 'reel';
    guardarHistorial(historial);

    return { mediaId, permalink };
  } else {
    console.error('❌ Error publicando Reel:', data2);
    return null;
  }
}

async function main() {
  const args = process.argv.slice(2);
  const modo = args[0] || '--auto';

  const { token, igUserId } = cargarCredenciales();
  if (!token || !igUserId) {
    console.error('❌ Falta token o ID de Instagram en config.json');
    process.exit(1);
  }

  console.log('='.repeat(65));
  console.log('🐶 PUBLICADOR EXCLUSIVO DE PERRITOS - @HUELLASCONPROPOSITO26');
  console.log('='.repeat(65));
  console.log(`🔹 Instagram ID: ${igUserId}`);
  console.log(`🔹 Modo: ${modo}`);

  const historial = cargarHistorial();

  if (modo === '--foto') {
    await publicarFotoPerrito(token, igUserId);
  } else if (modo === '--reel') {
    await publicarReelPerrito(token, igUserId);
  } else {
    // Modo automático: alternar entre foto y reel
    if (historial.ultimo_tipo === 'reel') {
      console.log('🔄 Turno automático: FOTO DE HISTORIA DE PERRITO');
      await publicarFotoPerrito(token, igUserId);
    } else {
      console.log('🔄 Turno automático: REEL VERTICAL DE HISTORIA DE PERRITO');
      await publicarReelPerrito(token, igUserId);
    }
  }

  console.log('\n🏁 Proceso de publicación completado.');
}

main().catch(err => {
  console.error('❌ Error general:', err);
  process.exit(1);
});
