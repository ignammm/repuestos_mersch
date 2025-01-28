from django.urls import path, include
from . import views

urlpatterns = [
    path('create_producto/', views.create_producto, name="crear_producto"),
    path('create_categoria/', views.create_categoria, name="crear_categoria"),
]
