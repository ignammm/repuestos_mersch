from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('detalle_articulo/<str:codigo_barras>', views.detalle_articulo, name='detalle_articulo')
    
]
