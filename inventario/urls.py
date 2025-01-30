from django.urls import path, include
from . import views


app_name = 'inventario'



urlpatterns = [
    path('', views.index, name="index"),
    path('create_producto/', views.create_producto, name="crear_producto"),
    path('edit_producto/<int:id_producto>', views.edit_producto, name="editar_producto"),
    path('eliminar/<int:producto_id>/', views.delete_producto, name='eliminar_producto'),
    path('create_categoria/', views.create_categoria, name="crear_categoria"),
]
