# Mi Blog con Django

Proyecto integrador: un blog hecho con Django. En esta etapa (Preentrega 9) el sitio se conectó a una base de datos SQLite mediante el ORM de Django: las publicaciones se cargan desde el panel de administración y se muestran dinámicamente en la página de listado.

## Qué incluye

- Página de **Inicio** con título y mensaje de bienvenida.
- Página **Acerca de** con una reseña del autor y el propósito del sitio.
- Página de **Posts** con el listado de publicaciones **leídas desde la base de datos** (solo las de estado *Publicado*, de la más nueva a la más antigua).
- Página de **detalle** de cada post (título, autor y contenido).
- Modelo `Post` con migraciones aplicadas.
- Panel de administración de Django configurado para gestionar los posts.
- Menú de navegación y enlace "Volver al inicio" en todas las páginas.
- Layout base reutilizable (`base.html`) con herencia de templates.
- Archivos estáticos: CSS, JavaScript y logo.

> **Nota:** la página de listado (`/posts/`) ya usa la base de datos. La página de detalle (`/posts/<id>/`) todavía usa una lista de ejemplo definida en `views.py`; se conectará a la base de datos en un módulo futuro.

## Modelo de datos

El modelo `Post` está definido en `posts/models.py`:

| Campo            | Tipo                                  | Descripción                                        |
|------------------|---------------------------------------|----------------------------------------------------|
| `titulo`         | `CharField(max_length=200)`           | Título del post                                    |
| `contenido`      | `TextField`                           | Contenido completo                                 |
| `autor`          | `CharField(max_length=100)`           | Nombre del autor                                   |
| `fecha_creacion` | `DateTimeField(auto_now_add=True)`    | Se completa automáticamente al crear el post       |
| `estado`         | `CharField` con `choices`             | `borrador` (por defecto), `publicado` o `archivado`|

El método `__str__` devuelve el título, y los posts se ordenan por defecto del más nuevo al más antiguo.

## Flujo de Django aplicado

```
Base de datos -> Vista (ORM) -> Contexto -> Template -> Navegador
```

1. Los posts se crean desde `/admin/` y se guardan en `db.sqlite3`.
2. La vista `lista_posts` (`posts/views.py`) consulta con el ORM:
   `Post.objects.filter(estado="publicado").order_by("-fecha_creacion")`.
3. La vista envía los posts al template mediante un contexto.
4. `lista_posts.html` hereda de `base.html` y recorre los posts con `{% for post in posts %}`.

## Panel de administración

1. Aplicar las migraciones:
   ```
   python manage.py migrate
   ```
2. Crear un superusuario:
   ```
   python manage.py createsuperuser
   ```
3. Iniciar el servidor:
   ```
   python manage.py runserver
   ```
4. Entrar a <http://127.0.0.1:8000/admin/> con el usuario y la contraseña creados.
5. En **Posts** se pueden crear, editar y eliminar publicaciones. Solo las que tienen estado **Publicado** aparecen en <http://127.0.0.1:8000/posts/>.

En el listado del admin se muestran el título, el autor, el estado y la fecha de creación, con búsqueda y filtros por estado y fecha.

## Estructura del proyecto

```
Django_Blog/
├── .vscode/                 # configuración del editor (del módulo anterior)
├── .gitignore
├── manage.py
├── README.md
├── requirements.txt
├── blog_project/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── posts/
    ├── migrations/
    │   ├── __init__.py
    │   └── 0001_initial.py
    ├── static/
    │   └── posts/
    │       ├── css/estilos.css
    │       ├── img/logo.jpg
    │       └── js/main.js
    ├── templates/
    │   └── posts/
    │       ├── acerca.html
    │       ├── base.html
    │       ├── detalle_post.html
    │       ├── inicio.html
    │       └── lista_posts.html
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── tests.py
    ├── urls.py
    └── views.py
```

> Las carpetas `venv/` y `__pycache__/` y el archivo `db.sqlite3` existen en el entorno local, pero están en el `.gitignore` y no se suben al repositorio. La base de datos se vuelve a crear ejecutando `python manage.py migrate`.

## Rutas

| URL              | Vista                | Nombre          |
|------------------|----------------------|-----------------|
| `/`              | `views.inicio`       | `inicio`        |
| `/acerca/`       | `views.acerca`       | `acerca`        |
| `/posts/`        | `views.lista_posts`  | `lista_posts`   |
| `/posts/<id>/`   | `views.detalle_post` | `detalle_post`  |
| `/admin/`        | Panel de Django      | —               |

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
4. Crear la base de datos aplicando las migraciones:
   ```
   python manage.py migrate
   ```
5. Crear un superusuario para entrar al admin:
   ```
   python manage.py createsuperuser
   ```
6. Iniciar el servidor:
   ```
   python manage.py runserver
   ```
7. Abrir en el navegador:
   - Sitio: <http://127.0.0.1:8000/>
   - Admin: <http://127.0.0.1:8000/admin/>

## Tecnologías

- Python
- Django (ORM, migraciones y panel de administración)
- SQLite
- HTML5, CSS3 y JavaScript

## Autor

Egle Martinelli — Proyecto integrador, Módulo 9.