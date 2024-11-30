# proyecto_web

# Proyecto_Web

Este repositorio contiene el código fuente para un proyecto que incluye un backend en Python y un frontend con herramientas basadas en Node.js.

## Requisitos

- Python 3.8 o superior
- Node.js y npm instalados
- Entorno Windows para los comandos descritos (pueden adaptarse a otros entornos)

---

## Instalación

### 1. Clonar el repositorio
```bash
python -m venv venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\activate

pip install -r requirements.txt

cd frontend

npm install

git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_REPOSITORIO>
# Proyecto: Aplicación Web Full Stack

Este repositorio contiene el código fuente de una aplicación web Full Stack con un backend desarrollado en Django y un frontend basado en React (Node.js). 

## Estructura del proyecto

```plaintext
.
├── backend/            # Código del servidor backend (Django)
│   ├── __init__.py
│   ├── asgi.py         # Configuración ASGI
│   ├── settings.py     # Configuración del proyecto Django
│   ├── urls.py         # Enrutamiento del backend
│   ├── wsgi.py         # Configuración WSGI
│   └── tienda/         # Aplicación principal
│       ├── migrations/ # Migraciones de la base de datos
│       ├── admin.py    # Configuración del panel de administración
│       ├── apps.py     # Configuración de la aplicación Django
│       ├── models.py   # Modelos de base de datos
│       ├── serializers.py # Serializadores para APIs
│       ├── tests.py    # Pruebas automatizadas
│       ├── urls.py     # Enrutamiento de la aplicación
│       └── views.py    # Lógica de las vistas
├── db.sqlite3          # Base de datos SQLite
├── manage.py           # Script principal para tareas de Django
├── frontend/           # Código del frontend (React)
│   ├── node_modules/   # Dependencias de Node.js
│   ├── public/         # Archivos públicos del frontend
│   ├── src/            # Código fuente de React
│   ├── package.json    # Configuración de dependencias del frontend
│   ├── package-lock.json # Bloqueo de versiones de dependencias
│   └── README.md       # Documentación del frontend
└── requirements.txt    # Dependencias del backend

