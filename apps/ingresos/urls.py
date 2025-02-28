from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('ingresosRSF/', views.ingersosRSF, name='ingresosRSF'),
    path('buscar_articulo/<str:codigo>/', views.buscar_articulo, name='buscar_articulo'),
    path('guardar_ingreso/', views.guardar_ingreso, name='guardar_ingreso'),
]
