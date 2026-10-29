from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Post(models.Model):
    ESTADOS = [
        ("borrador", "Borrador"),
        ("publicado", "Publicado"),
        ("archivado", "Archivado"),
    ]

    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts"
    )
    estado = models.CharField(max_length=20, choices=ESTADOS, default="borrador")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=220, unique=True, blank=True, null=True)
    imagen = models.ImageField(upload_to="posts/", null=True, blank=True)

    class Meta:
        ordering = ["-fecha_creacion"]

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        # El slug se genera una sola vez; si cambia el título, la URL no cambia.
        if not self.slug:
            base = slugify(self.titulo) or "post"
            slug, n = base, 2
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)