/**
 * PUBLICADOR AUTOMÁTICO DE REELS (INSTAGRAM & FACEBOOK)
 * -----------------------------------------------------
 * Publica videos verticales 9:16 en Instagram Reels y Facebook Reels
 * utilizando la Meta Graph API v19.0 y URLs públicas de GitHub Pages.
 * 
 * Uso:
 *   node publicador_reels.js --test           (Publica el primer Reel de prueba)
 *   node publicador_reels.js --all            (Procesa la cola de Reels pendientes)
 *   node publicador_reels.js --id 2           (Publica un Reel específico por su ID)
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const CONFIG_PATH = path.join(__dirname, 'config.json');
const INDEX_PATH = path.join(__dirname, 'videos_reels', 'videos_index.json');

const GITHUB_PAGES_BASE = 'https://jorgeanalista2008.github.io/publicador_facebook/';

function cargarCredenciales() {
  let cfg = {};
  if (fs.existsSync(CONFIG_PATH)) {
    cfg = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf-8'));
  }

  const tokenHuellas = process.env.META_ACCESS_TOKEN || cfg.PAGINAS?.huellas_con_proposito?.token || cfg.ACCESS_TOKEN;
  const pageIdHuellas = process.env.PAGE_ID || cfg.PAGINAS?.huellas_con_proposito?.id || cfg.PAGE_OR_PROFILE_ID;
  const igUserIdHuellas = process.env.IG_USER_ID || cfg.PAGINAS?.huellas_con_proposito?.instagram?.id;

  const tokenAcero = process.env.META_ACCESS_TOKEN_ACERO || cfg.PAGINAS?.mentalidad_de_acero?.token;
  const pageIdAcero = process.env.PAGE_ID_ACERO || cfg.PAGINAS?.mentalidad_de_acero?.id;

  return {
    huellas: { token: tokenHuellas, pageId: pageIdHuellas, igUserId: igUserIdHuellas },
    acero: { token: tokenAcero, pageId: pageIdAcero }
  };
}

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

/**
 * Espera a que Meta termine de procesar el contenedor de video en Instagram
 */
async function esperarProcesamientoInstagram(creationId, token, maxIntentos = 20) {
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
 * Publica un Reel en Instagram
 */
async function publicarReelInstagram(igUserId, token, videoUrl, caption) {
  console.log(`\n📸 [Instagram Reels] Iniciando publicación para @huellasconproposito26...`);
  console.log(`   URL Video: ${videoUrl}`);

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
    console.error('❌ Error creando contenedor de Reel en Instagram:', data1);
    return null;
  }

  const creationId = data1.id;
  console.log(`✅ Contenedor de Reel creado con éxito. ID: ${creationId}`);

  // 2. Esperar procesamiento del video
  const listo = await esperarProcesamientoInstagram(creationId, token);
  if (!listo) {
    console.error('❌ El video no terminó de procesarse a tiempo en Meta.');
    return null;
  }

  // 3. Publicar el Reel
  console.log(`🚀 Publicando Reel en el feed de Instagram...`);
  const body2 = new URLSearchParams();
  body2.append('creation_id', creationId);
  body2.append('access_token', token);

  const res2 = await fetch(`https://graph.facebook.com/v19.0/${igUserId}/media_publish`, {
    method: 'POST',
    body: body2
  });

  const data2 = await res2.json();
  if (res2.ok && data2.id) {
    const reelId = data2.id;
    console.log(`🎉 ¡REEL DE INSTAGRAM PUBLICADO CON ÉXITO! ID: ${reelId}`);

    // Obtener permalink
    try {
      const pRes = await fetch(`https://graph.facebook.com/v19.0/${reelId}?fields=permalink&access_token=${token}`);
      const pData = await pRes.json();
      if (pData.permalink) {
        console.log(`🔗 Enlace directo en Instagram: ${pData.permalink}`);
        return { id: reelId, permalink: pData.permalink };
      }
    } catch (e) {}

    return { id: reelId, permalink: `https://www.instagram.com/` };
  } else {
    console.error('❌ Error publicando contenedor en Instagram:', data2);
    return null;
  }
}

/**
 * Publica un Reel / Video Vertical en Facebook
 */
async function publicarReelFacebook(pageId, token, videoUrl, titulo, descripcion) {
  console.log(`\n🔵 [Facebook Reels] Publicando video en Página ID ${pageId}...`);

  const body = new URLSearchParams();
  body.append('file_url', videoUrl);
  body.append('title', titulo);
  body.append('description', descripcion);
  body.append('access_token', token);

  const res = await fetch(`https://graph.facebook.com/v19.0/${pageId}/videos`, {
    method: 'POST',
    body: body
  });

  const data = await res.json();
  if (res.ok && data.id) {
    console.log(`🎉 ¡VIDEO/REEL DE FACEBOOK PUBLICADO CON ÉXITO! ID: ${data.id}`);
    return { id: data.id, url: `https://www.facebook.com/${data.id}` };
  } else {
    console.error('❌ Error publicando en Facebook:', data);
    return null;
  }
}

async function procesarReel(item, creds) {
  console.log('\n' + '='.repeat(65));
  console.log(`🎬 PROCESANDO REEL #${item.id}: ${item.arquetipo || 'Video'}`);
  console.log('='.repeat(65));

  const relVideo = item.archivo_video.replace(/\\/g, '/');
  const videoPublicUrl = `${GITHUB_PAGES_BASE}${relVideo}`;

  const caption = `${item.guion}\n\n#MentalidadDeAcero #Disciplina #ReelsViral #Superacion #Exito #SinExcusas #Motivacion`;

  let resultado = { id: item.id };

  // 1. Publicar en Instagram si está disponible
  if (creds.huellas.igUserId && creds.huellas.token) {
    const igRes = await publicarReelInstagram(creds.huellas.igUserId, creds.huellas.token, videoPublicUrl, caption);
    if (igRes) {
      item.publicado_instagram = true;
      item.ig_reel_id = igRes.id;
      item.ig_permalink = igRes.permalink;
      item.fecha_publicacion_ig = new Date().toISOString();
      resultado.instagram = igRes;
    }
  }

  // 2. Publicar en Facebook (Huellas con Propósito)
  const targetPageId = creds.huellas.pageId;
  const targetToken = creds.huellas.token;

  if (targetPageId && targetToken) {
    const fbRes = await publicarReelFacebook(
      targetPageId,
      targetToken,
      videoPublicUrl,
      `• MENTALIDAD DE ACERO: ${item.arquetipo} •`,
      caption
    );
    if (fbRes) {
      item.publicado_facebook = true;
      item.fb_video_id = fbRes.id;
      item.fb_url = fbRes.url;
      item.fecha_publicacion_fb = new Date().toISOString();
      resultado.facebook = fbRes;
    }
  }

  return resultado;
}

async function main() {
  console.log('='.repeat(65));
  console.log('🚀 PUBLICADOR AUTOMÁTICO DE REELS - META GRAPH API v19.0');
  console.log('='.repeat(65));

  if (!fs.existsSync(INDEX_PATH)) {
    console.error(`❌ No existe el archivo de índice de videos: ${INDEX_PATH}`);
    process.exit(1);
  }

  const videos = JSON.parse(fs.readFileSync(INDEX_PATH, 'utf-8'));
  const creds = cargarCredenciales();

  const args = process.argv.slice(2);

  if (args.includes('--test')) {
    console.log('🧪 MODO DE PRUEBA: Publicando el primer Reel de la lista (Post #1)...');
    const item1 = videos.find(v => v.id === 1) || videos[0];
    await procesarReel(item1, creds);
    fs.writeFileSync(INDEX_PATH, JSON.stringify(videos, null, 2), 'utf-8');
  } else if (args.includes('--id')) {
    const idIdx = args.indexOf('--id') + 1;
    const targetId = parseInt(args[idIdx]);
    const item = videos.find(v => v.id === targetId);
    if (item) {
      await procesarReel(item, creds);
      fs.writeFileSync(INDEX_PATH, JSON.stringify(videos, null, 2), 'utf-8');
    } else {
      console.error(`❌ No se encontró el video con ID ${targetId}`);
    }
  } else {
    console.log(`📋 Total de videos disponibles en el catálogo: ${videos.length}`);
    console.log(`   Para publicar el primer Reel de prueba ejecuta:`);
    console.log(`   👉 node publicador_reels.js --test\n`);
    console.log(`   Para publicar un ID específico:`);
    console.log(`   👉 node publicador_reels.js --id 2`);
  }
}

main().catch(err => {
  console.error('❌ Error fatal en publicador de Reels:', err);
  process.exit(1);
});
