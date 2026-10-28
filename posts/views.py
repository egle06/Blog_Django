from django.shortcuts import render, redirect, get_object_or_404

from .forms import PostForm
from .models import Post


def inicio(request):
    return render(request, 'posts/inicio.html')


def acerca(request):
    return render(request, 'posts/acerca.html')


def lista_posts(request):
    posts = Post.objects.all().order_by("-fecha_creacion")
    return render(request, 'posts/lista_posts.html', {"posts": posts})


def detalle_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'posts/detalle_post.html', {"post": post})


def crear_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)   # request.FILES = la imagen
        if form.is_valid():
            post = form.save()
            return redirect("detalle_post", slug=post.slug)
    else:
        form = PostForm()

    return render(request, 'posts/post_form.html', {
        "form": form,
        "titulo_pagina": "Crear post",
        "texto_boton": "Guardar post",
    })


def editar_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect("detalle_post", slug=post.slug)
    else:
        form = PostForm(instance=post)

    return render(request, 'posts/post_form.html', {
        "form": form,
        "post": post,
        "titulo_pagina": "Editar post",
        "texto_boton": "Guardar cambios",
    })


def eliminar_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        post.delete()
        return redirect("lista_posts")
    return render(request, 'posts/post_confirm_delete.html', {"post": post})