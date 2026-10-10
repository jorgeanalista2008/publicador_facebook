/**
 * PROGRAMADOR AUTOMÁTICO DE METALIDAD DE ACERO
 * --------------------------------------------
 * Sube y programa las publicaciones con imagen en Meta Graph API.
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const CONFIG_PATH = path.join(__dirname, 'config.json');
const JSON_PATH = path.join(__dirname, 'mentalidad_de_acero', 'publicaciones.json');

function cargarConfig() {
  let token = process.env.META_ACCESS_TOKEN_ACERO;
  let pageId = process.env.PAGE_ID_ACERO;

  if (!token || !pageId) {
    if (fs.existsSync(CONFIG_PATH)) {
      const cfg = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf-8'));
      if (cfg.PAGINAS && cfg.PAGINAS.mentalidad_de_acero) {
        token = token || cfg.PAGINAS.mentalidad_de_acero.token;
        pageId = pageId || cfg.PAGINAS.mentalidad_de_acero.id;
      }
    }
  }

  return { token, pageId };
}

const sleep = ms => new Promise(r => setTimeout(r, ms));

async function programar() {
  const { token, pageId } = cargarConfig();

  if (!token || !pageId) {
    console.error('❌ Falta token o pageId de Metalidad de Acero');
    return;
  }

  if (!fs.existsSync(JSON_PATH)) {
    console.error('❌ No se encontró publicaciones.json');
    return;
  }

  const posts = JSON.parse(fs.readFileSync(JSON_PATH, 'utf-8'));
  console.log(`🚀 Programando publicaciones para Metalidad de Acero (Page ID: ${pageId})...`);

  const nowSec = Math.floor(Date.now() / 1000);
  const maxSec = nowSec + 28 * 86400; // Máximo 28 días
  let exitosos = 0;

  for (const post of posts) {
    if (post.estado !== 'pendiente') {
      continue;
    }

    // Calcular timestamp en zona horaria local (-04:00)
    const fechaHoraStr = `${post.fecha}T${post.hora}:00-04:00`;
    const targetDate = new Date(fechaHoraStr);
    const targetSec = Math.floor(targetDate.getTime() / 1000);

    if (targetSec <= nowSec + 600) {
      console.log(`⚠️ Post #${post.id} (${post.fecha} ${post.hora}) es muy cercano al presente o pasado. Omitiendo programación.`);
      continue;
    }

    if (targetSec > maxSec) {
      console.log(`⏳ Post #${post.id} (${post.fecha}) supera el límite de 28 días de Meta. Se programará dinámicamente.`);
      continue;
    }

    const imgPath = path.resolve(__dirname, post.imagen);
    if (!fs.existsSync(imgPath)) {
      console.error(`❌ Imagen no encontrada para post #${post.id}: ${imgPath}`);
      continue;
    }

    console.log(`\n📤 Programando Post #${post.id} para el ${post.fecha} a las ${post.hora} (${post.arquetipo})...`);

    try {
      const fileBuffer = fs.readFileSync(imgPath);
      const blob = new Blob([fileBuffer], { type: 'image/jpeg' });

      const formData = new FormData();
      formData.append('message', post.texto);
      formData.append('source', blob, path.basename(imgPath));
      formData.append('access_token', token);
      formData.append('published', 'false');
      formData.append('scheduled_publish_time', targetSec.toString());

      const res = await fetch(`https://graph.facebook.com/v19.0/${pageId}/photos`, {
        method: 'POST',
        body: formData
      });

      const data = await res.json();
      if (res.ok && (data.id || data.post_id)) {
        const finalId = data.post_id || data.id;
        console.log(`✅ ¡Post #${post.id} programado con éxito! ID: ${finalId}`);
        post.estado = 'programado';
        post.post_id = finalId;
        post.fecha_programada_unix = targetSec;
        exitosos++;
        // Guardamos tras cada éxito
        fs.writeFileSync(JSON_PATH, JSON.stringify(posts, null, 2), 'utf-8');
        await sleep(2500); // 2.5 seg entre uploads
      } else {
        console.error(`❌ Error de Meta al programar post #${post.id}:`, data);
      }
    } catch (e) {
      console.error(`❌ Error en post #${post.id}:`, e.message);
    }
  }

  fs.writeFileSync(JSON_PATH, JSON.stringify(posts, null, 2), 'utf-8');
  console.log(`\n🏁 Finalizado. Total publicaciones programadas exitosamente: ${exitosos}`);
}

programar();
