# Generador de sitemap CYLO Guatemala

## Qué hace

Este script genera un `sitemap.xml` actualizado para la nueva estructura de tu web.

Elimina de la lógica URLs antiguas como:

- `inicio.html`
- `catalogo.html`

Y usa la estructura actual:

- `/`
- `/Catalogo-digital-2026.html`
- `/nosotros.html`
- `/contacto.html`
- `/productos/<producto>.html`

## Cómo usarlo

1. Copia `generar_sitemap_cylo.py` en la raíz de tu proyecto.

2. Debe quedar donde están tus archivos principales:

```text
index.html
Catalogo-digital-2026.html
contacto.html
nosotros.html
productos_generados/
generar_sitemap_cylo.py
```

3. Ejecuta:

```bash
python generar_sitemap_cylo.py
```

4. Se generará:

```text
sitemap.xml
```

5. Sube `sitemap.xml` a GitHub junto con los cambios.

## Nota importante sobre productos

Si tus productos están localmente en:

```text
productos_generados/
```

el script los publica en el sitemap como:

```text
https://www.cyloguatemala.me/productos/nombre-del-producto.html
```

Esto es correcto si en Vercel/GitHub los productos finales quedan publicados bajo `/productos/`.

Si decides publicar literalmente la carpeta `/productos_generados/`, hay que cambiar esa regla en el script.
