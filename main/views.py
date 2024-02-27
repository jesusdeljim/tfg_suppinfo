import os
from re import sub
import shutil
import subprocess
import random

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.core.management import call_command
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
        form = InicioSesionForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenido, {user.username}!')
                return HttpResponseRedirect('/inicio.html')  
            else:
                messages.error(request, 'Credenciales inválidas. Inténtalo de nuevo.')
    else:
        form = InicioSesionForm()
    
    return render(request, 'inicio_sesion.html', {'form': form})

def cerrar_sesion(request):
    logout(request)
    return HttpResponseRedirect('/inicio.html')

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso! Bienvenido.')
            return HttpResponseRedirect('/inicio.html')  
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})

@login_required
def user_profile(request):
    usuario = request.user
    return render(request, 'user_profile.html', {'usuario': usuario})

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


def filter_by_category(request):
    categorias = Categoria.objects.all()
    productos = Producto.objects.all().order_by('categoria')

    selected_category = request.GET.get('category', None)
    if selected_category:
        productos = productos.filter(categoria__nombre=selected_category)

    return render(request, 'filter_by_category.html', {'productos': productos, 'categorias': categorias, 'selected_category': selected_category})

def filter_by_brand(request):
    brands = Marca.objects.all()
    productos = Producto.objects.all().order_by('marca')

    selected_brand = request.GET.get('brand', None)
    if selected_brand:
        productos = productos.filter(marca__nombre=selected_brand)

    return render(request, 'filter_by_brand.html', {'productos': productos, 'brands': brands, 'selected_brand': selected_brand})