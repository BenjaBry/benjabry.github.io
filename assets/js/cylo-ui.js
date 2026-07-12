// CYLO Unified Header/Nav
// Versión local para páginas ubicadas en la raíz del proyecto: index.html y Catalogo-digital-2026.html.

(function () {
  const mount = document.getElementById("cylo-header");
  if (!mount) return;

  const active = (mount.dataset.active || "").toLowerCase();
  const isPurificadores = active === "purificadores";
  const logoUrl = isPurificadores ? "purificadores-agua.html" : "index.html";
  const logoText = isPurificadores ? "Aqua<em>Pure</em>" : "CY<em>LO</em>";
  const logoStyle = isPurificadores ? "style=\"color: #1768D3;\"" : "";
  const subStyle = isPurificadores ? "style=\"color: #5AC8F2;\"" : "";

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
  const catalogUrl = `Catalogo-digital-2026.html`;

  const activeClass = (key) => active === key ? "is-active" : "";

  const categoryLinks = categories.map(([name, count, anchor]) => `
    <a href="${catalogUrl}#${anchor}">
      <span>${name}</span>
      <small>${count}</small>
    </a>
  `).join("");

  const topBarMarkup = isPurificadores ? `
    <div class="cylo-top-bar" style="background: var(--navy2);">
      <div class="cylo-container cylo-top-bar-inner">
        <div><strong>AquaPure Guatemala</strong> | Purificadores y filtros de agua pura de alto rendimiento</div>
        <div>WhatsApp: +502 3443-1638 | ventas@cyloguatemala.me</div>
      </div>
    </div>
  ` : `
    <div class="cylo-top-bar">
      <div class="cylo-container cylo-top-bar-inner">
        <div><strong>CYLO Guatemala</strong> | Insumos para alimentos y compras institucionales</div>
        <div>WhatsApp: +502 4054-5591 | ventas@cyloguatemala.me</div>
      </div>
    </div>
  `;

  const searchMarkup = isPurificadores ? `
    <div style="flex: 1;"></div>
  ` : `
    <form class="cylo-search" id="cyloGlobalSearch" action="${catalogUrl}">
      <input type="search" name="q" placeholder="Buscar productos, empaques, insumos o categorías">
      <button type="submit">Buscar</button>
    </form>
  `;

  const actionsMarkup = isPurificadores ? `
    <div class="cylo-header-actions">
      <a href="index.html" style="margin-right: 12px; font-weight: 800; color: var(--navy); text-decoration: none;">Volver a CYLO</a>
      <a class="cylo-whatsapp" href="https://wa.me/50234431638?text=Hola%20AquaPure,%20quiero%20cotizar%20un%20purificador%20de%20agua." target="_blank" rel="noopener" style="background: #1768D3; border-radius: 4px; color: white !important; padding: 11px 16px; text-decoration: none;">WhatsApp Ventas</a>
    </div>
  ` : `
    <div class="cylo-header-actions">
      <a href="contacto.html">Contacto</a>
      <a class="cylo-whatsapp" href="https://wa.me/50240545591?text=Hola%20CYLO,%20quiero%20cotizar%20productos%20para%20mi%20negocio." target="_blank" rel="noopener">Cotizar</a>
    </div>
  `;

  const menuMarkup = isPurificadores ? `
    <a href="purificadores-agua.html" class="is-active">Inicio Purificadores</a>
    <a href="purificadores-agua.html#catalogo">Modelos</a>
    <a href="purificadores-agua.html#calculadora">Calculadora de Ahorro</a>
    <a href="purificadores-agua.html#proceso">¿Cómo comprar?</a>
    <a href="index.html" class="back-to-cylo" style="margin-left: auto; border-right: none; background: rgba(255,255,255,0.08);">← Volver a CYLO</a>
  ` : `
    <a href="index.html" class="${activeClass("inicio")}">Inicio</a>
    <a href="${catalogUrl}" class="${activeClass("catalogo")}">Catálogo completo</a>
    <a href="purificadores-agua.html" class="${activeClass("purificadores")}">Purificadores</a>

    <details class="cylo-dropdown">
      <summary>Categorías</summary>
      <div class="cylo-dropdown-panel">
        ${categoryLinks}
      </div>
    </details>

    <a href="blog/index.html" class="${activeClass("blog")}">Blog</a>
    <a href="nosotros.html" class="${activeClass("nosotros")}">Nosotros</a>
    <a href="contacto.html" class="${activeClass("contacto")}">Contacto</a>
  `;

  mount.innerHTML = `
    <div class="cylo-shell">
      ${topBarMarkup}

      <header class="cylo-header">
        <div class="cylo-container cylo-header-main">
          <a href="${logoUrl}" class="cylo-logo" aria-label="${isPurificadores ? "AquaPure" : "CYLO"} Guatemala">
            <div class="cylo-logo-main" ${logoStyle}>${logoText}</div>
            <div class="cylo-logo-sub" ${subStyle}>Guatemala</div>
          </a>

          ${searchMarkup}
          ${actionsMarkup}
        </div>

        <nav class="cylo-main-menu" aria-label="Navegación principal">
          <div class="cylo-container cylo-menu-inner">
            ${menuMarkup}
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
      window.location.href = `Catalogo-digital-2026.html?q=${encodeURIComponent(query)}#catalog-search`;
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
