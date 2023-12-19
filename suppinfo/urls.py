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
    path('filter_by_category/', views.filter_by_category),
    path('filter_by_brand/', views.filter_by_brand),
    path('registro/', views.registro),
    path('inicio_sesion/', views.inicio_sesion),
    path('cerrar_sesion/', views.cerrar_sesion),
    path('eliminar_base_datos/', views.eliminar_base_datos),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
