from pathlib import Path
import re
import shutil

# Carpeta donde están las páginas individuales de productos
PRODUCTOS_DIR = Path("productos")

# Ruta pública correcta del favicon para Vercel / dominio principal
FAVICON_TAG = '<link rel="icon" href="/img/favicon.png" type="image/png">'

# Carpeta de respaldo
BACKUP_DIR = Path("_backup_productos_favicon")


def leer_archivo(path: Path) -> str:
    """Lee HTML intentando UTF-8 primero y Latin-1 como respaldo."""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="latin-1")


def escribir_archivo(path: Path, contenido: str):
    """Escribe el archivo en UTF-8."""
    path.write_text(contenido, encoding="utf-8")


def agregar_o_reemplazar_favicon(html: str) -> tuple[str, bool]:
    """
    Agrega o reemplaza el favicon dentro del <head>.
    Retorna: contenido_modificado, cambio_realizado
    """

    # Detecta cualquier favicon anterior:
    # rel="icon", rel='icon', rel="shortcut icon", etc.
    favicon_regex = re.compile(
        r'\s*<link\b[^>]*rel=["\'](?:shortcut\s+icon|icon)["\'][^>]*>\s*',
        re.IGNORECASE
    )

    if favicon_regex.search(html):
        nuevo_html = favicon_regex.sub("\n" + FAVICON_TAG + "\n", html, count=1)

        # Elimina posibles duplicados adicionales
        nuevo_html = favicon_regex.sub("\n", nuevo_html)

        return nuevo_html, nuevo_html != html

    # Si no existe favicon, lo inserta después de <title> si encuentra title
    title_regex = re.compile(r'(</title>)', re.IGNORECASE)

    if title_regex.search(html):
        nuevo_html = title_regex.sub(r'\1' + "\n" + FAVICON_TAG, html, count=1)
        return nuevo_html, True

    # Si no encuentra <title>, lo inserta antes de </head>
    head_regex = re.compile(r'(</head>)', re.IGNORECASE)

    if head_regex.search(html):
        nuevo_html = head_regex.sub(FAVICON_TAG + "\n" + r'\1', html, count=1)
        return nuevo_html, True

    return html, False


def main():
    if not PRODUCTOS_DIR.exists():
        print(f"ERROR: No existe la carpeta: {PRODUCTOS_DIR.resolve()}")
        return

    html_files = sorted(PRODUCTOS_DIR.glob("*.html"))

    if not html_files:
        print(f"ERROR: No se encontraron archivos .html en: {PRODUCTOS_DIR.resolve()}")
        return

    BACKUP_DIR.mkdir(exist_ok=True)

    modificados = 0
    sin_cambios = 0
    errores = 0

    for archivo in html_files:
        try:
            html = leer_archivo(archivo)
            nuevo_html, cambio = agregar_o_reemplazar_favicon(html)

            if cambio:
                # Crear backup conservando el nombre original
                backup_path = BACKUP_DIR / archivo.name
                shutil.copy2(archivo, backup_path)

                escribir_archivo(archivo, nuevo_html)
                modificados += 1
                print(f"OK: favicon agregado/reemplazado -> {archivo}")
            else:
                sin_cambios += 1
                print(f"AVISO: no se encontró <head> o <title> -> {archivo}")

        except Exception as e:
            errores += 1
            print(f"ERROR en {archivo}: {e}")

    print("\nResumen:")
    print(f"Archivos modificados: {modificados}")
    print(f"Archivos sin cambios: {sin_cambios}")
    print(f"Errores: {errores}")
    print(f"Backups guardados en: {BACKUP_DIR.resolve()}")


if __name__ == "__main__":
    main()