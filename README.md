# Blog Django

Proyecto base de un blog web desarrollado con Django.

## Descripción

Este repositorio contiene la estructura inicial de un proyecto Django para construir un blog.
Incluye la configuración base del proyecto (`blog_project`) y una aplicación llamada `posts`.

## Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/egle06/Blog_Django.git
```

2. Entrar a la carpeta del proyecto:

```bash
cd Blog_Django
```

3. Crear el entorno virtual:

```bash
python -m venv venv
```

4. Activar el entorno virtual.

En Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

En Linux o macOS:

```bash
source venv/bin/activate
```

5. Instalar las dependencias:

```bash
pip install -r requirements.txt
```

6. Ejecutar el servidor de desarrollo:

```bash
python manage.py runserver
```

7. Abrir en el navegador: http://127.0.0.1:8000/

## Aplicaciones

- `posts`: aplicación inicial para manejar las publicaciones del blog.