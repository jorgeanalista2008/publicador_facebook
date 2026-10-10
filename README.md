# 🚀 Publicador Automático Multi-Página de Facebook (Node.js + GitHub Actions + IA)

Ecosistema 100% automatizado en **Node.js** para programar contenido viral, responder comentarios con IA y monitorear métricas en tiempo real a través de la API oficial de Meta (Graph API v19.0) y **GitHub Actions** (100% gratuito, sin necesidad de servidores de pago ni VPS).

---

## 🏛️ Páginas Conectadas en el Ecosistema

| Página | ID de Facebook | Nicho & Estilo | IA Persona |
| :--- | :--- | :--- | :--- |
| **Huellas con Propósito** | `1367888553074849` | Rescate comunitario de perritos (#PerrosDeBarrio) y estoicismo clásico | Cálida, empática, amante de los animales y reflexiva estoica |
| **Metalidad de Acero** | `1375923958937880` | Mentalidad, disciplina implacable, 0 excusas y alto rendimiento (Goggins/Jocko) | Firme, inspiradora, sin filtros, desafía al lector y extermina el victimismo |

---

## ⏱️ Limitaciones Oficiales de Meta Graph API & Cómo las Gestiona el Sistema

1. **Ventana Estricta de Programación (10 min a 28 días):**
   * Meta **rechaza con error 400** cualquier intento de programar publicaciones a más de 29 días o a menos de 10 minutos en el futuro.
   * **Nuestra solución:** `publicador.js` calcula dinámicamente la ventana permitida `[ahora + 10m, ahora + 28 días]`. Las publicaciones futuras que superan los 28 días se mantienen en estado `pendiente`.
   * **GitHub Actions escalonado:** Como el flujo corre automáticamente cada 4 horas (`cron`), a medida que los días avanzan, los nuevos posts entran automáticamente en la ventana y se programan en Meta sin intervención manual.

2. **Límites de Tasa (Rate Limiting):**
   * Meta penaliza ráfagas masivas instantáneas. El motor incluye pausas automáticas de 2.5 segundos entre cada subida de foto y respuesta de comentarios.

3. **Tokens Perpetuos de Página:**
   * Los tokens de usuario caducan a las 2 horas. Hemos intercambiado los tokens por **Page Access Tokens Permanentes** (`expires_at: 0`), garantizando que la automatización no se interrumpa.

---

## 📁 Estructura del Repositorio Unificado

```text
D:\github\publicador_facebook\
├── .github/
│   └── workflows/
│       └── publicar.yml               # GitHub Actions: orquesta publicación, respuestas y métricas
├── mentalidad_de_acero/
│   ├── imagenes/                      # Infografías 4:5 virales (Contraste de Mentalidad)
│   └── publicaciones.json             # Batería de contenido de Metalidad de Acero
├── noviembre/
│   ├── perritos/                      # Fotos de perritos de barrio
│   ├── filosofia/                     # Imágenes de bustos estoicos
│   └── publicaciones.json             # Batería de 120 publicaciones para Huellas
├── componer_mentalidad_acero.py       # Motor gráfico de renderizado de infografías 4:5
├── cerebro_ia.js                      # Generador de crónicas y evaluador de comentarios con Gemini
├── publicador.js                      # Publicador UNIFICADO multi-página
├── respondedor_comentarios.js         # Community Manager IA UNIFICADO multi-página
├── metricas.js                        # Extractor de métricas Graph API multi-página
├── metricas.json                      # Base de datos JSON para el Dashboard
├── index.html                         # Dashboard Web interactivo en GitHub Pages
└── config.json                        # Credenciales locales (protegido por .gitignore)
```

---

## 🔑 Secretos Requeridos en GitHub Actions

En tu repositorio de GitHub, ve a **Settings** > **Secrets and variables** > **Actions** y agrega los siguientes secretos:

| Nombre del Secreto | Descripción | Valor Ejemplo |
| :--- | :--- | :--- |
| `PAGE_ID` | ID de Huellas con Propósito | `1367888553074849` |
| `META_ACCESS_TOKEN` | Token perpetuo de Huellas | `EAAi0EJZBzmJo...` |
| `PAGE_ID_ACERO` | ID de Metalidad de Acero | `1375923958937880` |
| `META_ACCESS_TOKEN_ACERO` | Token perpetuo de Metalidad de Acero | `EAAi0EJZBzmJo...` |
| `GEMINI_API_KEY` | Llave API de Google AI Studio | `AQ.Ab8RN6LD...` |

---

## 🌐 Dashboard en Vivo

Puedes acceder al Dashboard interactivo en GitHub Pages:
**`https://jorgeanalista2008.github.io/publicador_facebook/`**
* Permite alternar entre ambas páginas con el selector superior.
* Muestra métricas de seguidores, engagement, gráficos de interacciones y el calendario editorial completo de publicaciones programadas y pendientes.
