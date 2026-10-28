# Mi Blog con Django

Proyecto integrador: un blog hecho con Django. En esta etapa (Preentrega 10) el sitio permite **crear, ver, editar y eliminar publicaciones (CRUD) desde la propia interfaz web**, usando formularios `ModelForm`, y cada post puede tener una **imagen** asociada, cargada desde el formulario.

## Qué incluye

- Página de **Inicio** con título y mensaje de bienvenida.
- Página **Acerca de** con una reseña del autor y el propósito del sitio.
- Página de **Posts** con el listado de publicaciones **leídas desde la base de datos** (**todos los posts**, sin importar su estado: *Borrador*, *Publicado* o *Archivado*; de la más nueva a la más antigua).
- Página de **detalle** de cada post (título, contenido, autor, estado e imagen si existe), con URL amigable basada en `slug`.
- **CRUD completo** de posts desde el sitio: crear, listar, ver detalle, editar y eliminar (con página de confirmación).
- **Carga de imágenes** opcional en cada post.
- Modelo `Post` con migraciones aplicadas.
- Panel de administración de Django configurado para gestionar los posts.
- Menú de navegación y enlace "Volver al inicio" en todas las páginas.
- Layout base reutilizable (`base.html`) con herencia de templates.
- Archivos estáticos: CSS, JavaScript y logo.

## Modelo de datos

El modelo `Post` está definido en `posts/models.py`:

| Campo            | Tipo                                                  | Descripción                                                   |
|------------------|-------------------------------------------------------|---------------------------------------------------------------|
| `titulo`         | `CharField(max_length=200)`                           | Título del post                                               |
| `contenido`      | `TextField`                                           | Contenido completo                                            |
| `autor`          | `CharField(max_length=100)`                           | Nombre del autor                                              |
| `fecha_creacion` | `DateTimeField(auto_now_add=True)`                    | Se completa automáticamente al crear el post                  |
| `estado`         | `CharField` con `choices`                             | `borrador` (por defecto), `publicado` o `archivado`           |
| `slug`           | `SlugField(max_length=220, unique=True, blank=True, null=True)` | Se genera solo a partir del título (con `slugify`) |
| `imagen`         | `ImageField(upload_to='posts/', null=True, blank=True)` | Imagen opcional del post                                    |

El método `save()` genera el `slug` automáticamente si el post todavía no tiene uno. El método `__str__` devuelve el título, y los posts se ordenan por defecto del más nuevo al más antiguo.

## Operaciones CRUD

| Operación        | URL                           | Vista            | Nombre          |
|------------------|-------------------------------|------------------|-----------------|
| Listar posts     | `/posts/`                     | `lista_posts`    | `lista_posts`   |
| Ver detalle      | `/posts/<slug>/`              | `detalle_post`   | `detalle_post`  |
| Crear post       | `/posts/crear/`               | `crear_post`     | `crear_post`    |
| Editar post      | `/posts/<slug>/editar/`       | `editar_post`    | `editar_post`   |
| Eliminar post    | `/posts/<slug>/eliminar/`     | `eliminar_post`  | `eliminar_post` |

- **Crear / Editar:** usan el mismo template (`post_form.html`) y el formulario `PostForm`. Al guardar, redirigen al detalle del post.
- **Eliminar:** primero muestra una página de confirmación (`post_confirm_delete.html`). El post solo se borra cuando se envía el formulario por `POST`; luego redirige al listado.
- Las rutas más específicas (`crear/`, `editar/`, `eliminar/`) están definidas antes de `<slug:slug>/` para que Django no las confunda con un slug.

## Formulario (`ModelForm`)

`posts/forms.py` define `PostForm`, que hereda de `forms.ModelForm`, está basado en el modelo `Post` e incluye los campos `titulo`, `contenido`, `autor`, `estado` e `imagen`. Así no hace falta repetir los campos a mano: Django los genera, valida y guarda a partir del modelo.

## Manejo de imágenes

Para que los posts puedan tener imagen se configuró lo siguiente:

1. **Modelo:** campo `imagen = models.ImageField(upload_to='posts/', null=True, blank=True)`. Las imágenes se guardan en `media/posts/` y la imagen es opcional.
2. **Settings** (`blog_project/settings.py`):
   ```python
   MEDIA_URL = '/media/'
   MEDIA_ROOT = BASE_DIR / 'media'
   ```
3. **URLs del proyecto** (`blog_project/urls.py`): en desarrollo se sirven los archivos media con
   ```python
   if settings.DEBUG:
       urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
   ```
4. **Vistas:** en `crear_post` y `editar_post` el formulario se instancia con los datos y los archivos: `PostForm(request.POST, request.FILES)` (y `instance=post` al editar).
5. **Template del formulario** (`post_form.html`): la etiqueta `<form>` incluye `enctype="multipart/form-data"`; sin este atributo la imagen no llega al servidor.
6. **Mostrar la imagen:** los templates verifican `{% if post.imagen %}` antes de usar `post.imagen.url`, así un post sin imagen no rompe la página.

## Dependencia nueva

- **Pillow**: es necesaria para que Django pueda trabajar con `ImageField`. Ya está incluida en `requirements.txt` y se instala con `pip install -r requirements.txt`.

## Cómo probar la carga de imágenes

1. Iniciar el servidor con `python manage.py runserver`.
2. Entrar a <http://127.0.0.1:8000/posts/crear/>.
3. Completar el formulario, elegir una imagen en el campo **Imagen** y guardar (el post aparece en el listado con cualquier estado).
4. Verificar que la imagen se ve en el detalle del post y en el listado.
5. Entrar a **Editar**, cambiar la imagen y guardar.
6. Crear otro post **sin imagen** y comprobar que se muestra sin errores.
7. Probar **Eliminar**: debe aparecer la página de confirmación antes de borrar.

> La carpeta `media/` está en el `.gitignore`, por lo que las imágenes de prueba no se suben al repositorio.

## Flujo de Django aplicado

```
Base de datos -> Vista (ORM) -> Contexto -> Template -> Navegador
```

1. Los posts se pueden crear desde el sitio (`/posts/crear/`) o desde `/admin/` y se guardan en `db.sqlite3`.
2. La vista `lista_posts` (`posts/views.py`) consulta con el ORM:
   `Post.objects.all().order_by("-fecha_creacion")`, que trae todos los posts ordenados del más nuevo al más antiguo.
3. La vista envía los posts al template mediante un contexto.
4. `lista_posts.html` hereda de `base.html` y recorre los posts con `{% for post in posts %}`.
5. Para crear y editar, el flujo es: `GET` muestra el formulario → `POST` valida con `PostForm` → `form.save()` → `redirect`.

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
5. En **Posts** se pueden crear, editar y eliminar publicaciones. Todas aparecen en <http://127.0.0.1:8000/posts/>, sin importar su estado (la insignia de cada tarjeta indica si es *Borrador*, *Publicado* o *Archivado*).

En el listado del admin se muestran el título, el autor, el estado y la fecha de creación, con búsqueda y filtros por estado y fecha.

> Si hay posts creados antes de agregar el campo `slug`, hay que abrirlos en el admin y guardarlos de nuevo para que se les genere el slug.

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
├── media/                   # imágenes subidas (solo local, ignorada por git)
│   └── posts/
└── posts/
    ├── migrations/
    │   ├── __init__.py
    │   ├── 0001_initial.py
    │   └── ...              # migraciones de slug e imagen
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
    │       ├── lista_posts.html
    │       ├── post_confirm_delete.html
    │       └── post_form.html
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── forms.py
    ├── models.py
    ├── tests.py
    ├── urls.py
    └── views.py
```

> Las carpetas `venv/`, `__pycache__/` y `media/` y el archivo `db.sqlite3` existen en el entorno local, pero están en el `.gitignore` y no se suben al repositorio. La base de datos se vuelve a crear ejecutando `python manage.py migrate`.

## Rutas

| URL                       | Vista                | Nombre          |
|---------------------------|----------------------|-----------------|
| `/`                       | `views.inicio`       | `inicio`        |
| `/acerca/`                | `views.acerca`       | `acerca`        |
| `/posts/`                 | `views.lista_posts`  | `lista_posts`   |
| `/posts/crear/`           | `views.crear_post`   | `crear_post`    |
| `/posts/<slug>/editar/`   | `views.editar_post`  | `editar_post`   |
| `/posts/<slug>/eliminar/` | `views.eliminar_post`| `eliminar_post` |
| `/posts/<slug>/`          | `views.detalle_post` | `detalle_post`  |
| `/admin/`                 | Panel de Django      | —               |

## Cómo ejecutar el proyecto

1. Clonar el repositorio:
   ```
   git clone https://github.com/egle06/Blog_Django.git
   cd Blog_Django
   ```
2. Crear y activar el entorno virtual:
   - Windows: `python -m venv venv` y luego `venv\Scripts\activate`
   - Mac/Linux: `python3 -m venv venv` y luego `source venv/bin/activate`
3. Instalar dependencias (incluye Pillow):
   ```
   pip install -r requirements.txt
   ```
4. Crear la base de datos aplicando las migraciones:
   ```
   python manage.py migrate
   ```
5. Crear un superusuario para entrar al admin (opcional):
   ```
   python manage.py createsuperuser
   ```
6. Iniciar el servidor:
   ```
   python manage.py runserver
   ```
7. Abrir en el navegador:
   - Sitio: <http://127.0.0.1:8000/>
   - Posts: <http://127.0.0.1:8000/posts/>
   - Crear post: <http://127.0.0.1:8000/posts/crear/>
   - Admin: <http://127.0.0.1:8000/admin/>

## Tecnologías

- Python
- Django (ORM, migraciones, ModelForm y panel de administración)
- Pillow (manejo de imágenes)
- SQLite
- HTML5, CSS3 y JavaScript

## Autor

Egle Martinelli — Proyecto integrador, Módulo 10.