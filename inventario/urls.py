from django.urls import path, include
from . import views


app_name = 'inventario'



urlpatterns = [
    path('', views.index, name="index"),
    path('create_producto/', views.create_producto, name="crear_producto"),
    path('edit_producto/<int:producto_id>', views.edit_producto, name="editar_producto"),
    path('delete_producto/<int:producto_id>/', views.delete_producto, name='eliminar_producto'),
    path('detail_producto/<int:producto_id>/', views.detail_producto, name='detalle_producto'),
    path('create_categoria/<int:return_id>', views.create_categoria, name="crear_categoria"), #Si retorna de la pag categoria/create es 1 si es producto/create es 2
]
