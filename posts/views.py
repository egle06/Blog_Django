from django.http import Http404
from django.shortcuts import render

Posts = [
    {"id": 1, "titulo": "Mi primer post", "autor": "Ana",
     "contenido": "Contenido del primer post."},
    {"id": 2, "titulo": "Aprendiendo Django", "autor": "Luis",
     "contenido": "Contenido del segundo post."},
    {"id": 3, "titulo": "Templates reutilizables", "autor": "Marta",
     "contenido": "Contenido del tercer post."},
]


def inicio(request):
    return render(request, 'posts/inicio.html')


def acerca(request):
    return render(request, 'posts/acerca.html')


def lista_posts(request):
    return render(request, 'posts/lista_posts.html', {"posts": Posts})


def detalle_post(request, post_id):
    for post in Posts:
        if post["id"] == post_id:
            return render(request, 'posts/detalle_post.html', {"post": post})
    raise Http404("El post no existe")