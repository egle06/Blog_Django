# Mi Blog con Django

Proyecto integrador: un blog hecho con Django. En esta etapa (Preentrega 11) se agregó **autenticación de usuarios**: registro, inicio y cierre de sesión, un **perfil** con biografía y avatar, cambio de contraseña y **protección de las acciones sobre los posts**. Cada post pertenece a un usuario y solo su autor puede editarlo o borrarlo.

## Qué incluye

- Página de **Inicio** y página **Acerca de**.
- **Listado de posts** y **detalle** de cada post, visibles para cualquier visitante (con o sin sesión).
- **CRUD de posts con imágenes** (Módulo 10): crear, editar y eliminar requieren sesión iniciada y ser el autor del post.
- **Registro de usuarios** con formulario personalizado (usuario, email y contraseña).
- **Login** y **logout** con el sistema de autenticación de Django.
- Modelo **`Perfil`** (biografía, sitio web y avatar) relacionado uno a uno con `User`.
- **Página de perfil** y **edición de perfil** (datos del usuario, biografía y avatar).
- **Cambio de contraseña**.
- Menú de navegación que cambia según haya o no sesión iniciada.
- Panel de administración de Django con `Post` y `Perfil`.

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

Desde el Módulo 11 el autor ya no es un texto libre: es el usuario con sesión iniciada que crea el post.

### `Perfil` (`accounts/models.py`)

| Campo       | Tipo                                                              | Descripción                       |
|-------------|-------------------------------------------------------------------|-----------------------------------|
| `user`      | `OneToOneField(User, on_delete=CASCADE, related_name="perfil")`   | Usuario dueño del perfil          |
| `biografia` | `TextField(max_length=500, blank=True)`                           | Biografía del usuario             |
| `link_web`  | `URLField(max_length=200, blank=True)`                            | Sitio web (opcional)              |
| `avatar`    | `ImageField(upload_to="avatares/", null=True, blank=True)`        | Imagen de perfil (opcional)       |

La relación `OneToOneField` hace que cada usuario tenga **un solo** perfil. Con `related_name="perfil"` se accede desde el usuario con `user.perfil`.

## Cómo funciona la autenticación

### Registro
- URL: `/accounts/registro/`.
- Usa `RegistroUsuarioForm`, que hereda de `UserCreationForm` y agrega el campo `email` (no permite emails repetidos).
- Al registrarse, Django guarda la contraseña encriptada, el usuario queda con la sesión iniciada y se redirige al listado con un mensaje de bienvenida.
- Si un usuario con sesión iniciada entra al registro, se lo redirige al listado.

### Iniciar sesión
- URL: `/accounts/login/`, con `LoginView` de Django y el template `accounts/login.html`.
- Si el usuario o la contraseña son incorrectos, se muestra un error.
- Si el usuario llegó desde una página protegida, vuelve a ella después de iniciar sesión (parámetro `next`).

### Cerrar sesión
- URL: `/accounts/logout/`, con `LogoutView` de Django.
- Se hace con un **formulario `POST`** desde el menú (el botón "Cerrar sesión"). Un enlace común no funciona porque Django exige `POST` para cerrar sesión.

### Redirecciones (`settings.py`)
```python
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "lista_posts"
LOGOUT_REDIRECT_URL = "lista_posts"
```

## Perfil de usuario

### Creación automática con signals
Cada vez que se crea un usuario (por registro, desde el admin o con `createsuperuser`), una señal `post_save` crea su `Perfil` automáticamente. Está en `accounts/signals.py` y se conecta en `AccountsConfig.ready()` (`accounts/apps.py`).

```python
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def crear_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)
```
La vista de registro y las vistas de perfil usan `Perfil.objects.get_or_create(user=...)` para evitar errores con usuarios creados antes de existir la señal.

### Avatares
- El campo `avatar` es un `ImageField` que guarda las imágenes en `media/avatares/`.
- Se reutiliza la configuración del Módulo 10: `MEDIA_URL = '/media/'`, `MEDIA_ROOT = BASE_DIR / 'media'` y `static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)` en `blog_project/urls.py` (solo con `DEBUG = True`).
- La edición del perfil recibe la imagen con `PerfilForm(request.POST, request.FILES, instance=perfil)` y el `<form>` usa `enctype="multipart/form-data"`.
- Los templates verifican `{% if perfil.avatar %}` antes de mostrar la imagen. Si no hay avatar, se muestra un círculo con la inicial del usuario.

### Páginas de perfil
- `/accounts/perfil/`: muestra usuario, email, biografía, sitio web y avatar.
- `/accounts/perfil/editar/`: permite cambiar nombre, apellido, email, biografía, sitio web y avatar.
- `/accounts/password/`: permite cambiar la contraseña (`PasswordChangeView`), y `/accounts/password/cambiada/` confirma el cambio.

## Rutas y permisos

| URL                            | Vista                         | Nombre                | Acceso                          |
|--------------------------------|-------------------------------|-----------------------|---------------------------------|
| `/`                            | `posts.views.inicio`          | `inicio`              | Público                         |
| `/acerca/`                     | `posts.views.acerca`          | `acerca`              | Público                         |
| `/posts/`                      | `posts.views.lista_posts`     | `lista_posts`         | Público                         |
| `/posts/<slug>/`               | `posts.views.detalle_post`    | `detalle_post`        | Público                         |
| `/posts/crear/`                | `posts.views.crear_post`      | `crear_post`          | **Requiere sesión**             |
| `/posts/<slug>/editar/`        | `posts.views.editar_post`     | `editar_post`         | **Sesión + ser el autor**       |
| `/posts/<slug>/eliminar/`      | `posts.views.eliminar_post`   | `eliminar_post`       | **Sesión + ser el autor**       |
| `/accounts/registro/`          | `accounts.views.registro`     | `registro`            | Público                         |
| `/accounts/login/`             | `LoginView`                   | `login`               | Público                         |
| `/accounts/logout/`            | `LogoutView`                  | `logout`              | Con sesión (por `POST`)         |
| `/accounts/perfil/`            | `accounts.views.perfil`       | `perfil`              | **Requiere sesión**             |
| `/accounts/perfil/editar/`     | `accounts.views.editar_perfil`| `editar_perfil`       | **Requiere sesión**             |
| `/accounts/password/`          | `PasswordChangeView`          | `password_change`     | **Requiere sesión**             |
| `/accounts/password/cambiada/` | `PasswordChangeDoneView`      | `password_change_done`| **Requiere sesión**             |
| `/admin/`                      | Panel de Django               | —                     | Staff                           |

### Vistas que requieren autenticación
Se protegen con el decorador `@login_required`: `crear_post`, `editar_post`, `eliminar_post`, `perfil` y `editar_perfil`. Si un visitante sin sesión intenta entrar, Django lo redirige a `/accounts/login/?next=<url>`.

### Solo el autor puede modificar sus posts
`editar_post` y `eliminar_post` comparan `post.autor` con `request.user`; si no coinciden devuelven `HttpResponseForbidden` ("No tenés permiso para modificar este post"). Los botones de Editar y Eliminar solo se muestran al autor, pero la validación real está en la vista, de modo que escribir la URL a mano tampoco funciona.

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
4. Aplicar las migraciones (crea la base de datos, incluidas las tablas de `Post` y `Perfil`):
   ```
   python manage.py migrate
   ```
5. Crear un superusuario (opcional, para entrar al admin):
   ```
   python manage.py createsuperuser
   ```
6. Iniciar el servidor:
   ```
   python manage.py runserver
   ```
7. Abrir en el navegador:
   - Sitio: <http://127.0.0.1:8000/>
   - Registro: <http://127.0.0.1:8000/accounts/registro/>
   - Login: <http://127.0.0.1:8000/accounts/login/>
   - Admin: <http://127.0.0.1:8000/admin/>

### Sobre las migraciones
Este módulo agrega migraciones para el modelo `Perfil` (app `accounts`) y para cambiar el campo `autor` de `Post` a una relación con el usuario (app `posts`). Después de clonar el proyecto alcanza con `python manage.py migrate`. Si se modifica un modelo, hay que ejecutar antes `python manage.py makemigrations`.

> Nota: al cambiar `autor` de texto a `ForeignKey`, los posts creados antes del Módulo 11 no son compatibles y hay que borrarlos antes de migrar.

## Cómo probar el módulo

1. Registrar un usuario en `/accounts/registro/`: queda con la sesión iniciada y se crea su perfil automáticamente (se puede ver en el admin, en **Perfiles**).
2. Ir a **Mi perfil** > **Editar perfil**, completar la biografía y subir un avatar. Verificar que se ve en la página de perfil.
3. Crear un post en `/posts/crear/`: el autor es el usuario logueado.
4. Cerrar sesión y comprobar que `/posts/crear/`, `/accounts/perfil/` y las URL de editar y eliminar redirigen al login.
5. Registrar un segundo usuario: puede ver los posts del primero, pero sin botones de editar o eliminar, y si escribe la URL a mano recibe un mensaje de permiso denegado.
6. Probar el cambio de contraseña en **Mi perfil** > **Cambiar contraseña** e iniciar sesión con la nueva.

## Estructura del proyecto

```
Django_Blog/
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
│   ├── posts/
│   └── avatares/
├── accounts/
│   ├── migrations/
│   ├── templates/
│   │   └── accounts/
│   │       ├── login.html
│   │       ├── registro.html
│   │       ├── perfil.html
│   │       ├── editar_perfil.html
│   │       ├── password_change.html
│   │       └── password_change_done.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── signals.py
│   ├── urls.py
│   └── views.py
└── posts/
    ├── migrations/
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

> Las carpetas `venv/`, `__pycache__/` y `media/` y el archivo `db.sqlite3` existen en el entorno local, pero están en el `.gitignore` y no se suben al repositorio. La base de datos se vuelve a crear con `python manage.py migrate`.

## Tecnologías

- Python
- Django (ORM, migraciones, autenticación, signals, ModelForm y panel de administración)
- Pillow (manejo de imágenes)
- SQLite
- HTML5, CSS3 y JavaScript

## Autor

Egle Martinelli — Proyecto integrador, Módulo 11.