/**
 * PUBLICADOR AUTOMÁTICO DE FACEBOOK EN NODE.JS
 * --------------------------------------------
 * Diseñado para ejecutarse automáticamente en GitHub Actions (100% Gratis) o de forma local.
 * Utiliza fetch y FormData nativos de Node.js (Node 18+).
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const CONFIG_PATH = path.join(__dirname, 'config.json');
const DATA_PATH = path.join(__dirname, 'noviembre', 'publicaciones.json');

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

function aUnixTimestamp(fechaStr, horaStr) {
  const dt = new Date(`${fechaStr}T${horaStr}:00`);
  return Math.floor(dt.getTime() / 1000);
}

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function main() {
  console.log('='.repeat(65));
  console.log('🚀 PUBLICADOR NODE.JS EN GITHUB ACTIONS - HUELLAS CON PROPÓSITO');
  console.log('='.repeat(65));

  const { token, pageId } = cargarCredenciales();

  if (!token || !pageId) {
    console.error('❌ Error: Falta META_ACCESS_TOKEN o PAGE_ID en las variables de entorno / config.json');
    process.exit(1);
  }

  if (!fs.existsSync(DATA_PATH)) {
    console.error(`❌ Error: No se encontró el archivo de datos: ${DATA_PATH}`);
    process.exit(1);
  }

  const posts = JSON.parse(fs.readFileSync(DATA_PATH, 'utf-8'));
  const nowTs = Math.floor(Date.now() / 1000);
  // Límite estricto de Meta: máximo 28 a 29 días en el futuro (2,505,600 segundos)
  const maxSchedTs = nowTs + (29 * 86400);

  console.log(`Página destino ID: ${pageId}`);
  console.log(`Fecha actual del servidor: ${new Date().toLocaleString()}`);
  console.log(`Límite máximo de programación Meta (29 días): ${new Date(maxSchedTs * 1000).toLocaleString()}`);

  const programados = posts.filter(p => p.estado === 'programado');
  const pendientes = posts.filter(p => p.estado === 'pendiente');

  console.log(`📊 Publicaciones ya programadas: ${programados.length}`);
  console.log(`⏳ Publicaciones pendientes de programar: ${pendientes.length}\n`);

  let exitos = 0;
  let fueraDeVentana = 0;

  for (let i = 0; i < pendientes.length; i++) {
    const p = pendientes[i];
    const ts = aUnixTimestamp(p.fecha, p.hora);

    // Si supera los 29 días, ignorar en esta ejecución
    if (ts > maxSchedTs) {
      fueraDeVentana++;
      continue;
    }

    const icono = p.tipo === 'perrito' ? '🐶 PERRITO' : '🏛️ ESTOICO';
    const tituloCorto = p.titulo.replace(/[«»]/g, '').substring(0, 30);
    process.stdout.write(`[Programando] ${icono} #${String(p.id).padStart(3, '0')} | ${p.fecha} ${p.hora} | ${tituloCorto}... `);

    const relImg = p.ruta_imagen || `noviembre/${p.tipo === 'perrito' ? 'perritos' : 'filosofia'}/${p.archivo_imagen}`;
    const imgFullPath = path.join(__dirname, relImg);

    const caption = `${p.texto}\n\n${p.hashtags}`;
    const url = `https://graph.facebook.com/v19.0/${pageId}/photos`;

    const formData = new FormData();
    formData.append('caption', caption);
    formData.append('published', 'false');
    formData.append('scheduled_publish_time', String(ts));
    formData.append('access_token', token);

    try {
      if (fs.existsSync(imgFullPath)) {
        const fileBuffer = fs.readFileSync(imgFullPath);
        const blob = new Blob([fileBuffer], { type: 'image/jpeg' });
        formData.append('source', blob, path.basename(imgFullPath));
      }

      const res = await fetch(url, {
        method: 'POST',
        body: formData,
      });

      const data = await res.json();

      if (res.ok && (data.id || data.post_id)) {
        const postId = data.id || data.post_id;
        p.estado = 'programado';
        p.meta_post_id = postId;
        exitos++;

        // Guardar progreso inmediatamente en el JSON
        fs.writeFileSync(DATA_PATH, JSON.stringify(posts, null, 2), 'utf-8');
        console.log(`✅ OK (ID: ${postId})`);
      } else {
        const errMsg = data.error?.message || JSON.stringify(data);
        console.log(`❌ Error: ${errMsg}`);

        if (errMsg.toLowerCase().includes('expire') || errMsg.toLowerCase().includes('session')) {
          console.error('⚠️ El Access Token ha expirado. Renuévalo en GitHub Secrets.');
          break;
        }
      }
    } catch (err) {
      console.log(`❌ Excepción de red: ${err.message}`);
    }

    await sleep(2000); // Pausa amigable de 2s para evitar bloqueos
  }

  console.log('\n' + '='.repeat(60));
  console.log(`🎉 RESUMEN DE EJECUCIÓN NODE.JS:`);
  console.log(`   ✅ Nuevas publicaciones programadas en esta ejecución: ${exitos}`);
  console.log(`   📊 Total programadas acumuladas: ${programados.length + exitos}/${posts.length}`);
  if (fueraDeVentana > 0) {
    console.log(`   ⏳ En espera (${fueraDeVentana} posts): Superan los 29 días de anticipación de Meta.`);
    console.log(`      GitHub Actions las programará automáticamente en su próxima ejecución diaria.`);
  }
  console.log('='.repeat(60));
}

main().catch(err => {
  console.error('Error fatal:', err);
  process.exit(1);
});
