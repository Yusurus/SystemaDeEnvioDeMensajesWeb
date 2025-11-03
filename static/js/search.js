// Utilidad: debounce para evitar filtrar en cada tecla inmediatamente
function debounce(fn, delay) {
  var t;
  return function () {
    var ctx = this, args = arguments;
    clearTimeout(t);
    t = setTimeout(function () { fn.apply(ctx, args); }, delay);
  };
}

function updateExportLink(query) {
  var link = document.getElementById('exportar-excel');
  if (!link) return;
  try {
    var url = new URL(link.href, window.location.origin);
    if (query) {
      url.searchParams.set('search_name', query);
    } else {
      url.searchParams.delete('search_name');
    }
    link.href = url.toString();
  } catch (e) {
    // Fallback si URL() falla por href relativo
    var baseHref = link.getAttribute('href');
    var sep = baseHref.indexOf('?') === -1 ? '?' : '&';
    link.setAttribute('href', baseHref.split('?')[0] + (query ? sep + 'search_name=' + encodeURIComponent(query) : ''));
  }
}

function filterReportes(query) {
  var table = document.getElementById('tabla-reportes');
  var emptyMsg = document.getElementById('no-resultados');
  var emptyText = document.getElementById('nores-q');
  if (!table) return;

  var q = (query || '').trim().toLowerCase();
  var rows = table.querySelectorAll('tbody tr');
  var anyVisible = false;

  rows.forEach(function (row) {
    var nameCell = row.querySelector('.col-nombre');
    var text = (nameCell ? nameCell.textContent : row.textContent) || '';
    var match = text.toLowerCase().indexOf(q) !== -1;
    row.style.display = match ? '' : 'none';
    if (match) anyVisible = true;
  });

  // Mostrar/ocultar tabla y mensaje vacío
  if (rows.length) {
    table.style.display = anyVisible ? '' : 'none';
    if (emptyMsg) {
      emptyMsg.style.display = anyVisible ? 'none' : '';
      if (emptyText) emptyText.textContent = query || '';
    }
  }
}

function setupLiveSearch() {
  var input = document.getElementById('search_name');
  if (!input) return;

  var handler = debounce(function () {
    var q = input.value || '';
    filterReportes(q);
    updateExportLink(q);
  }, 250);

  input.addEventListener('input', handler);
}

// Inicializar al cargar el DOM
document.addEventListener('DOMContentLoaded', function () {
  setupLiveSearch();
});
