/**
 * AUTO COMMUNITY MANAGER IA - HUELLAS CON PROPÓSITO
 * --------------------------------------------------
 * 1. Lee comentarios nuevos en las publicaciones de Facebook.
 * 2. Analiza el sentimiento e intención con Google Gemini.
 * 3. Si es spam o insultos, lo ignora automáticamente.
 * 4. Si es una persona real, responde con calidez humana, empatía y su nombre.
 * 5. Registra el historial para no repetir respuestas.
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { analizarYResponderComentarioIA } from './cerebro_ia.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const CONFIG_PATH = path.join(__dirname, 'config.json');
const HISTORIAL_PATH = path.join(__dirname, 'historial_comentarios.json');

function cargarCredenciales() {
  let token = process.env.META_ACCESS_TOKEN;
  let pageId = process.env.PAGE_ID;

  if (!token || !pageId) {
    if (fs.existsSync(CONFIG_PATH)) {
      const cfg = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf-8'));
      token = token || cfg.ACCESS_TOKEN;
      pageId = pageId || cfg.PAGE_OR_PROFILE_ID;
    }
  }

  return { token, pageId };
}

function cargarHistorial() {
  if (fs.existsSync(HISTORIAL_PATH)) {
    try {
      return JSON.parse(fs.readFileSync(HISTORIAL_PATH, 'utf-8'));
    } catch (e) {
      return {};
    }
  }
  return {};
}

function guardarHistorial(historial) {
  fs.writeFileSync(HISTORIAL_PATH, JSON.stringify(historial, null, 2), 'utf-8');
}

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function responderComentarios() {
  const { token, pageId } = cargarCredenciales();

  if (!token || !pageId) {
    console.error('❌ Falta META_ACCESS_TOKEN o PAGE_ID');
    return;
  }

  const historial = cargarHistorial();
  console.log(`🤖 Iniciando Community Manager IA para la página ID: ${pageId}...`);

  // 1. Obtener los últimos 10 posts publicados
  let posts = [];
  try {
    const resPosts = await fetch(
      `https://graph.facebook.com/v19.0/${pageId}/published_posts?fields=id,message&limit=10&access_token=${token}`
    );
    const dataPosts = await resPosts.json();
    if (resPosts.ok && dataPosts.data) {
      posts = dataPosts.data;
    } else {
      console.error('❌ Error al consultar posts:', dataPosts);
      return;
    }
  } catch (err) {
    console.error('❌ Error de red consultando posts:', err.message);
    return;
  }

  console.log(`📋 Analizando comentarios en ${posts.length} publicaciones recientes...`);
  let totalRespondidos = 0;

  for (const post of posts) {
    try {
      // 2. Obtener comentarios de cada publicación
      const resComments = await fetch(
        `https://graph.facebook.com/v19.0/${post.id}/comments?fields=id,from,message,created_time,comments{from}&limit=50&access_token=${token}`
      );
      const dataComments = await resComments.json();

      if (!resComments.ok || !dataComments.data) continue;

      for (const com of dataComments.data) {
        const commentId = com.id;
        const autorId = com.from?.id;
        const autorNombre = com.from?.name || 'Amigo';
        const mensaje = (com.message || '').trim();

        // Regla A: No responderse a sí mismo (la propia página)
        if (autorId === pageId) continue;

        // Regla B: Si ya está en nuestro historial local, omitir
        if (historial[commentId]) continue;

        // Regla C: Si ya tiene una respuesta previa de la página en Facebook
        const replies = com.comments?.data || [];
        const yaRespondidoPorPagina = replies.some((r) => r.from?.id === pageId);
        if (yaRespondidoPorPagina) {
          historial[commentId] = {
            estado: 'ya_respondido_en_facebook',
            fecha: new Date().toISOString()
          };
          continue;
        }

        // Si no hay texto (solo sticker sin mensaje), omitir o saludar breve
        if (!mensaje) continue;

        console.log(`\n💬 Comentario nuevo de ${autorNombre}: "${mensaje}"`);

        // 3. Analizar y redactar con Gemini
        let respuestaIA = '';
        try {
          respuestaIA = await analizarYResponderComentarioIA(autorNombre, mensaje, post.message || '');
        } catch (e) {
          console.error(`⚠️ Error al generar respuesta con Gemini:`, e.message);
          continue;
        }

        if (!respuestaIA || respuestaIA.toUpperCase().includes('IGNORAR')) {
          console.log(`🛑 Cerebro IA clasificó como SPAM / IGNORAR.`);
          historial[commentId] = {
            estado: 'ignorado',
            usuario: autorNombre,
            comentario: mensaje,
            fecha: new Date().toISOString()
          };
          guardarHistorial(historial);
          continue;
        }

        // 4. Publicar la respuesta en Facebook
        console.log(`🤖 Respuesta redactada: "${respuestaIA}"`);
        try {
          const bodyData = new URLSearchParams();
          bodyData.append('message', respuestaIA);
          bodyData.append('access_token', token);

          const resPublicar = await fetch(`https://graph.facebook.com/v19.0/${commentId}/comments`, {
            method: 'POST',
            body: bodyData
          });

          const dataPub = await resPublicar.json();
          if (resPublicar.ok && dataPub.id) {
            console.log(`✅ ¡Respuesta publicada en Facebook! ID: ${dataPub.id}`);
            historial[commentId] = {
              estado: 'respondido',
              reply_id: dataPub.id,
              usuario: autorNombre,
              comentario: mensaje,
              respuesta: respuestaIA,
              fecha: new Date().toISOString()
            };
            guardarHistorial(historial);
            totalRespondidos++;
            await sleep(2000); // 2 segundos de pausa entre respuestas para no saturar la API
          } else {
            console.error(`❌ Error de Meta al publicar respuesta:`, dataPub);
          }
        } catch (e) {
          console.error(`❌ Error al enviar respuesta a Meta:`, e.message);
        }
      }
    } catch (e) {
      console.log(`Aviso revisando post ${post.id}:`, e.message);
    }
  }

  guardarHistorial(historial);
  console.log(`\n🏁 Proceso completado. Comentarios respondidos en esta ejecución: ${totalRespondidos}`);
}

responderComentarios();
