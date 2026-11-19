# 🎬 Página de Películas — Catálogo Web (Sprint 1)

Aplicación web desarrollada en **Django 5.2** para la gestión y catalogación de películas organizadas por categoría/género. Este documento detalla la arquitectura del proyecto, el diccionario de datos correspondiente al **Sprint 1** y la guía de instalación local.

---

## 🏗️ 1. Arquitectura del Proyecto

El proyecto sigue el patrón arquitectónico **MVT (Model-View-Template)** propio de Django, separando la configuración global del proyecto de la lógica de negocio de la aplicación principal.

### Tecnologías Utilizadas
* **Lenguaje:** Python 3.x
* **Framework Web:** Django `5.2`
* **Base de Datos:** SQLite 3 (`db.sqlite3` en entorno local)
* **Dependencias adicionales:** Pillow `13.0.0`
* **Control de Versiones:** Git & GitHub (flujo por ramas y Pull Requests)

### Estructura de Directorios
```text
Pagina_de_peliculas/
├── gestion/                     # Aplicación principal del catálogo
│   ├── migrations/              # Historial de migraciones de la base de datos
│   ├── admin.py                 # Registro de modelos en el panel administrativo
│   ├── apps.py                  # Configuración de la app 'gestion'
│   ├── models.py                # Definición de modelos (Categoria, Pelicula)
│   ├── tests.py                 # Pruebas unitarias
│   ├── urls.py                  # Enrutamiento de URLs de la app
│   └── views.py                 # Lógica de controladores/vistas
├── pagina_de_peliculas/         # Paquete de configuración raíz del proyecto
│   ├── asgi.py                  # Punto de entrada ASGI
│   ├── settings.py              # Configuración general, apps instaladas y BD
│   ├── urls.py                  # Enrutamiento principal de URLs
│   └── wsgi.py                  # Punto de entrada WSGI
├── .gitignore                   # Exclusión de entorno virtual (venv) y db.sqlite3
├── manage.py                    # Utilidad de línea de comandos de Django
├── registros_tarea4.json        # Fixture con los registros iniciales del catálogo
└── README.md                    # Documentación de arquitectura y diccionario de datos
