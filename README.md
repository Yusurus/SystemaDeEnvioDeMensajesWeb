# Sistema de Envío de Correos Automático para Certificados

Sistema web desarrollado en Flask para notificar automáticamente a los asistentes cuando sus certificados de eventos están listos para recoger.

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

Asegúrate de tener una base de datos MySQL con las siguientes tablas:

```sql
CREATE TABLE Eventos (
    id_evento INT PRIMARY KEY AUTO_INCREMENT,
    nombre_evento VARCHAR(255) NOT NULL
);

CREATE TABLE Asistentes (
    id_asistente INT PRIMARY KEY AUTO_INCREMENT,
    nombre_completo VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    id_evento_fk INT,
    estado_certificado ENUM('Pendiente', 'En Proceso', 'Listo') DEFAULT 'Pendiente',
    notificado TINYINT(1) DEFAULT 0,
    FOREIGN KEY (id_evento_fk) REFERENCES Eventos(id_evento)
);
```

### 5. Configurar credenciales

**En `database.py`**, actualiza las credenciales de tu base de datos:

```python
DB_HOST = "tu-host-mysql"
DB_USER = "tu-usuario"
DB_PASSWORD = "tu-contraseña"
DB_NAME = "tu-base-datos"
```

**En `email_sender.py`**, configura tu cuenta de Gmail:

```python
GMAIL_USER = "tu-email@gmail.com"
GMAIL_APP_PASSWORD = "tu-contraseña-aplicacion"  # ⚠️ No uses tu contraseña normal
EMAIL_REMITENTE_REAL = "correo-institucional@universidad.edu"
DIRECCION_RECOJO = "Tu dirección de recojo"
```

> ⚠️ **IMPORTANTE**: Para usar Gmail, necesitas generar una "Contraseña de Aplicación":
> 1. Ve a tu cuenta de Google
> 2. Seguridad → Verificación en 2 pasos (actívala si no la tienes)
> 3. Contraseñas de aplicaciones
> 4. Genera una nueva contraseña de 16 caracteres
> 5. Úsala en `GMAIL_APP_PASSWORD`

## 🚀 Uso

### Iniciar el servidor

```bash
python app.py
```

La aplicación estará disponible en `http://127.0.0.1:5000`

### Flujo de trabajo

1. **Accede al panel de control** en la página principal
2. **Revisa la tabla** de asistentes y su estado de certificados
3. **Presiona el botón** "Enviar Notificaciones Pendientes"
4. El sistema enviará correos solo a asistentes con:
   - `estado_certificado = 'Listo'`
   - `notificado = 0`
5. Después del envío, se marca automáticamente `notificado = 1`

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

- `get_db_connection()`: Establece conexión con MySQL
- `obtener_asistentes_para_notificar()`: Lista asistentes pendientes de notificar
- `marcar_asistente_como_notificado(id)`: Marca como notificado
- `obtener_todos_los_asistentes()`: Obtiene todos para la tabla

### email_sender.py

- `enviar_correo(email, nombre, evento)`: Envía correo personalizado

### app.py

- Ruta `/`: Muestra panel con tabla de asistentes
- Ruta `/enviar-notificaciones`: Procesa envío masivo

## 🐛 Solución de Problemas

### Error de conexión a MySQL
- Verifica las credenciales en `database.py`
- Asegúrate de que el servidor MySQL esté corriendo
- Revisa que el host y puerto sean correctos

### Error al enviar correos
- Verifica que hayas activado "Verificación en 2 pasos" en Google
- Usa una "Contraseña de Aplicación", no tu contraseña normal
- Verifica que `GMAIL_USER` y `GMAIL_APP_PASSWORD` sean correctos

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
