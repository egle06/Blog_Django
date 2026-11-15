from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.db.models import Q
from .forms import PostForm
from .models import Post


def inicio(request):
    return render(request, 'posts/inicio.html')


def acerca(request):
    return render(request, 'posts/acerca.html')


def lista_posts(request):
    posts = Post.objects.all()

    busqueda = request.GET.get("q")
    estado = request.GET.get("estado")
    orden = request.GET.get("orden", "reciente")

    if busqueda:
        posts = posts.filter(
            Q(titulo__icontains=busqueda) |
            Q(contenido__icontains=busqueda)
        )
    if estado:
        posts = posts.filter(estado=estado)
    if orden == "antiguo":
        posts = posts.order_by("fecha_creacion")
    else:
        posts = posts.order_by("-fecha_creacion")

    return render(request, 'posts/lista_posts.html', {
        "posts": posts,
        "busqueda": busqueda,
        "estado": estado,
        "orden": orden,
        "estados_opciones": Post.ESTADOS,
    })


def detalle_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'posts/detalle_post.html', {"post": post})

@login_required
def crear_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)   # request.FILES = la imagen
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user
            post.save()
            messages.success(request, 'El post fue creado correctamente.')
            return redirect("detalle_post", slug=post.slug)
    else:
        form = PostForm()

    return render(request, 'posts/post_form.html', {
        "form": form,
        "titulo_pagina": "Crear post",
        "texto_boton": "Guardar post",
    })

@login_required
def editar_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.autor != request.user:
        return HttpResponseForbidden("No tenés permiso para modificar este post.")
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'El post fue actualizado correctamente.')
            return redirect("detalle_post", slug=post.slug)
    else:
        form = PostForm(instance=post)

    return render(request, 'posts/post_form.html', {
        "form": form,
        "post": post,
        "titulo_pagina": "Editar post",
        "texto_boton": "Guardar cambios",
    })

@login_required
def eliminar_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if post.autor != request.user:
        return HttpResponseForbidden("No tenés permiso para modificar este post.")
    if request.method == "POST":
        post.delete()
        messages.success(request, 'El post fue eliminado correctamente.')
        return redirect("lista_posts")
    return render(request, 'posts/post_confirm_delete.html', {"post": post})