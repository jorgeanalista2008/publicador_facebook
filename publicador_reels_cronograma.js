/**
 * PUBLICADOR AUTOMÁTICO DE REELS PARA INSTAGRAM (@huellasconproposito26)
 * BASADO EN EL CRONOGRAMA DE 70 REELS (14 DÍAS - 5 DIARIOS)
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const CONFIG_PATH = path.join(__dirname, 'config.json');
const CRONOGRAMA_PATH = path.join(__dirname, 'cronograma_70_reels.json');
const HISTORIAL_PATH = path.join(__dirname, 'instagram_perritos_historial.json');

const GITHUB_PAGES_BASE = 'https://jorgeanalista2008.github.io/publicador_facebook/';
const GITHUB_RAW_BASE = 'https://raw.githubusercontent.com/jorgeanalista2008/publicador_facebook/main/';

const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

function cargarCredenciales() {
  let cfg = {};
  if (fs.existsSync(CONFIG_PATH)) {
    try {
      cfg = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf-8'));
    } catch (e) {}
  }

  const token = process.env.META_ACCESS_TOKEN || cfg.PAGINAS?.huellas_con_proposito?.token || cfg.ACCESS_TOKEN;
  let igUserId = process.env.IG_USER_ID || cfg.PAGINAS?.huellas_con_proposito?.instagram?.id || '17841426835073929';

  return { token, igUserId };
}

async function esperarProcesamientoReel(creationId, token, maxIntentos = 30) {
  for (let i = 1; i <= maxIntentos; i++) {
    process.stdout.write(`   ⏳ Verificando procesamiento Meta (intento ${i}/${maxIntentos})... `);
    try {
      const res = await fetch(`https://graph.facebook.com/v19.0/${creationId}?fields=status_code,status&access_token=${token}`);
      const data = await res.json();
      const code = data.status_code;

      if (code === 'FINISHED') {
        console.log('✅ ¡PROCESADO CON ÉXITO!');
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
      console.log('error red, reintentando...');
      await sleep(5000);
    }
  }
  return false;
}

async function publicarReel(candidato, token, igUserId) {
  console.log('='.repeat(65));
  console.log(`🚀 PUBLICANDO REEL #${candidato.id} (${candidato.slot_horario}) - ${candidato.nombre_perrito}`);
  console.log(`   Título: ${candidato.titulo}`);
  console.log('='.repeat(65));

  // Priorizar URL en GitHub Pages (o Raw)
  const videoUrl = encodeURI(`${GITHUB_PAGES_BASE}${candidato.archivo_video}`);
  console.log(`   Video URL: ${videoUrl}`);

  // 1. Crear contenedor de Reel
  const body1 = new URLSearchParams();
  body1.append('media_type', 'REELS');
  body1.append('video_url', videoUrl);
  body1.append('caption', candidato.caption);
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
  console.log(`   ✅ Contenedor creado. ID: ${creationId}`);

  // 2. Esperar procesamiento
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
    console.log(`\n🎉 ¡REEL PUBLICADO CON ÉXITO EN INSTAGRAM! Media ID: ${mediaId}`);

    await sleep(3000);
    const permRes = await fetch(`https://graph.facebook.com/v19.0/${mediaId}?fields=permalink&access_token=${token}`);
    const permData = await permRes.json();
    const permalink = permData.permalink || `https://www.instagram.com/reel/${mediaId}/`;

    console.log(`🔗 Enlace en vivo: ${permalink}\n`);

    return { mediaId, permalink };
  } else {
    console.error('❌ Error al publicar Reel:', data2);
    return null;
  }
}

async function main() {
  const args = process.argv.slice(2);
  const modo = args[0] || '--auto';

  if (!fs.existsSync(CRONOGRAMA_PATH)) {
    console.error('❌ No se encontró cronograma_70_reels.json');
    process.exit(1);
  }

  const cronograma = JSON.parse(fs.readFileSync(CRONOGRAMA_PATH, 'utf-8'));

  if (modo === '--listar') {
    console.log('\n📊 ESTADO DEL CRONOGRAMA DE 70 REELS:');
    cronograma.slice(0, 15).forEach(r => {
      console.log(`[${r.estado.toUpperCase()}] Reel #${r.id} | ${r.slot_horario} | ${r.nombre_perrito} - ${r.titulo.substring(0, 30)}...`);
    });
    const publicados = cronograma.filter(r => r.estado === 'publicado').length;
    const renderizados = cronograma.filter(r => r.estado === 'renderizado').length;
    const programados = cronograma.filter(r => r.estado === 'programado').length;
    console.log(`\nResumen: ${publicados} Publicados | ${renderizados} Renderizados Listos | ${programados} Pendientes`);
    return;
  }

  const { token, igUserId } = cargarCredenciales();
  if (!token || !igUserId) {
    console.error('❌ Falta token o Instagram ID');
    process.exit(1);
  }

  let candidato = null;

  if (modo === '--id' && args[1]) {
    const idBuscado = parseInt(args[1], 10);
    candidato = cronograma.find(r => r.id === idBuscado);
  } else {
    // Modo automático: buscar el primer Reel que esté "renderizado" y no publicado
    candidato = cronograma.find(r => r.estado === 'renderizado' && !r.permalink);
    
    // Si no hay con etiqueta "renderizado", buscar si el archivo_video ya existe físicamente
    if (!candidato) {
      candidato = cronograma.find(r => {
        if (r.estado === 'publicado') return false;
        return r.archivo_video && fs.existsSync(path.join(__dirname, r.archivo_video));
      });
    }
  }

  if (!candidato) {
    console.log('ℹ️ No hay Reels listos pendientes de publicación en este momento.');
    return;
  }

  const resultado = await publicarReel(candidato, token, igUserId);
  if (resultado) {
    candidato.estado = 'publicado';
    candidato.permalink = resultado.permalink;
    candidato.ig_media_id = resultado.mediaId;
    candidato.fecha_publicacion = new Date().toISOString();

    fs.writeFileSync(CRONOGRAMA_PATH, JSON.stringify(cronograma, null, 2), 'utf-8');

    // Registrar en historial general
    let historial = { publicaciones: [], ultimo_tipo: 'reel' };
    if (fs.existsSync(HISTORIAL_PATH)) {
      try {
        historial = JSON.parse(fs.readFileSync(HISTORIAL_PATH, 'utf-8'));
      } catch (e) {}
    }
    historial.publicaciones.push({
      tipo: 'reel_cinematico_cronograma',
      reel_id: candidato.id,
      nombre_perrito: candidato.nombre_perrito,
      slot_horario: candidato.slot_horario,
      media_id: resultado.mediaId,
      permalink: resultado.permalink,
      fecha: new Date().toISOString()
    });
    historial.ultimo_tipo = 'reel';
    fs.writeFileSync(HISTORIAL_PATH, JSON.stringify(historial, null, 2), 'utf-8');

    console.log(`✅ Cronograma e historial actualizados para Reel #${candidato.id}.`);
  }
}

main().catch(console.error);
