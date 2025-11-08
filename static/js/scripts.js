// ===== Sistema de Notificación de Certificados - JavaScript =====

// Variable global para las escuelas
const allEscuelas = window.escuelasData || [];

// Variable global para las tablas DataTables
var dataTables = {};

/**
 * Actualiza el dropdown de escuelas basado en la facultad seleccionada
 * @param {string} selectedFacultadId - ID de la facultad seleccionada
 * @param {string} targetEscuelaDropdownId - ID del dropdown de escuelas a actualizar
 */
function updateEscuelas(selectedFacultadId, targetEscuelaDropdownId) {
    const escuelaDropdown = document.getElementById(targetEscuelaDropdownId);
    
    if (!escuelaDropdown) {
        console.error(`No se encontró el dropdown con ID: ${targetEscuelaDropdownId}`);
        return;
    }
    
    // Limpiar opciones existentes
    escuelaDropdown.innerHTML = '';
    
    // Agregar opción por defecto
    const defaultOption = document.createElement('option');
    defaultOption.value = "";
    defaultOption.textContent = "-- Ninguna --";
    escuelaDropdown.appendChild(defaultOption);
    
    // Si no hay facultad seleccionada, deshabilitar el dropdown
    if (!selectedFacultadId || selectedFacultadId === "") {
        escuelaDropdown.disabled = true;
        return;
    }
    
    // Filtrar y agregar escuelas de la facultad seleccionada
    allEscuelas.forEach(escuela => {
        if (escuela.fk_idFacultad && escuela.fk_idFacultad.toString() === selectedFacultadId) {
            const option = document.createElement('option');
            option.value = escuela.idEscuela;
            option.textContent = escuela.nombreEscuela;
            escuelaDropdown.appendChild(option);
        }
    });
    
    // Habilitar el dropdown
    escuelaDropdown.disabled = false;
}

/**
 * Cambia entre pestañas
 * @param {string} tabName - Nombre de la pestaña a mostrar
 */
function openTab(tabName) {
    // Ocultar todos los tab-panes
    const tabPanes = document.getElementsByClassName("tab-pane");
    for (let i = 0; i < tabPanes.length; i++) {
        tabPanes[i].style.display = "none";
    }
    
    // Remover clase active de todos los botones
    const tabButtons = document.getElementsByClassName("tab-button");
    for (let i = 0; i < tabButtons.length; i++) {
        tabButtons[i].classList.remove("active");
    }
    
    // Mostrar el tab seleccionado
    const tabToShow = document.getElementById(tabName);
    if (tabToShow) {
        tabToShow.style.display = "block";
    } else {
        console.error(`No se encontró la pestaña: ${tabName}`);
    }
    
    // Activar el botón correspondiente
    for (let i = 0; i < tabButtons.length; i++) {
        const onclickAttr = tabButtons[i].getAttribute("onclick");
        if (onclickAttr && onclickAttr.includes(tabName)) {
            tabButtons[i].classList.add("active");
            break;
        }
    }
    
    // Ajustar columnas de las tablas DataTables cuando se cambia de pestaña
    adjustDataTableColumns(tabName);
}

/**
 * Ajusta las columnas de DataTables según la pestaña activa
 * @param {string} tabName - Nombre de la pestaña activa
 */
function adjustDataTableColumns(tabName) {
    switch(tabName) {
        case 'notificar':
            if (dataTables.notificar) {
                dataTables.notificar.columns.adjust();
            }
            break;
            
        case 'reporte-general':
            if (dataTables.reporteGeneral) {
                dataTables.reporteGeneral.columns.adjust().draw();
            }
            break;
            
        case 'vistas':
            if (dataTables.eventos) {
                dataTables.eventos.columns.adjust().draw();
            }
            if (dataTables.participantes) {
                dataTables.participantes.columns.adjust().draw();
            }
            break;
    }
}

/**
 * Inicializa todas las tablas DataTables
 */
function initializeDataTables() {
    const spanishLang = {
        "url": "//cdn.datatables.net/plug-ins/1.13.6/i18n/es-ES.json"
    };
    
    // Tabla Notificar
    const tablaNotificar = $('#tablaNotificar');
    if (tablaNotificar.length) {
        dataTables.notificar = tablaNotificar.DataTable({
            language: spanishLang,
            responsive: true,
            pageLength: 10,
            order: [[0, 'asc']]
        });
    }
    
    // Tabla Reporte General
    const tablaReporteGeneral = $('#tablaReporteGeneral');
    if (tablaReporteGeneral.length) {
        dataTables.reporteGeneral = tablaReporteGeneral.DataTable({
            language: spanishLang,
            scrollX: true,
            pageLength: 25,
            order: [[0, 'asc']]
        });
    }
    
    // Tabla Eventos (Vista)
    const tablaEventos = $('#tablaEventos');
    if (tablaEventos.length) {
        dataTables.eventos = tablaEventos.DataTable({
            language: spanishLang,
            scrollX: true,
            pageLength: 10,
            order: [[1, 'desc']] // Ordenar por fecha descendente
        });
    }
    
    // Tabla Participantes (Vista)
    const tablaParticipantes = $('#tablaParticipantes');
    if (tablaParticipantes.length) {
        dataTables.participantes = tablaParticipantes.DataTable({
            language: spanishLang,
            scrollX: true,
            pageLength: 25,
            order: [[0, 'asc']]
        });
    }
}

/**
 * Valida el formulario de agregar participante
 * @param {Event} e - Evento del formulario
 */
function validateParticipantForm(e) {
    const nombres = document.getElementById('nombres_participante');
    const correo = document.getElementById('correo_participante');
    const eventoId = document.getElementById('evento_id');
    
    if (!nombres.value.trim()) {
        alert('Por favor, ingresa el nombre del participante.');
        e.preventDefault();
        return false;
    }
    
    if (!correo.value.trim() || !correo.validity.valid) {
        alert('Por favor, ingresa un correo electrónico válido.');
        e.preventDefault();
        return false;
    }
    
    if (!eventoId.value) {
        alert('Por favor, selecciona un evento.');
        e.preventDefault();
        return false;
    }
    
    return true;
}

/**
 * Valida el formulario de agregar evento
 * @param {Event} e - Evento del formulario
 */
function validateEventForm(e) {
    const nombre = document.getElementById('nombre_evento');
    const fecha = document.getElementById('fecha_evento');
    
    if (!nombre.value.trim()) {
        alert('Por favor, ingresa el nombre del evento.');
        e.preventDefault();
        return false;
    }
    
    if (!fecha.value) {
        alert('Por favor, selecciona la fecha del evento.');
        e.preventDefault();
        return false;
    }
    
    return true;
}

/**
 * Confirma el envío de notificaciones
 * @param {Event} e - Evento del formulario
 */
function confirmSendNotifications(e) {
    const count = document.querySelector('[type="submit"]').textContent.match(/\d+/);
    if (count) {
        const message = `¿Estás seguro de que deseas notificar a ${count[0]} participante(s)?`;
        if (!confirm(message)) {
            e.preventDefault();
            return false;
        }
    }
    return true;
}

/**
 * Inicialización cuando el DOM está listo
 */
$(document).ready(function() {
    // Inicializar todas las tablas DataTables
    initializeDataTables();
    
    // Obtener la pestaña activa del atributo data o usar 'notificar' por defecto
    const activeTab = document.body.getAttribute('data-active-tab') || 'notificar';
    openTab(activeTab);
    
    // Agregar eventos de validación a los formularios
    const participantForm = document.querySelector('form[action*="add-participant"]');
    if (participantForm) {
        participantForm.addEventListener('submit', validateParticipantForm);
    }
    
    const eventForm = document.querySelector('form[action*="add-event"]');
    if (eventForm) {
        eventForm.addEventListener('submit', validateEventForm);
    }
    
    const notificationForm = document.querySelector('form[action*="enviar-notificaciones"]');
    if (notificationForm) {
        notificationForm.addEventListener('submit', confirmSendNotifications);
    }
    
    // Auto-cerrar mensajes flash después de 5 segundos
    setTimeout(function() {
        $('.flash').fadeOut('slow', function() {
            $(this).remove();
        });
    }, 5000);
    
    console.log('Sistema de Notificación inicializado correctamente');
});

// Exponer funciones globalmente para uso en el HTML
window.updateEscuelas = updateEscuelas;
window.openTab = openTab;
