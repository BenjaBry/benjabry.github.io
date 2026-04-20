# CYLO Guatemala — Sitio Web Completo

Sitio web multi-página listo para subir a GitHub Pages o cualquier hosting estático.

## Estructura de archivos

```
cylo_site/
├── index.html                  ← Redirección automática a inicio.html
├── inicio.html                 ← Página principal (Home)
├── nosotros.html               ← Quiénes somos
├── contacto.html               ← Contacto y formulario
├── catalogo.html               ← Página de categorías (puente)
├── styles.css                  ← Estilos compartidos para todas las páginas
├── components.js               ← JS compartido (nav, FAQ, animaciones)
│
└── catalogo_cylo_2026.html     ← ⚠️ AGREGAR TU ARCHIVO DE CATÁLOGO AQUÍ
    imagenes/                   ← ⚠️ AGREGAR CARPETA DE IMÁGENES AQUÍ
```

## Cómo desplegar en GitHub Pages

1. Crea un repositorio en GitHub (ej: `cyloguatemala`)
2. Sube todos estos archivos al repositorio
3. **Copia también** tu `catalogo_cylo_2026.html` y la carpeta `imagenes/`
4. Ve a **Settings → Pages → Source: main branch → / (root)**
5. Tu sitio estará en: `https://tuusuario.github.io/cyloguatemala/`

## Con dominio personalizado (cyloguatemala.me)

1. En GitHub Pages Settings, agrega tu dominio en "Custom domain"
2. En tu proveedor de dominio, configura los DNS:
   - Tipo A: `185.199.108.153`
   - Tipo A: `185.199.109.153`
   - Tipo A: `185.199.110.153`
   - Tipo A: `185.199.111.153`
   - CNAME: `www` → `tuusuario.github.io`

## Páginas incluidas

| Página | URL local | Descripción |
|--------|-----------|-------------|
| Inicio | `inicio.html` | Hero, categorías, pasos, FAQ, testimonios |
| Productos | `catalogo.html` | Resumen de categorías + link al catálogo |
| Nosotros | `nosotros.html` | Historia, misión, valores, equipo, mapa |
| Contacto | `contacto.html` | Formulario, canales, horarios, métodos de pago |

## Notas importantes

- El formulario de contacto redirige automáticamente a WhatsApp con el mensaje prellenado
- El botón flotante de WhatsApp aparece en todas las páginas
- Todas las páginas son 100% responsivas (mobile, tablet, desktop)
- El catálogo completo (`catalogo_cylo_2026.html`) debe colocarse en la misma carpeta
- Las imágenes deben estar en `imagenes/` junto a los HTMLs

## Tecnologías usadas

- HTML5 semántico puro
- CSS3 con variables personalizadas
- JavaScript vanilla (sin frameworks)
- Google Fonts: Playfair Display + DM Sans
- Sin dependencias externas

---
CYLO Guatemala 2026 © — Todos los derechos reservados.
