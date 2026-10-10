/**
 * AUTO COMMUNITY MANAGER IA MULTI-PÁGINA
 * ---------------------------------------
 * Gestiona y responde comentarios de forma autónoma con IA personalizada para cada página:
 * 1. Huellas con Propósito -> Persona empática, amorosa con los perritos y sabiduría estoica.
 * 2. Metalidad de Acero    -> Mentor implacable de disciplina, superación y cero victimismo.
 * 
 * Reglas de funcionamiento:
 * - Detecta y filtra SPAM o insultos de inmediato ("IGNORAR").
 * - Saluda al usuario por su nombre.
 * - Respuestas de 1 a 3 frases dinámicas para el algoritmo de Facebook.
 * - Registra en historial_comentarios.json para evitar duplicados.
 * - Pausa de 2s entre respuestas para respetar límites de Meta.
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { analizarYResponderComentarioIA, analizarYResponderComentarioAceroIA } from './cerebro_ia.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const CONFIG_PATH = path.join(__dirname, 'config.json');
const HISTORIAL_PATH = path.join(__dirname, 'historial_comentarios.json');

const PAGINAS = [
  {
    clave: 'huellas_con_proposito',
    nombre: 'Huellas con Propósito',
    idEnvKey: 'PAGE_ID',
    tokenEnvKey: 'META_ACCESS_TOKEN',
    responderFn: analizarYResponderComentarioIA
  },
  {
    clave: 'mentalidad_de_acero',
    nombre: 'Metalidad de Acero',
    idEnvKey: 'PAGE_ID_ACERO',
    tokenEnvKey: 'META_ACCESS_TOKEN_ACERO',
    responderFn: analizarYResponderComentarioAceroIA
  }
];

function cargarCredenciales(pagCfg) {
  let token = process.env[pagCfg.tokenEnvKey];
  let pageId = process.env[pagCfg.idEnvKey];

  if ((!token || !pageId) && fs.existsSync(CONFIG_PATH)) {
    try {
      const cfg = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf-8'));
      if (cfg.PAGINAS && cfg.PAGINAS[pagCfg.clave]) {
        token = token || cfg.PAGINAS[pagCfg.clave].token;
        pageId = pageId || cfg.PAGINAS[pagCfg.clave].id;
      }
      if (pagCfg.clave === 'huellas_con_proposito') {
        token = token || cfg.ACCESS_TOKEN;
        pageId = pageId || cfg.PAGE_OR_PROFILE_ID;
      }
    } catch (e) {
      console.warn(`Aviso al leer config.json: ${e.message}`);
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

async function procesarComentariosPagina(pagCfg, historial) {
  console.log('\n' + '='.repeat(60));
  console.log(`🤖 COMMUNITY MANAGER IA: ${pagCfg.nombre.toUpperCase()}`);
  console.log('='.repeat(60));

  const { token, pageId } = cargarCredenciales(pagCfg);

  if (!token || !pageId) {
    console.warn(`⚠️ Credenciales no encontradas para ${pagCfg.nombre}. Omitiendo.`);
    return 0;
  }

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
      console.error(`❌ Error al consultar posts en ${pagCfg.nombre}:`, dataPosts);
      return 0;
    }
  } catch (err) {
    console.error(`❌ Error de red consultando posts de ${pagCfg.nombre}:`, err.message);
    return 0;
  }

  console.log(`📋 Analizando comentarios en ${posts.length} publicaciones recientes de ${pagCfg.nombre}...`);
  let respondidosPagina = 0;

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
            pagina: pagCfg.nombre,
            estado: 'ya_respondido_en_facebook',
            fecha: new Date().toISOString()
          };
          continue;
        }

        // Si no hay texto (solo sticker sin mensaje), omitir
        if (!mensaje) continue;

        console.log(`\n💬 [${pagCfg.nombre}] Nuevo comentario de ${autorNombre}: "${mensaje}"`);

        // 3. Analizar y redactar con el cerebro IA especializado de esta página
        let respuestaIA = '';
        try {
          respuestaIA = await pagCfg.responderFn(autorNombre, mensaje, post.message || '');
        } catch (e) {
          console.error(`⚠️ Error al generar respuesta con Gemini:`, e.message);
          continue;
        }

        if (!respuestaIA || respuestaIA.toUpperCase().includes('IGNORAR')) {
          console.log(`🛑 Cerebro IA clasificó como SPAM / IGNORAR.`);
          historial[commentId] = {
            pagina: pagCfg.nombre,
            estado: 'ignorado',
            usuario: autorNombre,
            comentario: mensaje,
            fecha: new Date().toISOString()
          };
          guardarHistorial(historial);
          continue;
        }

        // 4. Publicar la respuesta en Facebook
        console.log(`🤖 Respuesta IA redactada: "${respuestaIA}"`);
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
              pagina: pagCfg.nombre,
              estado: 'respondido',
              reply_id: dataPub.id,
              usuario: autorNombre,
              comentario: mensaje,
              respuesta: respuestaIA,
              fecha: new Date().toISOString()
            };
            guardarHistorial(historial);
            respondidosPagina++;
            await sleep(2500); // 2.5s entre respuestas para respetar rate limit
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

  console.log(`🏁 Respuestas completadas para ${pagCfg.nombre}: ${respondidosPagina}`);
  return respondidosPagina;
}

async function main() {
  console.log('='.repeat(65));
  console.log('🚀 INICIANDO COMMUNITY MANAGER IA MULTI-PÁGINA');
  console.log('='.repeat(65));

  const historial = cargarHistorial();
  let totalRespondidos = 0;

  for (const pag of PAGINAS) {
    const r = await procesarComentariosPagina(pag, historial);
    totalRespondidos += r;
  }

  guardarHistorial(historial);
  console.log('\n' + '='.repeat(65));
  console.log(`🎉 FIN DEL PROCESO: Total comentarios respondidos en todas las páginas: ${totalRespondidos}`);
  console.log('='.repeat(65));
}

main().catch(err => {
  console.error('Error fatal en Community Manager:', err);
  process.exit(1);
});
