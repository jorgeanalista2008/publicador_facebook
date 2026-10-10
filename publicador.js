/**
 * PUBLICADOR AUTOMÁTICO MULTI-PÁGINA DE FACEBOOK EN NODE.JS
 * -----------------------------------------------------------
 * Diseñado para ejecutarse automáticamente en GitHub Actions o de forma local.
 * Gestiona múltiples páginas de forma centralizada y unificada:
 * 1. Huellas con Propósito (Rescate animal y filosofía)
 * 2. Metalidad de Acero (Disciplina, superación y mentalidad)
 * 
 * Cumple estrictamente las limitaciones de Meta Graph API:
 * - Ventana de programación: Entre 10 minutos y 28 días en el futuro.
 * - Los posts más allá de 28 días se conservan en estado 'pendiente' y se
 *   programan automáticamente a medida que GitHub Actions se ejecuta diariamente.
 * - Pausas de 2.5s entre publicaciones para respetar los límites de tasa (rate limits).
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const CONFIG_PATH = path.join(__dirname, 'config.json');

const PAGINAS = [
  {
    clave: 'huellas_con_proposito',
    nombre: 'Huellas con Propósito',
    idEnvKey: 'PAGE_ID',
    tokenEnvKey: 'META_ACCESS_TOKEN',
    dataPath: path.join(__dirname, 'noviembre', 'publicaciones.json'),
    resolverRutaImagen: (p) => {
      const rel = p.ruta_imagen || `noviembre/${p.tipo === 'perrito' ? 'perritos' : 'filosofia'}/${p.archivo_imagen}`;
      return path.join(__dirname, rel);
    },
    formatearTexto: (p) => `${p.texto}\n\n${p.hashtags || ''}`.trim()
  },
  {
    clave: 'mentalidad_de_acero',
    nombre: 'Metalidad de Acero',
    idEnvKey: 'PAGE_ID_ACERO',
    tokenEnvKey: 'META_ACCESS_TOKEN_ACERO',
    dataPath: path.join(__dirname, 'mentalidad_de_acero', 'publicaciones.json'),
    resolverRutaImagen: (p) => path.join(__dirname, p.imagen),
    formatearTexto: (p) => p.texto.trim()
  }
];

function cargarCredenciales(paginaCfg) {
  let token = process.env[paginaCfg.tokenEnvKey];
  let pageId = process.env[paginaCfg.idEnvKey];

  if ((!token || !pageId) && fs.existsSync(CONFIG_PATH)) {
    try {
      const cfg = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf-8'));
      if (cfg.PAGINAS && cfg.PAGINAS[paginaCfg.clave]) {
        token = token || cfg.PAGINAS[paginaCfg.clave].token;
        pageId = pageId || cfg.PAGINAS[paginaCfg.clave].id;
      }
      // Fallback para Huellas que también estaba en la raíz de config.json
      if (paginaCfg.clave === 'huellas_con_proposito') {
        token = token || cfg.ACCESS_TOKEN;
        pageId = pageId || cfg.PAGE_OR_PROFILE_ID;
      }
    } catch (e) {
      console.warn(`Aviso al leer config.json: ${e.message}`);
    }
  }

  return { token, pageId };
}

function aUnixTimestamp(fechaStr, horaStr) {
  // Manejo de zona horaria: si no tiene offset, asumir hora local/servidor
  const dt = new Date(`${fechaStr}T${horaStr}:00`);
  return Math.floor(dt.getTime() / 1000);
}

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function procesarPagina(paginaCfg) {
  console.log('\n' + '='.repeat(65));
  console.log(`📌 PROCESANDO PÁGINA: ${paginaCfg.nombre.toUpperCase()}`);
  console.log('='.repeat(65));

  const { token, pageId } = cargarCredenciales(paginaCfg);

  if (!token || !pageId) {
    console.warn(`⚠️ Credenciales no encontradas para ${paginaCfg.nombre} (${paginaCfg.idEnvKey} / ${paginaCfg.tokenEnvKey}). Omitiendo.`);
    return { exitos: 0, pendientesRestantes: 0, fueraDeVentana: 0 };
  }

  if (!fs.existsSync(paginaCfg.dataPath)) {
    console.warn(`⚠️ No existe el archivo de publicaciones: ${paginaCfg.dataPath}. Omitiendo.`);
    return { exitos: 0, pendientesRestantes: 0, fueraDeVentana: 0 };
  }

  let posts = [];
  try {
    posts = JSON.parse(fs.readFileSync(paginaCfg.dataPath, 'utf-8'));
  } catch (e) {
    console.error(`❌ Error al parsear JSON ${paginaCfg.dataPath}: ${e.message}`);
    return { exitos: 0, pendientesRestantes: 0, fueraDeVentana: 0 };
  }

  const nowTs = Math.floor(Date.now() / 1000);
  const minSchedTs = nowTs + 600; // Mínimo 10 minutos hacia el futuro según Meta
  const maxSchedTs = nowTs + (28 * 86400); // Límite estricto y seguro de Meta: 28 días

  console.log(`🔹 Page ID: ${pageId}`);
  console.log(`🔹 Fecha actual: ${new Date().toLocaleString()}`);
  console.log(`🔹 Ventana permitida por Meta:`);
  console.log(`   - Mínimo (+10 min): ${new Date(minSchedTs * 1000).toLocaleString()}`);
  console.log(`   - Máximo (+28 días): ${new Date(maxSchedTs * 1000).toLocaleString()}`);

  const programados = posts.filter(p => p.estado === 'programado' || p.estado === 'publicado');
  const pendientes = posts.filter(p => p.estado === 'pendiente');

  console.log(`📊 Total en cola: ${posts.length}`);
  console.log(`   ✅ Ya programados/publicados: ${programados.length}`);
  console.log(`   ⏳ Pendientes por evaluar: ${pendientes.length}\n`);

  let exitos = 0;
  let fueraDeVentana = 0;

  for (let i = 0; i < pendientes.length; i++) {
    const p = pendientes[i];
    const ts = aUnixTimestamp(p.fecha, p.hora);

    // 1. Validar si está en el pasado o a menos de 10 min
    if (ts < minSchedTs) {
      console.log(`⚠️ Post #${p.id} (${p.fecha} ${p.hora}) tiene fecha en el pasado o menor a 10 min. Omitiendo programación automática.`);
      continue;
    }

    // 2. Validar límite máximo de Meta (28 días)
    if (ts > maxSchedTs) {
      fueraDeVentana++;
      continue;
    }

    const tituloCorto = (p.titulo || p.arquetipo || `Post #${p.id}`).substring(0, 35);
    process.stdout.write(`[Programando Meta] #${String(p.id).padStart(3, '0')} | ${p.fecha} ${p.hora} | ${tituloCorto}... `);

    const imgFullPath = paginaCfg.resolverRutaImagen(p);
    const caption = paginaCfg.formatearTexto(p);
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
      } else {
        console.log(`❌ Imagen no encontrada en: ${imgFullPath}`);
        continue;
      }

      const res = await fetch(url, {
        method: 'POST',
        body: formData,
      });

      const data = await res.json();

      if (res.ok && (data.id || data.post_id)) {
        const postId = data.id || data.post_id;
        p.estado = 'programado';
        p.post_id = postId;
        p.meta_post_id = postId;
        p.fecha_programada_unix = ts;
        exitos++;

        // Guardar progreso inmediatamente para evitar pérdidas ante cortes
        fs.writeFileSync(paginaCfg.dataPath, JSON.stringify(posts, null, 2), 'utf-8');
        console.log(`✅ OK (ID: ${postId})`);
      } else {
        const errMsg = data.error?.message || JSON.stringify(data);
        console.log(`❌ Error Meta: ${errMsg}`);

        if (errMsg.toLowerCase().includes('expire') || errMsg.toLowerCase().includes('session')) {
          console.error(`⚠️ Token de ${paginaCfg.nombre} ha expirado. Requiere renovación.`);
          break;
        }
      }
    } catch (err) {
      console.log(`❌ Excepción de red: ${err.message}`);
    }

    await sleep(2500); // Pausa amigable de 2.5s para respetar rate limits de Meta
  }

  // Guardado final asegurado
  fs.writeFileSync(paginaCfg.dataPath, JSON.stringify(posts, null, 2), 'utf-8');

  console.log(`\n📋 Resumen ${paginaCfg.nombre}:`);
  console.log(`   ✅ Nuevos programados hoy: ${exitos}`);
  console.log(`   ⏳ Fuera de ventana (>28 días): ${fueraDeVentana} (se programarán automáticamente al entrar en fecha)`);

  return { exitos, fueraDeVentana, pendientesRestantes: pendientes.length - exitos };
}

async function main() {
  console.log('='.repeat(70));
  console.log('🤖 SISTEMA UNIFICADO DE PUBLICACIÓN MULTI-PÁGINA FACEBOOK');
  console.log('   Páginas vinculadas: Huellas con Propósito & Metalidad de Acero');
  console.log('='.repeat(70));

  let totalExitos = 0;
  let totalEsperandoVentana = 0;

  for (const pag of PAGINAS) {
    const res = await procesarPagina(pag);
    totalExitos += res.exitos;
    totalEsperandoVentana += res.fueraDeVentana;
  }

  console.log('\n' + '='.repeat(70));
  console.log('🎉 RESUMEN GLOBAL DE EJECUCIÓN MULTI-PÁGINA:');
  console.log(`   ✅ Total de publicaciones programadas con éxito en Meta: ${totalExitos}`);
  if (totalEsperandoVentana > 0) {
    console.log(`   ⏳ Publicaciones en espera (${totalEsperandoVentana} posts):`);
    console.log(`      Superan el límite estricto de 28 días de Meta. GitHub Actions las irá`);
    console.log(`      programando de forma escalonada en sus ejecuciones automáticas.`);
  }
  console.log('='.repeat(70));
}

main().catch(err => {
  console.error('❌ Error fatal en publicador:', err);
  process.exit(1);
});
