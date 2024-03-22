from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.utils.text import slugify


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre)
        super(Categoria, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre


class Subcategoria(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre)
        super(Subcategoria, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre


class Sabor(models.Model):
    sabor = models.CharField(max_length=30)

    def __str__(self):
        return self.sabor


class Ingrediente(models.Model):
    ingrediente = models.CharField(max_length=30)

    def __str__(self):
        return self.nombre


class Marca(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=120)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    subcategoria = models.ForeignKey(Subcategoria, on_delete=models.CASCADE)
    sabor = models.ManyToManyField(Sabor)
    ingrediente = models.ManyToManyField(Ingrediente)
    stock = models.BooleanField(default=True)
    url = models.URLField()
    imagen = models.ImageField(upload_to="static", verbose_name="Imagen")
    rating_original = models.DecimalField(max_digits=10, decimal_places=1)
    rating = models.DecimalField(null=True, max_digits=10, decimal_places=1)

    def __str__(self):
        return self.nombre

    def esta_en_lista_deseos(self, usuario):
        lista_deseos, creado = ListaDeseos.objects.get_or_create(usuario=usuario)
        return self in lista_deseos.productos.all()


class Usuario(AbstractUser):
    # Campos personalizados
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255, blank=True, null=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    ciudad = models.CharField(max_length=255, null=True, blank=True)
    pais = models.CharField(max_length=255, null=True, blank=True)
    codigo_postal = models.CharField(max_length=20, null=True, blank=True)
    profile_image = models.ImageField(
        upload_to="static/profile_images/", blank=True, null=True
    )

    # Especifica related_name de manera única para evitar conflictos
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="usuario_groups",  # Cambia 'usuario_groups' según tus preferencias
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="usuario_permissions",  # Cambia 'usuario_permissions' según tus preferencias
        blank=True,
    )

    def lista_deseos(self):
        lista_deseos, creado = ListaDeseos.objects.get_or_create(usuario=self)
        return lista_deseos

    def __str__(self):
        return self.username


class ListaDeseos(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    producto = models.ManyToManyField(Producto)

    def __str__(self):
        return self.producto


class Conversation(models.Model):
    participants = models.ManyToManyField(
        Usuario, related_name="conversation_participants"
    )


class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name="sent_messages"
    )
    receiver = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name="received_messages"
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


class Notification(models.Model):
    user = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name="notifications"
    )
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


class UserBlock(models.Model):
    blocked_user = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name="blocked_by"
    )
    blocked_by = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name="blocked_users"
    )


class ConversationMember(models.Model):
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="members"
    )
    user = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name="conversations"
    )
