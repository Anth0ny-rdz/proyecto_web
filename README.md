# proyecto_web

# Core Web Frutas
Este proyecto consiste en desarrollar una tienda en línea de frutas, . La plataforma
permitirá a los usuarios navegar por una amplia variedad de frutas frescas y otros
productos naturales, comprar en línea, y recibir entregas en sus hogares o realizar
pedidos para recoger en tienda. Los usuarios podrán ver descripciones detalladas de
los productos, agregar artículos a un carrito de compras, realizar pagos seguros en línea
y recibir notificaciones de entrega. Además, el sistema estará optimizado tanto para
dispositivos móviles como de escritorio, mejorando la accesibilidad y la experiencia de
usuario.
2.-Explicación del Cores.
El Core de este proyecto estará centrado en la gestión de productos (frutas), el manejo
del carrito de compras y el sistema de inventario, así como en la integración de pagos y
el seguimiento de pedidos. Esto implica que las funcionalidades principales serán las
siguientes:
1. Gestión de productos: Los administradores podrán agregar, editar, y eliminar
productos de la tienda, asignando categorías (frutas tropicales, de temporada,
etc.), precios y descripciones.
2. Manejo del inventario: El sistema controlará las cantidades disponibles en
stock y emitirá alertas cuando ciertas frutas estén agotadas o próximas a
agotarse. También permitirá gestionar variaciones de productos, como frutas
orgánicas o convencionales.
3. Carrito de compras: Los usuarios podrán agregar frutas al carrito, calcular el
costo total (incluyendo impuestos y envío), y proceder al pago.
4. Sistema de pago seguro: Integración con pasarelas de pago para procesar
transacciones de manera segura, con soporte para múltiples métodos de pago,
como tarjetas de crédito/débito y plataformas de pago en línea.
5. Seguimiento de pedidos: Una vez completada la compra, los usuarios podrán
seguir el estado de sus pedidos, desde la confirmación hasta la entrega
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

