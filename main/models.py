from django.db import models
from django.contrib.auth.models import AbstractUser

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.nombre

class Subcategoria(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True)

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
    imagen = models.ImageField(upload_to='static', verbose_name='Imagen')
    rating_original = models.DecimalField(max_digits=10, decimal_places=1)
    rating = models.DecimalField(null = True, max_digits=10, decimal_places=1)

    def __str__(self):
        return self.nombre

    
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
    profile_image = models.ImageField(upload_to='static/profile_images/', blank=True, null=True)
    
    # Otros campos que puedas necesitar
    #lista_favoritos = models.ManyToManyField(Producto, related_name='usuarios_favoritos', blank=True)
    # ... otros campos ...

    # Especifica related_name de manera única para evitar conflictos
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='usuario_groups',  # Cambia 'usuario_groups' según tus preferencias
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='usuario_permissions',  # Cambia 'usuario_permissions' según tus preferencias
        blank=True,
    )

    def __str__(self):
        return self.username