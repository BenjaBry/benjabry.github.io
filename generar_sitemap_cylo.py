# -*- coding: utf-8 -*-
"""
Generador de sitemap.xml para CYLO Guatemala con soporte para Blog.
Colócalo en la raíz del proyecto y ejecuta:
python generar_sitemap_cylo.py
"""

from datetime import date
from pathlib import Path
from typing import Dict, Optional
from xml.sax.saxutils import escape

DOMINIO = "https://www.cyloguatemala.me"
RAIZ = Path(__file__).resolve().parent
SALIDA_SITEMAP = RAIZ / "sitemap.xml"
IDIOMA = "es-GT"

CARPETAS_EXCLUIDAS = {
    ".git", ".github", ".vercel", "__pycache__", "node_modules",
    ".next", "dist", "build", "assets", "img", "images", "css", "js", "fonts"
}

ARCHIVOS_EXCLUIDOS = {
    "template.html", "template_producto.html", "plantilla.html",
    "404.html", "500.html", "test.html", "prueba.html"
}

RUTAS_ANTIGUAS_EXCLUIDAS = {
    "inicio.html", "catalogo.html", "Catalogo.html",
    "catalogo-digital.html", "Catalogo-digital.html"
}

def prioridad_y_frecuencia(url_path: str) -> tuple[str, str]:
    limpio = url_path.strip("/")

    if limpio == "":
        return "1.00", "weekly"
    if limpio == "Catalogo-digital-2026.html":
        return "0.95", "weekly"
    if limpio == "blog/index.html":
        return "0.78", "weekly"
    if limpio.startswith("blog/"):
        return "0.68", "monthly"
    if limpio.startswith("productos/"):
        return "0.80", "monthly"
    if limpio == "contacto.html":
        return "0.80", "monthly"
    if limpio == "nosotros.html":
        return "0.70", "monthly"
    if limpio in {"politica-de-privacidad.html", "terminos-y-condiciones.html"}:
        return "0.30", "yearly"
    return "0.50", "monthly"

def normalizar_url(base: str, url_path: str) -> str:
    if url_path == "":
        return base.rstrip("/") + "/"
    return base.rstrip("/") + "/" + url_path.lstrip("/")

def debe_excluir_archivo(path: Path) -> bool:
    if path.name in ARCHIVOS_EXCLUIDOS:
        return True
    if path.name in RUTAS_ANTIGUAS_EXCLUIDAS:
        return True
    if path.name.startswith("_"):
        return True
    if set(path.parts).intersection(CARPETAS_EXCLUIDAS):
        return True
    return False

def obtener_lastmod(path: Optional[Path]) -> str:
    if path and path.exists():
        try:
            return date.fromtimestamp(path.stat().st_mtime).isoformat()
        except Exception:
            pass
    return date.today().isoformat()

def convertir_path_a_url(path: Path) -> Optional[str]:
    rel = path.relative_to(RAIZ).as_posix()

    if path.name == "index.html" and "/" not in rel:
        return ""

    if rel == "blog/index.html":
        return "blog/"

    if rel.startswith("productos_generados/"):
        return f"productos/{path.name}"

    return rel

def construir_entrada(url: str, lastmod: str, changefreq: str, priority: str) -> str:
    url_escapada = escape(url)
    return f"""  <url>
    <loc>{url_escapada}</loc>
    <lastmod>{lastmod}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
    <xhtml:link rel="alternate" hreflang="{IDIOMA}" href="{url_escapada}"/>
  </url>"""

def generar_sitemap() -> None:
    urls: Dict[str, Dict[str, str]] = {}

    for path in RAIZ.rglob("*.html"):
        if debe_excluir_archivo(path):
            continue

        url_path = convertir_path_a_url(path)
        if url_path is None:
            continue

        if url_path.strip("/") in RUTAS_ANTIGUAS_EXCLUIDAS:
            continue

        url_publica = normalizar_url(DOMINIO, url_path)
        priority, changefreq = prioridad_y_frecuencia(url_path)

        urls[url_publica] = {
            "lastmod": obtener_lastmod(path),
            "changefreq": changefreq,
            "priority": priority,
        }

    # Forzar principales
    principales = {
        "": RAIZ / "index.html",
        "Catalogo-digital-2026.html": RAIZ / "Catalogo-digital-2026.html",
        "blog/": RAIZ / "blog" / "index.html",
        "nosotros.html": RAIZ / "nosotros.html",
        "contacto.html": RAIZ / "contacto.html",
    }

    for url_path, local_path in principales.items():
        url_publica = normalizar_url(DOMINIO, url_path)
        priority, changefreq = prioridad_y_frecuencia("blog/index.html" if url_path == "blog/" else url_path)
        urls[url_publica] = {
            "lastmod": obtener_lastmod(local_path if local_path.exists() else None),
            "changefreq": changefreq,
            "priority": priority,
        }

    def orden(url: str) -> tuple[int, str]:
        path = url.replace(DOMINIO.rstrip("/") + "/", "")
        if url.rstrip("/") == DOMINIO.rstrip("/"):
            return (0, "")
        if path == "Catalogo-digital-2026.html":
            return (1, path)
        if path == "blog/":
            return (2, path)
        if path.startswith("blog/"):
            return (3, path)
        if path in {"contacto.html", "nosotros.html"}:
            return (4, path)
        if path.startswith("productos/"):
            return (5, path)
        return (6, path)

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">',
        ""
    ]

    for url in sorted(urls.keys(), key=orden):
        data = urls[url]
        lines.append(construir_entrada(url, data["lastmod"], data["changefreq"], data["priority"]))
        lines.append("")

    lines.append("</urlset>")
    lines.append("")

    SALIDA_SITEMAP.write_text("\n".join(lines), encoding="utf-8")

    total_blog = sum(1 for u in urls if "/blog/" in u)
    total_productos = sum(1 for u in urls if "/productos/" in u)

    print("SITEMAP GENERADO")
    print(f"Archivo: {SALIDA_SITEMAP}")
    print(f"Total URLs: {len(urls)}")
    print(f"Blog URLs: {total_blog}")
    print(f"Productos detectados: {total_productos}")

if __name__ == "__main__":
    generar_sitemap()
