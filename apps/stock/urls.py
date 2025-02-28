from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('consultar_articulo/', views.consultar_articulo, name='consultar_articulo'),
]
