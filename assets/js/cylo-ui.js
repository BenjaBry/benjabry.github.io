// CYLO Unified Header/Nav
// Versión local para páginas ubicadas en la raíz del proyecto: index.html y Catalogo-digital-2026.html.

(function () {
  const mount = document.getElementById("cylo-header");
  if (!mount) return;

  const active = (mount.dataset.active || "").toLowerCase();

  const categories = [
    ["Desechables", "76", "cat-desechables"],
    ["Utensilios", "136", "cat-utensilios"],
    ["Cocción", "34", "cat-cocci-n"],
    ["Accesorios", "59", "cat-accesorios"],
    ["Repostería", "59", "cat-reposter-a"],
    ["Pizzería", "16", "cat-pizzer-a"],
    ["Contenedores", "38", "cat-contenedores"],
    ["Catering", "84", "cat-catering"],
    ["Servicio", "96", "cat-servicio"],
    ["Bartender", "77", "cat-bartender"],
    ["Cafetería", "48", "cat-cafeter-a"],
    ["Presentación", "17", "cat-presentaci-n"],
    ["Vajilla", "108", "cat-vajilla"],
    ["Cristalería", "123", "cat-cristaler-a"]
  ];

  const base = "";
  const catalogUrl = `/Catalogo-digital-2026.html`;

  const activeClass = (key) => active === key ? "is-active" : "";

  const categoryLinks = categories.map(([name, count, anchor]) => `
    <a href="${catalogUrl}#${anchor}">
      <span>${name}</span>
      <small>${count}</small>
    </a>
  `).join("");

  mount.innerHTML = `
    <div class="cylo-shell">
      <div class="cylo-top-bar">
        <div class="cylo-container cylo-top-bar-inner">
          <div><strong>CYLO Guatemala</strong> | Insumos para alimentos y compras institucionales</div>
          <div>WhatsApp: +502 4054-5591 | ventas@cyloguatemala.me</div>
        </div>
      </div>

      <header class="cylo-header">
        <div class="cylo-container cylo-header-main">
          <a href="/index.html" class="cylo-logo" aria-label="CYLO Guatemala">
            <div class="cylo-logo-main">CY<em>LO</em></div>
            <div class="cylo-logo-sub">Guatemala</div>
          </a>

          <form class="cylo-search" id="cyloGlobalSearch" action="${catalogUrl}">
            <input type="search" name="q" placeholder="Buscar productos, empaques, insumos o categorías">
            <button type="submit">Buscar</button>
          </form>

          <div class="cylo-header-actions">
            <a href="/contacto.html">Contacto</a>
            <a class="cylo-whatsapp" href="https://wa.me/50240545591?text=Hola%20CYLO,%20quiero%20cotizar%20productos%20para%20mi%20negocio." target="_blank" rel="noopener">Cotizar</a>
          </div>
        </div>

        <nav class="cylo-main-menu" aria-label="Navegación principal">
          <div class="cylo-container cylo-menu-inner">
            <a href="/index.html" class="${activeClass("inicio")}">Inicio</a>
            <a href="${catalogUrl}" class="${activeClass("catalogo")}">Catálogo completo</a>

            <details class="cylo-dropdown">
              <summary>Categorías</summary>
              <div class="cylo-dropdown-panel">
                ${categoryLinks}
              </div>
            </details>

<a href="/blog/index.html" class="${activeClass("blog")}">Blog</a>
<a href="/nosotros.html" class="${activeClass("nosotros")}">Nosotros</a>
<a href="/contacto.html" class="${activeClass("contacto")}">Contacto</a>
          </div>
        </nav>
      </header>
    </div>
  `;

  const search = mount.querySelector("#cyloGlobalSearch");
  if (search) {
    search.addEventListener("submit", function (event) {
      const input = search.querySelector('input[name="q"]');
      const query = input ? input.value.trim() : "";

      if (!query) return;

      event.preventDefault();
      window.location.href = `/Catalogo-digital-2026.html?q=${encodeURIComponent(query)}#catalog-search`;
    });
  }

  const dropdown = mount.querySelector(".cylo-dropdown");
  if (dropdown) {
    document.addEventListener("click", function (event) {
      if (!dropdown.contains(event.target)) {
        dropdown.removeAttribute("open");
      }
    });

    dropdown.querySelectorAll("a").forEach(link => {
      link.addEventListener("click", function () {
        dropdown.removeAttribute("open");
      });
    });
  }
})();
