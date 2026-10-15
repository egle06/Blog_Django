# Mi Blog con Django

Proyecto integrador: un blog hecho con Django. En esta etapa (Preentrega 8) el sitio pasó de responder texto plano a mostrar páginas HTML con herencia de templates, navegación, estilos CSS y JavaScript.

## Qué incluye

- Página de **Inicio** con título y mensaje de bienvenida.
- Página **Acerca de** con una reseña del autor y el propósito del sitio.
- Página de **Posts** con un listado de publicaciones de ejemplo.
- Página de **detalle** de cada post (título, autor y contenido).
- Menú de navegación entre las páginas.
- Layout base reutilizable (`base.html`) con herencia de templates.
- Archivos estáticos: CSS, JavaScript y logo.

> Los posts son datos de ejemplo definidos como una lista de diccionarios en `views.py`. Todavía no se usa base de datos; eso se incorporará en módulos futuros.

## Flujo de Django aplicado

```
Ruta -> Vista -> Template -> Estático
```

1. La URL se define en `posts/urls.py` y se conecta con `include()` desde `blog_project/urls.py`.
2. La vista (`posts/views.py`) usa `render()` para devolver el template.
3. El template hereda de `base.html` con `{% extends %}`.
4. `base.html` carga CSS, JS y logo con `{% load static %}` y `{% static %}`.

## Estructura del proyecto

```
blog_django/
├── manage.py
├── README.md
├── requirements.txt
├── blog_project/
│   ├── settings.py
│   ├── urls.py
│   └── ...
└── posts/
    ├── views.py
    ├── urls.py
    ├── templates/
    │   └── posts/
    │       ├── base.html
    │       ├── inicio.html
    │       ├── acerca.html
    │       ├── lista_posts.html
    │       └── detalle_post.html
    └── static/
        └── posts/
            ├── css/estilos.css
            ├── js/main.js
            └── img/logo.jpg
```

## Rutas

| URL              | Vista                | Nombre          |
|------------------|----------------------|-----------------|
| `/`              | `views.inicio`       | `inicio`        |
| `/acerca/`       | `views.acerca`       | `acerca`        |
| `/posts/`        | `views.lista_posts`  | `lista_posts`   |
| `/posts/<id>/`   | `views.detalle_post` | `detalle_post`  |

## Cómo ejecutar el proyecto

1. Clonar el repositorio:
   ```
   git clone https://github.com/egle06/Blog_Django.git
   cd Blog_Django
   ```
2. Crear y activar el entorno virtual:
   - Windows: `python -m venv venv` y luego `venv\Scripts\activate`
   - Mac/Linux: `python3 -m venv venv` y luego `source venv/bin/activate`
3. Instalar dependencias:
   ```
   pip install -r requirements.txt
   ```
4. Iniciar el servidor:
   ```
   python manage.py runserver
   ```
5. Abrir en el navegador: <http://127.0.0.1:8000/>

## Tecnologías

- Python
- Django
- HTML5, CSS3 y JavaScript

## Autor

Egle Martinelli — Proyecto integrador, Módulo 8.