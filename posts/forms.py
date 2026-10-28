from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["titulo", "contenido", "autor", "estado", "imagen"]
        labels = {
            "titulo": "Título",
            "contenido": "Contenido",
            "autor": "Autor",
            "estado": "Estado",
            "imagen": "Imagen",
        }
        widgets = {
            "titulo": forms.TextInput(attrs={
                "placeholder": "Escribe el título del post"
            }),
            "contenido": forms.Textarea(attrs={
                "placeholder": "Escribe el contenido del post",
                "rows": 6
            }),
            "autor": forms.TextInput(attrs={
                "placeholder": "Nombre del autor"
            }),
        }