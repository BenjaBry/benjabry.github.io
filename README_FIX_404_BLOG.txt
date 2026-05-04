CYLO - FIX 404 BLOG

Problema detectado:
El bloque del blog está enviando a una URL raíz sin /blog/, por ejemplo:
https://www.cyloguatemala.me/como-elegir-empaques-para-delivery-en-guatemala

Pero los artículos fueron generados dentro de:
https://www.cyloguatemala.me/blog/como-elegir-empaques-para-delivery-en-guatemala.html

Correcciones incluidas:
1. blog/index.html ahora usa enlaces absolutos:
   /blog/nombre-del-articulo.html

2. Los artículos del blog usan rutas absolutas para:
   /assets/css/cylo-ui.css
   /assets/css/cylo-blog.css
   /index.html
   /Catalogo-digital-2026.html
   /contacto.html
   /nosotros.html

3. Se incluye vercel.json con rewrites para soportar:
   /blog/nombre-del-articulo
   /nombre-del-articulo

Instalación:
1. Sube la carpeta blog/ completa.
2. Sube assets/css/cylo-blog.css si aún no está.
3. Sube assets/css/cylo-ui.css si quieres usar la versión incluida.
4. Sube vercel.json a la raíz del proyecto.
5. Corrige los cards del blog en tu index principal usando PARCHE_LINKS_BLOG_INDEX.txt si tienes cards de blog fuera de /blog/.
6. Haz commit y deploy en Vercel.

Nota:
Si ya tienes un vercel.json en tu proyecto, no lo reemplaces a ciegas. Integra la sección "rewrites" de este archivo con tu configuración actual.
