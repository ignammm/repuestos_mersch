from django.urls import path
from . import views


app_name = 'ventas'


urlpatterns = [
    path('', views.index, name="index"),
    path('crear/', views.crear, name="crear"),
    path('buscar_productos/', views.buscar_productos, name='buscar_productos'),
    path('reponer_producto/<int:venta_id>/', views.reponer_producto, name='reponer_producto'),
]
