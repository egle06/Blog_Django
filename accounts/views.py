from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistroUsuarioForm, UsuarioForm, PerfilForm
from .models import Perfil

User = get_user_model()



def registro(request):
    if request.user.is_authenticated:
        return redirect("lista_posts")

    if request.method == "POST":
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            Perfil.objects.get_or_create(user=user)
            login(request, user)
            messages.success(request, f"¡Bienvenido, {user.username}!")
            return redirect("lista_posts")
    else:
        form = RegistroUsuarioForm()

    return render(request, "accounts/registro.html", {"form": form})

@login_required
def perfil(request):
    perfil, creado = Perfil.objects.get_or_create(user=request.user)
    return render(request, "accounts/perfil.html", {"perfil": perfil})

@login_required
def editar_perfil(request):
    perfil, creado = Perfil.objects.get_or_create(user=request.user)

    if request.method == "POST":
        usuario_form = UsuarioForm(request.POST, instance=request.user)
        perfil_form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if usuario_form.is_valid() and perfil_form.is_valid():
            usuario_form.save()
            perfil_form.save()
            messages.success(request, "Perfil actualizado.")
            return redirect("perfil")
    else:
        usuario_form = UsuarioForm(instance=request.user)
        perfil_form = PerfilForm(instance=perfil)

    return render(request, "accounts/editar_perfil.html", {
        "usuario_form": usuario_form,
        "perfil_form": perfil_form,
    })

def lista_autores(request):
    autores = (
        User.objects.select_related("perfil")
        .annotate(total_posts=Count("posts"))
        .order_by("username")
    )

    busqueda = request.GET.get("q")
    if busqueda:
        autores = autores.filter(username__icontains=busqueda)

    return render(request, "accounts/lista_autores.html", {
        "autores": autores,
        "busqueda": busqueda,
    })


def perfil_publico(request, username):
    autor = get_object_or_404(User, username=username)
    perfil, creado = Perfil.objects.get_or_create(user=autor)
    posts = autor.posts.all()

    return render(request, "accounts/perfil_publico.html", {
        "autor": autor,
        "perfil": perfil,
        "posts": posts,
    })