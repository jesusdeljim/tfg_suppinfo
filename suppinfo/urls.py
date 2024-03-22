"""
URL configuration for suppinfo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path

from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio),
    path('inicio.html/', views.inicio),
    path('carga/', views.carga),
    path('registro/', views.registro),
    path('inicio_sesion/', views.inicio_sesion),
    path('cerrar_sesion/', views.cerrar_sesion),
    path('eliminar_base_datos/', views.eliminar_base_datos),
    path('admin_profile/', views.admin_profile),
    path('search/', views.search_products, name='search_products'),
    path('advanced_search/', views.advanced_search, name='advanced_search'),
    path('producto/<int:id>/', views.producto_detail, name='producto_detail'),
    path('categoria/<slug:categoria_slug>/', views.categoria_search, name='categorias'),
    path('categoria/<slug:categoria_slug>/<slug:subcategoria_slug>/', views.subcategoria_search, name='subcategorias'),
    path('mi_cuenta/mis_datos', views.user_profile, name='user_profile'),
    path('mi_cuenta/lista_deseos', views.user_wishlist, name='user_wishlist'),
    path('add-to-wishlist/<int:producto_id>', views.add_to_wishlist, name='agregar_a_lista_deseos'),
    path('remove-from-wishlist/<int:producto_id>', views.remove_from_wishlist, name='quitar_de_lista_deseos'),
    path('mi_cuenta/opiniones', views.user_reviews, name='user_reviews'),
    path('mi_cuenta/mensajes', views.user_messages, name='user_messages'),
    path('mi_cuenta/mensajes/conversation/<int:conversation_id>/', views.view_conversation, name='view_conversation'),
    path('mi_cuenta/mensajes/conversation/<int:conversation_id>/delete/', views.delete_conversation, name='delete_conversation'),
    path('faqs/', views.faqs, name='faqs'),
    path('terminos_y_condiciones/', views.terminos_y_condiciones, name='terminos_y_condiciones'),
    path('politica_de_privacidad/', views.politica_de_privacidad, name='politica_de_privacidad'),
    path('politica_de_cookies/', views.politica_de_cookies, name='politica_de_cookies'),
    path('save_profile_data/', views.update_profile, name='update_profile'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
