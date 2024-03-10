import os
from re import sub
import shutil
import subprocess
import random
import requests

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import AuthenticationForm
from django.core.management import call_command
from django.core.files.storage import FileSystemStorage
from django.db import connection
from django.db.models import Q
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse

from main.forms import *
from main.models import (Categoria, Subcategoria, Ingrediente, Marca, Producto, Proteina,
                         Sabor, Snack, Vitamina)
from main.populateDB import populate

from whoosh.fields import DATETIME, ID, KEYWORD, Schema, TEXT
from whoosh.index import create_in, open_dir
from whoosh.qparser import MultifieldParser, OrGroup, QueryParser
from whoosh.query import And
from django.core.paginator import Paginator


#----------------VIEWS FOR BD LOAD AND DELETE---------------------------

def carga(request):
    populate()
    return HttpResponseRedirect('/inicio.html')


@user_passes_test(lambda u: u.is_superuser)
def eliminar_base_datos(request):
    if request.method == 'POST':
        confirmacion = request.POST.get('confirmacion', '')
        if confirmacion.lower() == 'eliminar':
            # Obtener el nombre de las tablas específicas del superusuario que deben conservarse
            tables_to_keep = ['main_user', 'main_usuario', 'main_usuario_groups', 'main_usuario_lista_favoritos', 'main_usuario_user_permissions']

            # Obtener el nombre de todas las tablas en la base de datos
            with connection.cursor() as cursor:
                cursor.execute("PRAGMA foreign_keys=off;")
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
                all_tables = cursor.fetchall()

                # Eliminar todos los contenidos de las tablas que empiecen por main_, excepto las específicas del superusuario
                for table in all_tables:
                    table_name = table[0]
                    if table_name.startswith('main_') and table_name not in tables_to_keep:
                        cursor.execute(f"DELETE FROM {table_name};")
                        cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table_name}';")
                cursor.execute("PRAGMA foreign_keys=on;")
            # Eliminar el contenido de la carpeta static/images
            images_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static', 'images'))
            shutil.rmtree(images_folder)
            # Eliminar todo el contenido creado con Whoosh en el directorio index
            index_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Index'))
            shutil.rmtree(index_folder)
            # Crear la carpeta nuevamente
            os.makedirs(index_folder)
            os.makedirs(images_folder)
            # Generar archivos de migración
            subprocess.run(["python", "manage.py", "makemigrations"])

            # Ejecutar las migraciones después de eliminar los contenidos de las tablas
            subprocess.run(["python", "manage.py", "migrate"])

            return HttpResponseRedirect('/inicio.html')  # Cambia 'index' con la URL de tu página principal
    
    return render(request, 'eliminar_base_datos.html')

#----------------VIEWS FOR USER MANAGEMENT---------------------------

def inicio_sesion(request):
    if request.method == 'POST':
        login_form = InicioSesionForm(request, request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenido, {user.username}!')
                return HttpResponseRedirect('/inicio.html')  
            else:
                messages.error(request, 'Credenciales inválidas. Inténtalo de nuevo.')
    else:
        login_form = InicioSesionForm()
    
    return render(request, 'inicio_sesion.html', {'login_form': login_form})

def cerrar_sesion(request):
    logout(request)
    return HttpResponseRedirect('/inicio.html')

def registro(request):
    response = requests.get('https://restcountries.com/v3.1/all')
    countries = response.json()
    country_names = [country['name']['common'] for country in countries]
    if request.method == 'POST':
        register_form = RegistroForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso! Bienvenido.')
            return HttpResponseRedirect('/inicio.html')  
    else:
        register_form = RegistroForm()
    return render(request, 'registro.html', {'register_form': register_form, 'countries': country_names})

@login_required
def user_profile(request):
    subcategorias = Subcategoria.objects.all()
    categorias = Categoria.objects.all()
    productos = Producto.objects.all()
    usuario = request.user
    return render(request, 'user_profile.html', {'usuario': usuario, 'productos': productos, 'categorias': categorias, 'subcategorias': subcategorias})


@login_required
@require_POST
def update_profile(request):
    # Asegúrate de que el usuario esté autenticado
    user = request.user

    # Obtén los datos enviados desde el formulario
    username = request.POST.get('username')
    email = request.POST.get('email')
    first_name = request.POST.get('nombre')
    last_name = request.POST.get('apellidos')
    fecha_nacimiento = request.POST.get('fecha_nacimiento')
    pais = request.POST.get('pais')
    ciudad = request.POST.get('ciudad')
    direccion = request.POST.get('direccion')
    codigo_postal = request.POST.get('codigo_postal')

    profile_image = request.FILES.get('profile_image')
    if profile_image:
        #si habia una imagen de perfil anterior, la borra
        if user.profile_image:
            ruta_imagen = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static', 'profile_images', user.profile_image.url.split('/')[-1]))
            os.remove(ruta_imagen)
        fs = FileSystemStorage()
        filename = fs.save('static/profile_images/' + username + "_"+ str(user.id)+".jpg", profile_image)
        user.profile_image = fs.url(filename)  # Asegúrate de que tu modelo de usuario tenga un campo 'profile_image'
    # Actualiza los datos del usuario
    user.username = username
    user.email = email
    user.nombre = first_name
    user.apellidos = last_name
    user.fecha_nacimiento = fecha_nacimiento
    user.pais = pais
    user.ciudad = ciudad
    user.direccion = direccion
    user.codigo_postal = codigo_postal

    # Guarda los cambios en la base de datos
    user.save()
    profile_image_url = request.user.profile_image.url if request.user.profile_image else None
    # Devuelve una respuesta
    return JsonResponse({'status': 'success', 'profile_image_url': profile_image_url})

@user_passes_test(lambda u: u.is_superuser)
def admin_profile(request):
    usuario = request.user
    return render(request, 'admin_profile.html', {'usuario': usuario})


#----------------VIEWS FOR PRODUCTS MANAGEMENT---------------------------

def inicio(request):
    # Define la cantidad de productos recomendados que deseas mostrar
    cantidad_recomendados = 15
    
    # Obtén los productos con mayor rating_original
    productos_con_alto_rating = Producto.objects.filter(rating_original__isnull=False).order_by('-rating_original')
    productos=Producto.objects.all()
    categorias = Categoria.objects.all()
    subcategorias = Subcategoria.objects.all()
    # Selecciona una muestra aleatoria de productos recomendados
    productos_recomendados = random.sample(list(productos_con_alto_rating), min(cantidad_recomendados, len(productos_con_alto_rating)))
    
    return render(request, 'inicio.html', {'productos_recomendados': productos_recomendados, 'productos': productos, 'categorias': categorias, 'subcategorias': subcategorias})

def search_products(request):
    search_term = request.GET.get('query', '')
    if search_term:
        # Realiza la búsqueda en tu modelo de productos
        matching_products = Producto.objects.filter(
            Q(nombre__icontains=search_term) 
        )
        total_matches = matching_products.count()  # Cuenta el total de coincidencias
        products = matching_products.values('id', 'nombre', 'precio', 'imagen')[:10]  # Limita los resultados a 10

        # Prepara la respuesta
        results = {
            'products': list(products),  # Convierte el QuerySet en una lista para JSON
            'total_matches': total_matches  # Incluye el número total de coincidencias
        }
    else:
        results = {'products': [], 'total_matches': 0}

    return JsonResponse(results)  # Devuelve los resultados como JSON

def producto_detail(request, id):
    producto = Producto.objects.get(pk=id)
    productos=Producto.objects.all()
    categorias = Categoria.objects.all()
    subcategorias = Subcategoria.objects.all()

    return render(request, 'producto.html', {'producto': producto, 'productos': productos, 'categorias': categorias, 'subcategorias': subcategorias})

def categoria_search(request, categoria_slug):

    categoria = Categoria.objects.get(slug=categoria_slug)
    categorias = Categoria.objects.all()
    subcategorias = Subcategoria.objects.all()
    productos = Producto.objects.all()
    if categoria:
        productos = productos.filter(categoria__nombre=categoria)

    order = request.GET.get('order')
    if order == 'asc':
        productos= productos.order_by('precio')
    elif order == 'desc':
        productos = productos.order_by('-precio')
    #elif order == 'relevant':
        # Define cómo quieres ordenar por relevancia
    elif order == 'new':
        productos = productos.order_by('-id')  
    elif order == 'rating':
        productos = productos.order_by('-rating_original')

    paginator = Paginator(productos, 18)  # Muestra 20 productos por página

    page_number = request.GET.get('page')
    productos = paginator.get_page(page_number)
    

    return render(request, 'categorias.html', {'categoria': categoria, 'productos': productos, 'categorias': categorias, 'subcategorias': subcategorias})

def subcategoria_search(request,categoria_slug, subcategoria_slug):
    categoria = Categoria.objects.get(slug=categoria_slug)
    subcategoria = Subcategoria.objects.get(slug=subcategoria_slug)
    subcategorias = Subcategoria.objects.all()
    categorias = Categoria.objects.all()
    productos = Producto.objects.all()

    if subcategoria:
        productos = productos.filter(subcategoria__nombre=subcategoria)

    order = request.GET.get('order')
    if order == 'asc':
        productos= productos.order_by('precio')
    elif order == 'desc':
        productos = productos.order_by('-precio')
    #elif order == 'reviews':
        # Define cómo quieres ordenar por relevancia
    elif order == 'new':
        productos = productos.order_by('-id')  
    elif order == 'rating':
        productos = productos.order_by('-rating_original')

    paginator = Paginator(productos, 18)  # Muestra 20 productos por página

    page_number = request.GET.get('page')
    productos = paginator.get_page(page_number)

    

    return render(request, 'subcategorias.html', {'categoria': categoria,'subcategoria': subcategoria, 'productos': productos, 'categorias': categorias, 'subcategorias': subcategorias})

