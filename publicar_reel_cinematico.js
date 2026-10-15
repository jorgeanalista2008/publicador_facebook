import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const CONFIG_PATH = path.join(__dirname, 'config.json');
const HISTORIAL_PATH = path.join(__dirname, 'instagram_perritos_historial.json');

const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

async function main() {
  const cfg = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf-8'));
  const token = cfg.PAGINAS?.huellas_con_proposito?.token || cfg.ACCESS_TOKEN;
  const igUserId = cfg.PAGINAS?.huellas_con_proposito?.instagram?.id;

  if (!token || !igUserId) {
    console.error('❌ Falta token o Instagram ID');
    process.exit(1);
  }

  // 1. Eliminar la versión anterior estática de prueba
  const reelAntiguoId = '18095272214445173';
  console.log(`🗑️ Eliminando Reel de prueba antiguo (${reelAntiguoId})...`);
  try {
    const delRes = await fetch(`https://graph.facebook.com/v19.0/${reelAntiguoId}?access_token=${token}`, {
      method: 'DELETE'
    });
    const delData = await delRes.json();
    console.log('   Resultado eliminación:', delData);
  } catch (e) {
    console.log('   Aviso al borrar reel anterior:', e.message);
  }

  // 2. Publicar nuevo Reel Cinemático
  const videoUrl = 'https://jorgeanalista2008.github.io/publicador_facebook/videos_reels_cinematicos/reel_cinematico_1_tinaco.mp4';
  const caption = `🎬🐾 HISTORIA REAL: Lo dejaron en la azotea el día que entregaron las llaves.\n\nDoña Beatriz escuchó un llanto seco en la azotea vecina. Al asomarse, vio a este perrito atado a la pata de un tinaco bajo el sol ardiente del mediodía.\n\nLos vecinos se unieron para pasarle comida y agua hasta que los bomberos cortaron el cable incrustado en su cuello.\n\nHoy vive amado, corre libre y el sol nunca más volverá a lastimarlo. ❤️\n\n🐕 Súmate a @huellasconproposito26 si crees en las segundas oportunidades.\n\n#HuellasConPropósito #PerrosDeBarrio #RescateAnimal #HistoriasReales #AdoptaNoCompres #AmorPerruno #ReelsInstagram`;

  console.log('\n🚀 Creando contenedor de Reel Cinemático en Instagram...');
  console.log('   Video URL:', videoUrl);

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
    process.exit(1);
  }

  const creationId = data1.id;
  console.log(`   ✅ Contenedor creado. ID: ${creationId}`);

  // 3. Esperar a que Meta procese el video
  console.log('⏳ Esperando que Meta procese el video cinemático...');
  let listo = false;
  for (let i = 1; i <= 30; i++) {
    process.stdout.write(`   Intento ${i}/30... `);
    try {
      const res = await fetch(`https://graph.facebook.com/v19.0/${creationId}?fields=status_code,status&access_token=${token}`);
      const data = await res.json();
      const code = data.status_code;

      if (code === 'FINISHED') {
        console.log('✅ ¡PROCESADO CON ÉXITO!');
        listo = true;
        break;
      } else if (code === 'IN_PROGRESS') {
        console.log('en progreso...');
        await sleep(5000);
      } else if (code === 'ERROR') {
        console.log('❌ Error de procesamiento:', data);
        process.exit(1);
      } else {
        console.log(`estado: ${code || JSON.stringify(data)}`);
        await sleep(5000);
      }
    } catch (e) {
      console.log('error red, reintentando...');
      await sleep(5000);
    }
  }

  if (!listo) {
    console.error('❌ Tiempo de espera agotado.');
    process.exit(1);
  }

  // 4. Publicar
  console.log('📤 Publicando Reel en el feed de Instagram...');
  const body2 = new URLSearchParams();
  body2.append('creation_id', creationId);
  body2.append('access_token', token);

  const res2 = await fetch(`https://graph.facebook.com/v19.0/${igUserId}/media_publish`, {
    method: 'POST',
    body: body2
  });

  const data2 = await res2.json();
  if (!res2.ok || !data2.id) {
    console.error('❌ Error publicando Reel:', data2);
    process.exit(1);
  }

  const mediaId = data2.id;
  console.log(`\n🎉 ¡REEL CINEMÁTICO PUBLICADO CON ÉXITO! Media ID: ${mediaId}`);

  await sleep(3000);
  const permRes = await fetch(`https://graph.facebook.com/v19.0/${mediaId}?fields=permalink&access_token=${token}`);
  const permData = await permRes.json();
  const permalink = permData.permalink || `https://www.instagram.com/reel/${mediaId}/`;

  console.log(`🔗 Enlace en vivo del Reel Cinemático: ${permalink}`);

  // Actualizar historial
  let historial = { publicaciones: [], ultimo_tipo: 'reel' };
  if (fs.existsSync(HISTORIAL_PATH)) {
    try {
      historial = JSON.parse(fs.readFileSync(HISTORIAL_PATH, 'utf-8'));
    } catch (e) {}
  }

  historial.publicaciones.push({
    tipo: 'reel_cinematico',
    reel_id: 1,
    nombre_perrito: 'Tinaco (Versión Cinemática Multi-Escena)',
    media_id: mediaId,
    permalink: permalink,
    fecha: new Date().toISOString()
  });
  historial.ultimo_tipo = 'reel';
  fs.writeFileSync(HISTORIAL_PATH, JSON.stringify(historial, null, 2), 'utf-8');

  console.log('✅ Historial actualizado.');
}

main().catch(console.error);
