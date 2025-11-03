# Sistema de Envío de Correos Automático para Certificados

Sistema web (Flask) que notifica por correo a los asistentes cuando su certificado está listo para recojo físico. Incluye vista con tabla de asistentes, botón para enviar notificaciones pendientes y registro de envíos en una tabla de log.

## 📋 Características

- ✉️ Envío automático de correos electrónicos usando Gmail SMTP
- 📊 Panel de control con tabla de asistentes
- 🎯 Notificaciones solo para certificados con estado "Listo" no notificados
- 📝 Registro automático de notificaciones enviadas
- 🎨 Interfaz moderna y responsive
- 🔒 Conexión segura a base de datos MySQL

## 🛠️ Tecnologías Utilizadas

- **Backend**: Flask (Python)
- **Base de datos**: MySQL
- **Email**: SMTP de Gmail
- **Frontend**: HTML5, CSS3, Jinja2

## 📦 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/Yusurus/SystemaDeEnvioDeMensajesWeb.git
cd SystemaDeEnvioDeMensajesWeb
```

### 2. Crear entorno virtual (recomendado)

```bash
python -m venv venv
venv\Scripts\activate  # En Windows
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar base de datos

Usa MySQL con el siguiente modelo (según tu script):

```sql
CREATE SCHEMA IF NOT EXISTS `yusurus_enviar_email` DEFAULT CHARACTER SET utf8 ;
USE `yusurus_enviar_email` ;

CREATE TABLE IF NOT EXISTS `Eventos` (
    `idEvento` INT NOT NULL AUTO_INCREMENT,
    `nombre` VARCHAR(45) NOT NULL,
    `fecha` DATE NOT NULL,
    PRIMARY KEY (`idEvento`)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `Perticipantes` (
    `idPerticipante` INT NOT NULL AUTO_INCREMENT,
    `nombresCompleto` VARCHAR(60) NOT NULL,
    `correo` VARCHAR(45) NOT NULL,
    `estadoNotificado` ENUM('si', 'no') NOT NULL,
    `fk_idEvento` INT NOT NULL,
    PRIMARY KEY (`idPerticipante`),
    INDEX `fk_Perticipantes_Eventos_idx` (`fk_idEvento` ASC) VISIBLE,
    CONSTRAINT `fk_Perticipantes_Eventos`
        FOREIGN KEY (`fk_idEvento`) REFERENCES `Eventos` (`idEvento`)
        ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `Log_perticipantesNotificados` (
    `idLog_perticipanteNotificado` INT NOT NULL,
    `nombre` VARCHAR(45) NOT NULL,
    `correo` VARCHAR(45) NOT NULL,
    `fecha` DATETIME NOT NULL,
    `estadoAnterior` VARCHAR(45) NOT NULL,
    `estadoDespues` VARCHAR(45) NOT NULL,
    PRIMARY KEY (`idLog_perticipanteNotificado`)
) ENGINE=InnoDB;
```

### 5. Variables de entorno requeridas

La app lee TODA la configuración desde variables de entorno (no edites el código para credenciales):

Requeridas para MySQL:
- `DB_HOST` (p. ej. 127.0.0.1)
- `DB_PORT` (por defecto 3306)
- `DB_USER`
- `DB_PASSWORD`
- `DB_NAME` (p. ej. yusurus_enviar_email)

Requeridas para correo (Gmail SMTP):
- `GMAIL_USER` (tu correo Gmail)
- `GMAIL_APP_PASSWORD` (contraseña de aplicación de 16 caracteres)

Opcionales:
- `EMAIL_REMITENTE_REAL` (correo visible para Reply-To)
- `DIRECCION_RECOJO` (texto que se incluye en el correo)
- `FLASK_SECRET_KEY` (si no se define, se usa una clave de ejemplo solo para desarrollo)

En Windows (cmd.exe) puedes exportarlas temporalmente así:

```bat
set DB_HOST=127.0.0.1
set DB_PORT=3306
set DB_USER=tu_usuario
set DB_PASSWORD=tu_password
set DB_NAME=yusurus_enviar_email

set GMAIL_USER=tu_correo@gmail.com
set GMAIL_APP_PASSWORD=tu_contrasena_app

set EMAIL_REMITENTE_REAL=correo-institucional@tu-dominio.com
set DIRECCION_RECOJO=Av. Siempre Viva 123, Lima
set FLASK_SECRET_KEY=clave-secreta-dev
```

> ⚠️ **IMPORTANTE**: Para usar Gmail, necesitas generar una "Contraseña de Aplicación":
> 1. Ve a tu cuenta de Google
> 2. Seguridad → Verificación en 2 pasos (actívala si no la tienes)
> 3. Contraseñas de aplicaciones
> 4. Genera una nueva contraseña de 16 caracteres
> 5. Úsala en `GMAIL_APP_PASSWORD`

## 🚀 Uso

### Iniciar el servidor

```bat
python app.py
```

La aplicación estará disponible en `http://127.0.0.1:5000`

### Flujo de trabajo

1. **Accede al panel de control** en la página principal
2. **Revisa la tabla** de asistentes y su estado de certificados
3. **Presiona el botón** "Enviar Notificaciones Pendientes"
4. El sistema enviará correos solo a asistentes con `estadoNotificado = 'no'`
5. Después del envío, se actualiza a `estadoNotificado = 'si'` y se guarda un registro en `Log_perticipantesNotificados`

## 📁 Estructura del Proyecto

```
SystemaDeEnvioDeMensajesWeb/
│
├── app.py                 # Aplicación Flask (Controlador)
├── database.py            # Conexión y consultas MySQL (Modelo)
├── email_sender.py        # Lógica de envío de correos (Servicio)
├── requirements.txt       # Dependencias
├── README.md             # Este archivo
│
├── static/
│   └── style.css         # Estilos CSS
│
└── templates/
    ├── base.html         # Plantilla base
    └── index.html        # Página principal
```

## 🎨 Arquitectura MVC

- **Modelo** (`database.py`): Gestión de datos y consultas SQL
- **Vista** (`templates/`): Interfaz HTML con Jinja2
- **Controlador** (`app.py`): Lógica de rutas y flujo de datos
- **Servicio** (`email_sender.py`): Envío de correos

## 🔧 Funciones Principales

### database.py

- `obtener_todos_los_asistentes()`: Lista todos con su evento y estado
- `obtener_asistentes_para_notificar()`: Solo con `estadoNotificado = 'no'`
- `marcar_asistente_como_notificado(id)`: Actualiza a `'si'` e inserta en log

### email_sender.py

- `enviar_correo(email, nombre, evento)`: Envía correo personalizado (texto + HTML)

### app.py

- Ruta `/`: Muestra panel con tabla de asistentes
- Ruta `/enviar-notificaciones`: Procesa envío masivo

## 🐛 Solución de Problemas

### Error de conexión a MySQL
- Verifica variables de entorno `DB_*`
- Asegúrate de que el servidor MySQL esté corriendo
- Revisa que el host y puerto sean correctos

### Error al enviar correos
- Verifica que hayas activado "Verificación en 2 pasos" en Google
- Usa una "Contraseña de Aplicación", no tu contraseña normal
- Verifica que `GMAIL_USER` y `GMAIL_APP_PASSWORD` sean correctos

### El botón aparece deshabilitado
- Se deshabilita si no hay asistentes con `estadoNotificado = 'no'` en la lista

### La tabla no muestra datos
- Verifica que haya datos en la base de datos
- Revisa la consola de Flask para errores de consultas SQL

## 📝 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 👨‍💻 Autor

**Yusurus**
- GitHub: [@Yusurus](https://github.com/Yusurus)

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Haz fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

⭐ Si este proyecto te fue útil, ¡considera darle una estrella en GitHub!
