# 🚀 Publicador Automático de Facebook (Node.js + GitHub Actions)

Sistema automatizado en **Node.js** para programar contenido en la página de Facebook **Huellas con Propósito** utilizando la API oficial de Meta (Graph API) y **GitHub Actions** (100% gratuito, sin servidores externos).

---

## 📁 Estructura del Proyecto

```text
D:\github\publicador_facebook\
├── .github/
│   └── workflows/
│       └── publicar.yml        # Flujo de GitHub Actions (Cron diario + botón manual)
├── noviembre/
│   ├── perritos/               # 60 fotos reales de perritos de barrio
│   ├── filosofia/              # 60 imágenes de bustos de mármol estoico
│   └── publicaciones.json      # Base de datos con las 120 publicaciones
├── publicador.js               # Script en Node.js nativo (fetch + FormData)
├── package.json
├── index.html                  # Calendario web interactivo
└── .gitignore
```

---

##  pasos para Conectar con GitHub

### 1. Inicializar Git y subir a tu GitHub

Abre tu terminal en `D:\github\publicador_facebook` y ejecuta:

```bash
git init
git add .
git commit -m "feat: publicador automatico nodejs para huellas con proposito"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/publicador_facebook.git
git push -u origin main
```

*(Reemplaza `TU_USUARIO` con tu nombre de usuario de GitHub).*

---

### 2. Configurar los Secretos en GitHub (Solo se hace una vez)

En tu repositorio de GitHub:
1. Ve a **Settings** (Configuración) > **Secrets and variables** > **Actions**.
2. Haz clic en **New repository secret** y añade estos dos secretos:

| Nombre del Secreto | Valor |
| :--- | :--- |
| `PAGE_ID` | `1367888553074849` |
| `META_ACCESS_TOKEN` | Tu Token oficial de la página (el que generas en developers.facebook.com) |

> 🔒 **Seguridad total:** Gracias a `.gitignore`, tu archivo `config.json` local nunca se sube a internet. Tus credenciales quedan protegidas bajo el cifrado de GitHub.

---

### 3. ¿Cómo funciona la automatización?

* ⏰ **Automático por Cron:** Todos los días a las **12:00 UTC (08:00 AM hora local)**, GitHub Actions despierta una máquina virtual en la nube, ejecuta `node publicador.js` y revisa qué publicaciones han entrado dentro de la ventana de 29 días de Meta para programarlas.
* 🖱️ **Manual con 1 Clic:** En tu GitHub, ve a la pestaña **Actions** > **Programador Automático de Facebook** > **Run workflow**.
* 💾 **Auto-guardado:** Cuando GitHub programa nuevos posts, automáticamente hace un commit de vuelta a `noviembre/publicaciones.json` con el estado actualizado y los IDs de Meta.
