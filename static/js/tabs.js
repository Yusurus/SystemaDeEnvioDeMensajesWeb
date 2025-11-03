function openTab(tabName) {
  var i, tabcontent, tabbuttons;

  // Ocultar todos los contenidos de las pestañas
  tabcontent = document.getElementsByClassName("tab-pane");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Quitar la clase "active" de todos los botones
  tabbuttons = document.getElementsByClassName("tab-button");
  for (i = 0; i < tabbuttons.length; i++) {
    tabbuttons[i].classList.remove("active");
  }

  // Mostrar la pestaña actual
  var tabToShow = document.getElementById(tabName);
  if (tabToShow) {
    tabToShow.style.display = "block";
  }

  // Añadir la clase "active" al botón que abrió la pestaña
  var buttons = document.getElementsByClassName("tab-button");
  for (i = 0; i < buttons.length; i++) {
    if (buttons[i].getAttribute("onclick") === "openTab('" + tabName + "')") {
      buttons[i].classList.add("active");
    }
  }
}

// Abrir la pestaña por defecto proveniente del atributo data-active-tab del <body>
document.addEventListener("DOMContentLoaded", function () {
  var defaultTab = document.body.getAttribute("data-active-tab") || "notificar";
  openTab(defaultTab);
});
