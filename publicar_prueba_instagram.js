/**
 * SCRIPT DE PRUEBA EN VIVO: PUBLICACIÓN EN INSTAGRAM
 * ----------------------------------------------------
 * Publica una foto real en la cuenta @huellasconproposito26
 * usando la Meta Graph API v19.0 y el Token Perpetuo.
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const CONFIG_PATH = path.join(__dirname, 'config.json');

async function publicarEnInstagram() {
  console.log('='.repeat(65));
  console.log('📸 INICIANDO PRUEBA DE PUBLICACIÓN EN INSTAGRAM');
  console.log('='.repeat(65));

  if (!fs.existsSync(CONFIG_PATH)) {
    console.error('❌ Error: No se encontró config.json');
    return;
  }

  const cfg = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf-8'));
  const token = cfg.PAGINAS?.huellas_con_proposito?.token || cfg.ACCESS_TOKEN;
  const igUserId = cfg.PAGINAS?.huellas_con_proposito?.instagram?.id;

  if (!token || !igUserId) {
    console.error('❌ Falta token o ID de Instagram en config.json');
    return;
  }

  console.log(`🔹 Instagram Business ID: ${igUserId}`);
  console.log(`🔹 Cuenta destino: @huellasconproposito26`);

  // URL pública de la imagen en GitHub
  const imageUrl = 'https://raw.githubusercontent.com/jorgeanalista2008/publicador_facebook/main/noviembre/perritos/nov_002_2026-11-01_perrito_1230.jpg';
  
  const caption = `🐾 Cada mirada cuenta una historia de lealtad y esperanza. 

En "Huellas con Propósito" creemos que ningún perrito de barrio merece el olvido. Su nobleza no conoce rencores; solo esperan una mano amiga que les devuelva la fe en la humanidad. ❤️

Si crees en darles una segunda oportunidad, únete a nuestra comunidad. 🐕✨

#HuellasConPropósito #PerrosDeBarrio #RescateAnimal #AdoptaNoCompres #AmorPerruno #HistoriasReales`;

  console.log(`\n1. Creando contenedor de medios en Instagram con imagen pública...`);
  console.log(`   URL Imagen: ${imageUrl}`);

  try {
    const params1 = new URLSearchParams();
    params1.append('image_url', imageUrl);
    params1.append('caption', caption);
    params1.append('access_token', token);

    const res1 = await fetch(`https://graph.facebook.com/v19.0/${igUserId}/media`, {
      method: 'POST',
      body: params1
    });

    const data1 = await res1.json();
    console.log('   Respuesta creación:', data1);

    if (!res1.ok || !data1.id) {
      console.error('❌ Error creando contenedor:', data1);
      return;
    }

    const creationId = data1.id;
    console.log(`✅ Contenedor creado con éxito. Creation ID: ${creationId}`);

    console.log('\n2. Esperando 4 segundos a que Meta procese la imagen...');
    await new Promise(r => setTimeout(r, 4000));

    console.log('3. Publicando contenedor en el feed de Instagram...');
    const params2 = new URLSearchParams();
    params2.append('creation_id', creationId);
    params2.append('access_token', token);

    const res2 = await fetch(`https://graph.facebook.com/v19.0/${igUserId}/media_publish`, {
      method: 'POST',
      body: params2
    });

    const data2 = await res2.json();
    console.log('   Respuesta publicación:', data2);

    if (res2.ok && data2.id) {
      const mediaId = data2.id;
      console.log('\n' + '='.repeat(65));
      console.log(`🎉 ¡PUBLICACIÓN EN INSTAGRAM EXITOSA! Media ID: ${mediaId}`);
      console.log('='.repeat(65));

      // Obtener el enlace directo (permalink) del post
      const permalinkRes = await fetch(`https://graph.facebook.com/v19.0/${mediaId}?fields=permalink,timestamp,media_type&access_token=${token}`);
      const permalinkData = await permalinkRes.json();
      if (permalinkData.permalink) {
        console.log(`🔗 Enlace directo al post en Instagram: ${permalinkData.permalink}`);
      }
    } else {
      console.error('❌ Error publicando en Instagram:', data2);
    }
  } catch (err) {
    console.error('❌ Excepción de red:', err.message);
  }
}

publicarEnInstagram();
