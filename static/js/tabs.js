/**
 * Sistema de pestañas con Bootstrap 5
 */
function openTab(tabName) {
  // Ocultar todos los contenidos de las pestañas
  var tabcontent = document.getElementsByClassName("tab-pane");
  for (var i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
    tabcontent[i].classList.remove("active");
  }

  // Quitar la clase "active" de todos los botones
  var tabbuttons = document.getElementsByClassName("nav-link");
  for (var i = 0; i < tabbuttons.length; i++) {
    tabbuttons[i].classList.remove("active");
  }

  // Mostrar la pestaña actual
  var tabToShow = document.getElementById(tabName);
  if (tabToShow) {
    tabToShow.style.display = "block";
    tabToShow.classList.add("active");
  }

  // Añadir la clase "active" al botón que abrió la pestaña
  var currentTabButton = document.getElementById("tab-" + tabName);
  if (currentTabButton) {
    currentTabButton.classList.add("active");
  }
}

// Abrir la pestaña por defecto proveniente del atributo data-active-tab del <body>
document.addEventListener("DOMContentLoaded", function () {
  var defaultTab = document.body.getAttribute("data-active-tab") || "notificar";
  openTab(defaultTab);
});
