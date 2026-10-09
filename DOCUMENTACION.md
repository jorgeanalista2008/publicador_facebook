# 🐾 Documentación Completa del Sistema de Automatización y Cerebro IA en Facebook

> **Página Oficial:** Huellas con Propósito (ID: `1367888553074849`)  
> **Repositorio GitHub:** [jorgeanalista2008/publicador_facebook](https://github.com/jorgeanalista2008/publicador_facebook)  
> **Dashboard en Vivo:** [https://jorgeanalista2008.github.io/publicador_facebook/](https://jorgeanalista2008.github.io/publicador_facebook/)  
> **Fecha de Implementación:** Octubre 2026  

---

## 📌 1. Resumen Ejecutivo del Proyecto

Se diseñó e implementó un ecosistema completo y **100% autónomo** en la nube (con coste de servidor \$0 USD) para gestionar, publicar, analizar y responder interacciones en la página de Facebook **"Huellas con Propósito"**.

El sistema integra:
1. **Publicación y Programación Masiva** respetando las restricciones de la API de Meta.
2. **Cerebro Inteligente con Google Gemini API** para redactar contenido viral y contestar comentarios.
3. **Generación Gráfica Profesional** en formato vertical de alto impacto (estilo Carlos Arias).
4. **Community Manager Autónomo con IA** para interactuar con los seguidores en tiempo real.
5. **Dashboard Web en Vivo en GitHub Pages** para consultar métricas, alcance y calendario editorial.
6. **Ejecución Continua con GitHub Actions** cada 4 horas en la nube sin necesidad de tener la computadora encendida.

---

## 📅 2. Estrategia Editorial y Calendario de Publicaciones

### A. Octubre 2026 (48 Publicaciones Programadas y Activas)
- **Frecuencia:** 2 publicaciones diarias (09:00 AM y 19:30 PM).
- **Temática:** Crónicas de rescate animal y adopción comunitaria con fotografías reales de perritos.

### B. Noviembre 2026 (120 Publicaciones Listas)
- **Frecuencia:** 4 turnos diarios automáticos:
  - **08:00 AM** — 🏛️ Filosofía Estoica (Marco Aurelio, Séneca, Epicteto).
  - **12:30 PM** — 🐶 Crónica de Perrito de Barrio.
  - **17:30 PM** — 🏛️ Filosofía Estoica (Storytelling biográfico).
  - **20:30 PM** — 🐶 Crónica de Perrito de Barrio.
- **Estado en Meta:** Los primeros 24 posts (1 al 6 de Noviembre) ya se encuentran programados y activos en Facebook. Las fechas posteriores se programan progresivamente para cumplir la regla estricta de Meta Graph API (máximo 28-29 días de anticipación).

---

## 🎨 3. Patrones de Redacción y Diseño Gráfico Viral

### 🐶 A. Crónicas Comunitarias (#PerrosDeBarrio)
Estructura rigurosa en 5 párrafos diseñada para detener el scroll y generar máxima empatía:
1. **Gancho de Barrio:** Nombre de vecino/calle real, situación cotidiana (mudanza, letrero de renta), frase indignante entre comillas («el perro no cabe», «no es mi problema») y emoji de dolor (😡 / 💔).
2. **Dolor Conductual:** El perro esperando junto a la reja o portón, levantando las orejas ante cada motor creyendo que es su familia.
3. **El Rescate:** Rescate en un día específico ("Al sexto día..."), estado físico crudo y gesto conmovedor ("movía tímidamente su cola").
4. **Justicia Vecinal:** Multa, amonestación o lección moral a los antiguos dueños.
5. **Final y Adopción:** Nuevo hogar con nombre simbólico, superación del trauma y cierre esperanzador con ❤️.

### 🏛️ B. Filosofía Estoica (Estilo Carlos Arias / Daily Stoic)
- **Narrativa:** Comienza con el dolor histórico del filósofo (peste de Antonino, exilio en Córcega, esclavitud en Roma), cita clave contundente y aplicación práctica inmediata al lector contemporáneo.
- **Gráfica:** Formato vertical 4:5 (1080 x 1350 px), barras laterales en naranja terracota cálido, obra de arte central o busto romano en mármol auténtico, tipografía serif blanca para el nombre y cita destacada en letras doradas.

---

## 🛠️ 4. Arquitectura Técnica y Módulos Desarrollados

El proyecto fue desarrollado en **Node.js (v22/v24)** con módulos ES nativos y llamadas REST directas a **Meta Graph API (v19.0)** y **Google Gemini API**:

```
d:\github\publicador_facebook\
├── .github/
│   └── workflows/
│       └── publicar.yml               # GitHub Actions: Ejecución cada 4 horas
├── noviembre/
│   ├── perritos/                     # 60 fotos reales curadas de perritos
│   ├── filosofia/                    # 60 bustos y obras de arte estoicas
│   └── publicaciones.json            # Base de datos de 120 posts de noviembre
├── cerebro_ia.js                     # Motor de IA con Gemini 3.5 Flash
├── publicador.js                     # Publicador y programador a Meta Graph API
├── respondedor_comentarios.js        # Community Manager IA autónomo
├── metricas.js                       # Extractor de métricas de Facebook
├── metricas.json                     # Snapshot de métricas consumido por el front
├── historial_comentarios.json        # Registro anti-duplicados de comentarios
├── index.html                        # Dashboard web con Tailwind CSS y Chart.js
├── .nojekyll                         # Despliegue inmediato en GitHub Pages
├── .gitignore                        # Protección estricta de tokens y claves
└── config.json                       # Credenciales locales (ignorado por Git)
```

### 🧠 `cerebro_ia.js` (Google Gemini)
- Conexión con `gemini-3.5-flash` (con respaldo automático a `gemini-3.7-flash` y `gemini-flash-latest`).
- Redactor automático de crónicas y ensayos estoicos.
- Analizador de intenciones y sentimientos de comentarios.

### 🤖 `respondedor_comentarios.js` (Community Manager IA)
- Monitorea publicaciones recientes.
- Clasifica comentarios:
  - **Adopción / Ayuda:** Agradece con calidez e invita a escribir por mensaje privado (inbox).
  - **Empatía / Emoción:** Valida el sentimiento con afecto y emojis.
  - **Debate filosófico:** Responde con sabiduría estoica.
  - **Spam / Odio:** Filtra y descarta (`IGNORAR`).
- Publica la respuesta oficial como `Huellas con Propósito`.

### 📊 `metricas.js` e `index.html` (Dashboard Web)
- Extracción de seguidores reales, foto de página, reacciones, comentarios y compartidos.
- Gráficos interactivos de alcance por día y distribución por temática.
- Tabla con enlace directo `Ver en Facebook ↗` a cada post publicado.
- Pestaña de calendario editorial interactivo con botón de copiado rápido.

---

## ☁️ 5. Flujo de Ejecución en la Nube (GitHub Actions)

El archivo `.github/workflows/publicar.yml` corre con el cron `'0 0,4,8,12,16,20 * * *'` (cada 4 horas):
1. **Clona el repositorio** en una máquina virtual Linux.
2. **Ejecuta `publicador.js`:** Programa los posts que hayan entrado en la ventana de 28 días.
3. **Ejecuta `respondedor_comentarios.js`:** Lee y responde comentarios nuevos con Gemini.
4. **Ejecuta `metricas.js`:** Extrae las métricas actualizadas de Facebook.
5. **Git Auto-Commit:** Guarda los cambios en `publicaciones.json`, `metricas.json` e `historial_comentarios.json` con `[skip ci]`.
6. **GitHub Pages:** Publica automáticamente las actualizaciones en el sitio web público.

---

## 🔒 6. Seguridad y Credenciales

- **Token de Acceso Permanente:** Generado con expiración infinita (`expires_at: 0`) para la página `Huellas con Propósito`.
- **GitHub Secrets:** Almacenamiento cifrado en la nube:
  - `PAGE_ID`: `1367888553074849`
  - `META_ACCESS_TOKEN`: Token permanente de página.
  - `GEMINI_API_KEY`: API Key de Google AI Studio.
- **Git Seguro:** Ninguna credencial ni token sensible se encuentra en el código ni en el historial de Git, permitiendo que el repositorio sea público para GitHub Pages con total tranquilidad.

---

## 🚀 7. Enlaces y Accesos Rápidos

- 🌐 **Dashboard en Vivo:** [https://jorgeanalista2008.github.io/publicador_facebook/](https://jorgeanalista2008.github.io/publicador_facebook/)
- 💻 **Repositorio de Código:** [https://github.com/jorgeanalista2008/publicador_facebook](https://github.com/jorgeanalista2008/publicador_facebook)
- ⚙️ **Ejecución Manual de Tareas:** [GitHub Actions Tab](https://github.com/jorgeanalista2008/publicador_facebook/actions)
- 🐾 **Página de Facebook:** [Huellas con Propósito](https://www.facebook.com/1367888553074849)
