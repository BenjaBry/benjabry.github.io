# -*- coding: utf-8 -*-
"""
CYLO RESET CATEGORÍAS V11
-------------------------

Este script corrige de raíz el problema del catálogo general:

1. Dentro del catálogo, las categorías ya NO recargan la página.
   Quedan como:
   href="#cat-pizzer-a"

2. Desde páginas de producto, las categorías apuntan al catálogo con hash limpio:
   href="/Catalogo-digital-2026.html#cat-pizzer-a"

3. Elimina scripts anteriores que mezclaban:
   ?cat=cat-x#cat-y

4. Inserta un único script limpio de navegación por categorías.

Uso:
- Coloca este archivo en la raíz del proyecto.
- Ejecuta:
  python reset_categorias_catalogo_v11.py
- Luego sube los archivos modificados a GitHub/Vercel.
"""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent

CATEGORIES = [
    ("Desechables", "cat-desechables"),
    ("Utensilios", "cat-utensilios"),
    ("Cocción", "cat-cocci-n"),
    ("Accesorios", "cat-accesorios"),
    ("Repostería", "cat-reposter-a"),
    ("Pizzería", "cat-pizzer-a"),
    ("Contenedores", "cat-contenedores"),
    ("Catering", "cat-catering"),
    ("Servicio", "cat-servicio"),
    ("Bartender", "cat-bartender"),
    ("Cafetería", "cat-cafeter-a"),
    ("Presentación", "cat-presentaci-n"),
    ("Vajilla", "cat-vajilla"),
    ("Cristalería", "cat-cristaler-a"),
]

CAT_IDS = [cat_id for _, cat_id in CATEGORIES]


CATALOG_CSS = r"""
<style>
/* CYLO RESET CATEGORÍAS V11 */
html {
  scroll-behavior: auto !important;
}

.cylo-catalog-page .cat-section,
.cylo-catalog-page [id^="cat-"] {
  scroll-margin-top: var(--cylo-category-offset, 96px) !important;
}

.cylo-catalog-page .cat-section.cylo-current-category {
  outline: 3px solid rgba(244, 123, 32, 0.32);
  outline-offset: 4px;
}

.toc-item.cylo-current-link,
.category-link.cylo-current-link,
.sidebar-cat.cylo-current-link,
a.cylo-current-link {
  background: #FFF8F1 !important;
  color: #F47B20 !important;
  border-left-color: #F47B20 !important;
}
</style>
"""


CATALOG_JS = r"""
<script>
/* CYLO RESET CATEGORÍAS V11 - navegación limpia sin recarga */
(function () {
  const CATEGORY_IDS = new Set([
    "cat-desechables",
    "cat-utensilios",
    "cat-cocci-n",
    "cat-accesorios",
    "cat-reposter-a",
    "cat-pizzer-a",
    "cat-contenedores",
    "cat-catering",
    "cat-servicio",
    "cat-bartender",
    "cat-cafeter-a",
    "cat-presentaci-n",
    "cat-vajilla",
    "cat-cristaler-a"
  ]);

  function clean(value) {
    return String(value || "").replace(/^#/, "").trim();
  }

  function getHeaderOffset() {
    const selectors = [
      ".cylo-header",
      ".site-header",
      ".catalog-header",
      ".catalog-topbar",
      ".search-bar"
    ];

    let total = 0;
    const counted = new Set();

    selectors.forEach(function (selector) {
      const el = document.querySelector(selector);
      if (!el || counted.has(el)) return;

      const rect = el.getBoundingClientRect();
      const style = window.getComputedStyle(el);

      if (rect.height <= 0) return;

      if ((style.position === "sticky" || style.position === "fixed") && rect.top <= 10) {
        total += Math.ceil(rect.height);
        counted.add(el);
      }
    });

    if (total < 70) {
      total = window.innerWidth <= 900 ? 78 : 92;
    }

    return total + 16;
  }

  function setOffsetVar() {
    document.documentElement.style.setProperty("--cylo-category-offset", getHeaderOffset() + "px");
  }

  function getCategoryFromHref(href) {
    if (!href) return "";

    try {
      const url = new URL(href, window.location.origin);
      const hash = clean(url.hash);
      if (CATEGORY_IDS.has(hash)) return hash;

      const queryCat = clean(url.searchParams.get("cat"));
      if (CATEGORY_IDS.has(queryCat)) return queryCat;
    } catch (error) {
      const rawHash = href.includes("#") ? href.split("#").pop() : "";
      const hash = clean(rawHash);
      if (CATEGORY_IDS.has(hash)) return hash;
    }

    return "";
  }

  function markCategory(catId) {
    document.querySelectorAll(".cylo-current-category").forEach(function (el) {
      el.classList.remove("cylo-current-category");
    });

    document.querySelectorAll(".cylo-current-link").forEach(function (el) {
      el.classList.remove("cylo-current-link");
    });

    const section = document.getElementById(catId);

    if (section) {
      section.classList.add("cylo-current-category");
      setTimeout(function () {
        section.classList.remove("cylo-current-category");
      }, 1200);
    }

    document.querySelectorAll('a[href="#' + catId + '"], a[href$="#' + catId + '"], a[href*="?cat=' + catId + '"]').forEach(function (link) {
      link.classList.add("cylo-current-link");
    });
  }

  function scrollToCategory(catId, behavior) {
    catId = clean(catId);

    if (!CATEGORY_IDS.has(catId)) return false;

    const target = document.getElementById(catId);
    if (!target) return false;

    setOffsetVar();

    const top = Math.max(
      0,
      target.getBoundingClientRect().top + window.pageYOffset - getHeaderOffset()
    );

    window.scrollTo({
      top: top,
      behavior: behavior || "smooth"
    });

    markCategory(catId);
    return true;
  }

  function scrollReliable(catId, behavior) {
    catId = clean(catId);
    if (!CATEGORY_IDS.has(catId)) return;

    [0, 120, 360, 850].forEach(function (delay, index) {
      setTimeout(function () {
        scrollToCategory(catId, index === 0 ? behavior : "auto");
      }, delay);
    });
  }

  function replaceUrlWithHash(catId) {
    if (!CATEGORY_IDS.has(catId)) return;
    history.pushState(null, "", "#" + catId);
  }

  document.addEventListener("click", function (event) {
    const link = event.target.closest("a[href]");
    if (!link) return;

    const catId = getCategoryFromHref(link.getAttribute("href"));
    if (!catId) return;

    /*
      Regla:
      - Si ya estamos dentro del catálogo, no recargar nunca.
      - Solo hacer scroll interno y dejar URL como #cat-x.
    */
    event.preventDefault();
    event.stopPropagation();
    event.stopImmediatePropagation();

    replaceUrlWithHash(catId);
    scrollReliable(catId, "smooth");
  }, true);

  document.addEventListener("change", function (event) {
    const select = event.target.closest("#catalogCategorySelect, #categorySelect");
    if (!select) return;

    const value = select.value || "";
    const catId = CATEGORY_IDS.has(clean(value)) ? clean(value) : getCategoryFromHref(value);

    if (!catId) return;

    event.preventDefault();
    event.stopPropagation();
    event.stopImmediatePropagation();

    replaceUrlWithHash(catId);
    scrollReliable(catId, "smooth");
  }, true);

  function boot() {
    setOffsetVar();

    const initial = getCategoryFromHref(window.location.href);
    if (initial) {
      history.replaceState(null, "", "#" + initial);
      scrollReliable(initial, "auto");
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }

  window.addEventListener("load", boot);
  window.addEventListener("resize", setOffsetVar);
  window.addEventListener("popstate", function () {
    const catId = getCategoryFromHref(window.location.href);
    if (catId) scrollReliable(catId, "smooth");
  });
})();
</script>
"""


def remove_old_category_code(text: str) -> str:
    """
    Remueve todos los intentos anteriores de categoría para no pelear entre scripts.
    """
    patterns = [
        r'\n?<style>\s*/\*\s*CYLO ANCHOR FIX V\d+.*?</style>\s*',
        r'\n?<style>\s*/\*\s*CYLO CATEGORY FIX V\d+.*?</style>\s*',
        r'\n?<style>\s*/\*\s*CYLO RESET CATEGORÍAS V\d+.*?</style>\s*',
        r'\n?<style>\s*/\*\s*Corrección de anclas de categorías.*?</style>\s*',

        r'\n?<script>\s*/\*\s*CYLO CATEGORY NAV V\d+.*?</script>\s*',
        r'\n?<script>\s*/\*\s*CYLO CATEGORY FIX V\d+.*?</script>\s*',
        r'\n?<script>\s*/\*\s*CYLO RESET CATEGORÍAS V\d+.*?</script>\s*',
        r'\n?<script>\s*/\*\s*CYLO FIX FINAL - Navegación exacta a categorías.*?</script>\s*',
        r'\n?<script>\s*/\*\s*Scroll preciso hacia categorías.*?</script>\s*',
    ]

    for pattern in patterns:
      text = re.sub(pattern, "\n", text, flags=re.S)

    return text


def fix_catalog_category_links(text: str) -> str:
    """
    Dentro del catálogo, todos los enlaces de categoría deben ser hash puro.
    Esto evita recargas y evita query/hash desalineados.
    """
    for _, cat_id in CATEGORIES:
        # href="/Catalogo-digital-2026.html?cat=algo#cat-id" -> href="#cat-id"
        text = re.sub(
            r'href="(?:https://www\.cyloguatemala\.me)?/?(?:\.\./|\.\/)?Catalogo-digital-2026(?:\.html)?(?:\?[^"#]*)?#' + re.escape(cat_id) + r'"',
            f'href="#{cat_id}"',
            text
        )

        # href="/Catalogo-digital-2026?cat=cat-id" sin hash -> href="#cat-id"
        text = re.sub(
            r'href="(?:https://www\.cyloguatemala\.me)?/?(?:\.\./|\.\/)?Catalogo-digital-2026(?:\.html)?\?cat=' + re.escape(cat_id) + r'"',
            f'href="#{cat_id}"',
            text
        )

        # href="#cat-id" se queda igual
        text = re.sub(
            r'href="#' + re.escape(cat_id) + r'"',
            f'href="#{cat_id}"',
            text
        )

    # Select de categorías: valores limpios si existen como URL completa.
    for _, cat_id in CATEGORIES:
        text = re.sub(
            r'value="(?:https://www\.cyloguatemala\.me)?/?(?:\.\./|\.\/)?Catalogo-digital-2026(?:\.html)?(?:\?[^"#]*)?#' + re.escape(cat_id) + r'"',
            f'value="{cat_id}"',
            text
        )
        text = re.sub(
            r'value="#' + re.escape(cat_id) + r'"',
            f'value="{cat_id}"',
            text
        )

    return text


def fix_product_category_links(text: str) -> str:
    """
    Desde fichas de producto, sí necesitamos ir al catálogo,
    pero sin query cat. Solo hash limpio.
    """
    for _, cat_id in CATEGORIES:
        text = re.sub(
            r'href="(?:https://www\.cyloguatemala\.me)?/?(?:\.\./|\.\/)?Catalogo-digital-2026(?:\.html)?(?:\?[^"#]*)?#' + re.escape(cat_id) + r'"',
            f'href="/Catalogo-digital-2026.html#{cat_id}"',
            text
        )
        text = re.sub(
            r'href="(?:https://www\.cyloguatemala\.me)?/?(?:\.\./|\.\/)?Catalogo-digital-2026(?:\.html)?\?cat=' + re.escape(cat_id) + r'"',
            f'href="/Catalogo-digital-2026.html#{cat_id}"',
            text
        )

    return text


def fix_related_product_links(text: str) -> str:
    """
    Mantiene corregido el problema del 404:
    /index.htmlproductos/slug -> /productos/slug.html
    """
    text = text.replace("https://www.cyloguatemala.me/index.htmlproductos/", "https://www.cyloguatemala.me/productos/")
    text = text.replace("/index.htmlproductos/", "/productos/")
    text = text.replace("../index.htmlproductos/", "/productos/")
    text = text.replace("./index.htmlproductos/", "/productos/")
    text = text.replace("index.htmlproductos/", "/productos/")

    # Si aparece /productos/slug sin .html en href, agregar .html salvo si ya termina con / o trae #/?
    def add_html(match):
        prefix = match.group(1)
        slug = match.group(2)
        suffix = match.group(3) or '"'

        if slug.endswith(".html"):
            return match.group(0)

        return f'{prefix}/productos/{slug}.html{suffix}'

    text = re.sub(
        r'(href=")(?:https://www\.cyloguatemala\.me)?/?productos/([^"#?]+?)(\.html)?(")',
        lambda m: f'{m.group(1)}/productos/{m.group(2)}.html{m.group(4)}' if not m.group(3) else m.group(0).replace('https://www.cyloguatemala.me', ''),
        text
    )

    return text


def patch_catalog(path: Path) -> bool:
    original = path.read_text(encoding="utf-8", errors="replace")
    text = original

    text = remove_old_category_code(text)
    text = fix_catalog_category_links(text)
    text = fix_related_product_links(text)

    if "CYLO RESET CATEGORÍAS V11" not in text:
        if "</head>" in text:
            text = text.replace("</head>", CATALOG_CSS + "\n</head>", 1)
        else:
            text = CATALOG_CSS + "\n" + text

    if "CYLO RESET CATEGORÍAS V11 - navegación limpia" not in text:
        idx = text.rfind("</body>")
        if idx != -1:
            text = text[:idx] + CATALOG_JS + "\n" + text[idx:]
        else:
            text += CATALOG_JS

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True

    return False


def patch_product_or_template(path: Path) -> bool:
    original = path.read_text(encoding="utf-8", errors="replace")
    text = original

    text = fix_product_category_links(text)
    text = fix_related_product_links(text)

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True

    return False


def main() -> None:
    changed = []

    catalog = ROOT / "Catalogo-digital-2026.html"
    if catalog.exists():
        if patch_catalog(catalog):
            changed.append(catalog)

    template = ROOT / "template.html"
    if template.exists():
        if patch_product_or_template(template):
            changed.append(template)

    # Fichas ya generadas
    for folder_name in ["productos", "productos_generados"]:
        folder = ROOT / folder_name
        if not folder.exists():
            continue

        for path in folder.rglob("*.html"):
            if patch_product_or_template(path):
                changed.append(path)

    print("CYLO RESET CATEGORÍAS V11 FINALIZADO")
    print(f"Archivos modificados: {len(changed)}")

    for path in changed:
        print(" -", path.relative_to(ROOT))

    print()
    print("Validación recomendada:")
    print("1. Abre /Catalogo-digital-2026.html")
    print("2. Haz clic en varias categorías seguidas.")
    print("3. La URL debe quedar como #cat-x, sin ?cat=")
    print("4. Desde una ficha de producto, una categoría debe abrir /Catalogo-digital-2026.html#cat-x")


if __name__ == "__main__":
    main()
