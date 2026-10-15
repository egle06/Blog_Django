from django.urls import path
from . import views

urlpatterns = [
   path("", views.inicio, name="inicio"),
   path("acerca/", views.acerca, name="acerca"),
   path("posts/", views.lista_posts, name="lista_posts"),
   path("posts/<int:post_id>/", views.detalle_post, name="detalle_post"),
]