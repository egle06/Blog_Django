# Mi Blog con Django

Blog web hecho con Django como proyecto integrador. Permite publicar posts con imágenes, registrarse e iniciar sesión, tener un perfil con avatar y ver a los autores del blog. Cada post pertenece a un usuario y solo su autor puede editarlo o eliminarlo.

## Tecnologías

- Python
- Django (ORM, migraciones, autenticación, signals, ModelForm y panel de administración)
- Pillow (manejo de imágenes)
- python-decouple (variables de entorno)
- SQLite
- HTML5, CSS3 y JavaScript

## Funcionalidades principales

- Páginas de **Inicio** y **Acerca de**.
- **Listado de posts** público, con búsqueda por texto, filtro por estado y orden (más recientes o más antiguos).
- **Detalle de post** con título, contenido, autor, estado e imagen.
- **CRUD de posts con imágenes**: crear, editar y eliminar (con página de confirmación). Requiere sesión iniciada y ser el autor del post.
- **Registro**, **login** y **logout** de usuarios.
- **Perfil de usuario** con biografía, sitio web y avatar, creado automáticamente con signals.
- **Edición de perfil** y **cambio de contraseña**.
- **Lista pública de autores** con buscador y **perfil público** de cada autor con sus posts.
- Mensajes de confirmación al registrarse, crear, editar y eliminar.
- Panel de administración de Django para `Post` y `Perfil`.

## Instalación y ejecución local

Con estos pasos se reconstruye el proyecto desde cero, sin necesidad de `db.sqlite3` ni de la carpeta `media/` (que no se suben al repositorio).

1. **Clonar el repositorio:**
   ```
   git clone https://github.com/egle06/Blog_Django.git
   cd Blog_Django
   ```

2. **Crear y activar el entorno virtual:**
   - Windows: `python -m venv venv` y luego `venv\Scripts\activate`
   - Mac/Linux: `python3 -m venv venv` y luego `source venv/bin/activate`

3. **Instalar las dependencias:**
   ```
   pip install -r requirements.txt
   ```

4. **Crear el archivo de variables de entorno.** El proyecto lee su configuración desde un archivo `.env`, que no está en el repositorio. Se crea copiando el archivo de ejemplo:
   - Windows: `copy .env.example .env`
   - Mac/Linux: `cp .env.example .env`

   Con solo ese comando alcanza para ejecutar el proyecto en modo desarrollo: no hace falta editar nada.

   El archivo `.env` contiene estas variables:

   | Variable     | Descripción                                     | Valor en el ejemplo              |
   |--------------|-------------------------------------------------|----------------------------------|
   | `SECRET_KEY` | Clave secreta de Django.                        | `colocar-una-clave-secreta`      |
   | `DEBUG`      | `True` en desarrollo, `False` en producción.    | `True`                           |

   > **Opcional:** el valor de ejemplo de `SECRET_KEY` sirve para probar el proyecto en local. Para un uso real, conviene reemplazarlo por una clave propia y no compartirla. Se puede generar una con:
   > ```
   > python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   > ```
   > y pegarla en el `.env` después de `SECRET_KEY=`.

   El archivo `.env` está en el `.gitignore` y **no se sube al repositorio**. Solo se incluye `.env.example`, sin valores reales.

5. **Aplicar las migraciones** (crea la base de datos SQLite con las tablas de `Post`, `Perfil`, usuarios, etc.):
   ```
   python manage.py migrate
   ```

6. **Crear un superusuario** (necesario para entrar al panel de administración):
   ```
   python manage.py createsuperuser
   ```
   Solo los usuarios marcados como *staff* pueden entrar al admin. Los usuarios que se registran desde el sitio son usuarios comunes y no tienen acceso al panel.

7. **Iniciar el servidor:**
   ```
   python manage.py runserver
   ```

8. **Abrir en el navegador:**
   - Sitio: <http://127.0.0.1:8000/>
   - Registro: <http://127.0.0.1:8000/accounts/registro/>
   - Login: <http://127.0.0.1:8000/accounts/login/>
   - Autores: <http://127.0.0.1:8000/accounts/autores/>
   - Admin: <http://127.0.0.1:8000/admin/>

## Cómo probar el proyecto

1. Registrar un usuario en `/accounts/registro/`: queda con la sesión iniciada y su perfil se crea automáticamente (se ve en **Perfiles** del admin).
2. Ir a **Mi perfil** > **Editar perfil**, completar la biografía y subir un avatar.
3. Crear un post en `/posts/crear/` con una imagen. El autor es el usuario logueado.
4. En `/posts/`, probar el buscador, el filtro por estado y el orden.
5. Cerrar sesión y comprobar que `/posts/crear/`, `/accounts/perfil/` y las URL de editar y eliminar redirigen al login.
6. Registrar un segundo usuario: ve los posts del primero, pero sin botones de editar o eliminar, y si escribe la URL a mano recibe un mensaje de permiso denegado.
7. Entrar a `/accounts/autores/`, buscar un autor y abrir su perfil público.
8. Probar el cambio de contraseña desde **Mi perfil**.

## Modelos de datos

### `Post` (`posts/models.py`)

| Campo            | Tipo                                                    | Descripción                                                   |
|------------------|---------------------------------------------------------|---------------------------------------------------------------|
| `titulo`         | `CharField(max_length=200)`                             | Título del post                                               |
| `contenido`      | `TextField`                                             | Contenido completo                                            |
| `autor`          | `ForeignKey(AUTH_USER_MODEL, related_name="posts")`     | Usuario que creó el post (se asigna con `request.user`)       |
| `estado`         | `CharField` con `choices`                               | `borrador` (por defecto), `publicado` o `archivado`           |
| `fecha_creacion` | `DateTimeField(auto_now_add=True)`                      | Se completa automáticamente                                   |
| `slug`           | `SlugField(max_length=220, unique=True)`                | Se genera desde el título; si se repite, agrega `-2`, `-3`... |
| `imagen`         | `ImageField(upload_to='posts/', null=True, blank=True)` | Imagen opcional del post                                      |

### `Perfil` (`accounts/models.py`)

| Campo       | Tipo                                                            | Descripción                  |
|-------------|-----------------------------------------------------------------|------------------------------|
| `user`      | `OneToOneField(User, on_delete=CASCADE, related_name="perfil")` | Usuario dueño del perfil     |
| `biografia` | `TextField(max_length=500, blank=True)`                         | Biografía del usuario        |
| `link_web`  | `URLField(max_length=200, blank=True)`                          | Sitio web (opcional)         |
| `avatar`    | `ImageField(upload_to="avatares/", null=True, blank=True)`      | Imagen de perfil (opcional)  |

## Autenticación

- **Registro** (`/accounts/registro/`): `RegistroUsuarioForm` hereda de `UserCreationForm`, agrega el email y no permite emails repetidos. Al registrarse, el usuario queda con la sesión iniciada.
- **Login** (`/accounts/login/`): `LoginView` de Django. Si el usuario llegó desde una página protegida, vuelve a ella después de iniciar sesión (parámetro `next`).
- **Logout** (`/accounts/logout/`): `LogoutView` de Django, que se envía por `POST` desde el botón "Cerrar sesión" del menú.
- **Redirecciones** (`settings.py`): `LOGIN_URL = "login"`, `LOGIN_REDIRECT_URL = "lista_posts"` y `LOGOUT_REDIRECT_URL = "lista_posts"`.

## Perfiles y autores

### Creación automática con signals
Cada vez que se crea un usuario (por registro, desde el admin o con `createsuperuser`), una señal `post_save` crea su `Perfil`. Está en `accounts/signals.py` y se conecta en `AccountsConfig.ready()` (`accounts/apps.py`). Las vistas de perfil usan `get_or_create` para cubrir usuarios que pudieran no tenerlo.

### Imágenes y avatares
- `MEDIA_URL = '/media/'` y `MEDIA_ROOT = BASE_DIR / 'media'` en `settings.py`.
- En `blog_project/urls.py` se sirven los archivos media durante el desarrollo (solo con `DEBUG = True`).
- Los formularios con imágenes usan `enctype="multipart/form-data"` y reciben los archivos con `request.FILES`.
- Los templates verifican que exista la imagen antes de mostrarla. Si no hay avatar, se muestra un círculo con la inicial del usuario.
- La carpeta `media/` se crea sola al subir la primera imagen.

### Lista y perfil público de autores
- `/accounts/autores/` muestra todos los autores (con avatar, cantidad de posts y biografía) y un buscador por nombre de usuario.
- `/accounts/autores/<username>/` muestra el perfil público de un autor y sus posts. No muestra el email.
- Ambas páginas son de solo lectura y públicas. El botón "Editar perfil" solo aparece cuando el perfil visto es el del usuario logueado.

## Rutas y permisos

| URL                            | Vista                          | Nombre                 | Acceso                    |
|--------------------------------|--------------------------------|------------------------|---------------------------|
| `/`                            | `posts.views.inicio`           | `inicio`               | Público                   |
| `/acerca/`                     | `posts.views.acerca`           | `acerca`               | Público                   |
| `/posts/`                      | `posts.views.lista_posts`      | `lista_posts`          | Público                   |
| `/posts/<slug>/`               | `posts.views.detalle_post`     | `detalle_post`         | Público                   |
| `/posts/crear/`                | `posts.views.crear_post`       | `crear_post`           | **Requiere sesión**       |
| `/posts/<slug>/editar/`        | `posts.views.editar_post`      | `editar_post`          | **Sesión + ser el autor** |
| `/posts/<slug>/eliminar/`      | `posts.views.eliminar_post`    | `eliminar_post`        | **Sesión + ser el autor** |
| `/accounts/registro/`          | `accounts.views.registro`      | `registro`             | Público                   |
| `/accounts/login/`             | `LoginView`                    | `login`                | Público                   |
| `/accounts/logout/`            | `LogoutView`                   | `logout`               | Con sesión (por `POST`)   |
| `/accounts/autores/`           | `accounts.views.lista_autores` | `lista_autores`        | Público                   |
| `/accounts/autores/<username>/`| `accounts.views.perfil_publico`| `perfil_publico`       | Público                   |
| `/accounts/perfil/`            | `accounts.views.perfil`        | `perfil`               | **Requiere sesión**       |
| `/accounts/perfil/editar/`     | `accounts.views.editar_perfil` | `editar_perfil`        | **Requiere sesión**       |
| `/accounts/password/`          | `PasswordChangeView`           | `password_change`      | **Requiere sesión**       |
| `/accounts/password/cambiada/` | `PasswordChangeDoneView`       | `password_change_done` | **Requiere sesión**       |
| `/admin/`                      | Panel de Django                | —                      | Solo staff                |

### Rutas protegidas
Se protegen con `@login_required`: `crear_post`, `editar_post`, `eliminar_post`, `perfil` y `editar_perfil`. Un visitante sin sesión es redirigido a `/accounts/login/?next=<url>`.

### Solo el autor modifica sus posts
`editar_post` y `eliminar_post` comparan `post.autor` con `request.user`; si no coinciden devuelven `HttpResponseForbidden`. Los botones de editar y eliminar solo se muestran al autor, pero la validación real está en la vista, así que escribir la URL a mano tampoco funciona.

## Estructura del proyecto

```
Blog_Django/
├── .env.example             # plantilla de variables de entorno (sin valores reales)
├── .gitignore
├── manage.py
├── README.md
├── requirements.txt
├── blog_project/
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/
│   ├── migrations/
│   ├── templates/accounts/
│   │   ├── login.html
│   │   ├── registro.html
│   │   ├── perfil.html
│   │   ├── perfil_publico.html
│   │   ├── lista_autores.html
│   │   ├── editar_perfil.html
│   │   ├── password_change.html
│   │   └── password_change_done.html
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── signals.py
│   ├── urls.py
│   └── views.py
└── posts/
    ├── migrations/
    ├── static/posts/
    │   ├── css/estilos.css
    │   ├── img/logo.jpg
    │   └── js/main.js
    ├── templates/posts/
    │   ├── acerca.html
    │   ├── base.html
    │   ├── detalle_post.html
    │   ├── inicio.html
    │   ├── lista_posts.html
    │   ├── post_confirm_delete.html
    │   └── post_form.html
    ├── admin.py
    ├── apps.py
    ├── forms.py
    ├── models.py
    ├── urls.py
    └── views.py
```

> Las carpetas `venv/`, `__pycache__/`, `media/` y `.vscode/`, y los archivos `.env` y `db.sqlite3`, existen solo en el entorno local. Están en el `.gitignore` y no se suben al repositorio.

## Autor

Egle Martinelli — Proyecto integrador.