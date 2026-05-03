# CYLO Unified Nav

Archivos:
- assets/css/cylo-ui.css
- assets/js/cylo-ui.js

Uso en cada página:
1. En el <head>, agrega:
<link rel="stylesheet" href="https://www.cyloguatemala.me/assets/css/cylo-ui.css">

2. Justo después de abrir <body>, agrega:
<div id="cylo-header" data-active="catalogo"></div>

Valores de data-active:
- inicio
- catalogo
- nosotros
- contacto

Para páginas de producto usa:
<div id="cylo-header" data-active="catalogo"></div>

3. Antes de </body>, agrega:
<script src="https://www.cyloguatemala.me/assets/js/cylo-ui.js" defer></script>

4. Elimina de cada página el header viejo:
- top-bar
- site-header
- main-menu
- nav antiguo

Para pruebas locales, puedes usar:
<link rel="stylesheet" href="assets/css/cylo-ui.css">
<script src="assets/js/cylo-ui.js" defer></script>
