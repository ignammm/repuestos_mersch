from django.urls import path
from . import views

app_name = 'ventas'

urlpatterns = [
    path('', views.index, name='index'),
    path('carrito_ventas/', views.carrito_ventas, name='carrito_ventas'),
    path('agregar-producto/', views.agregar_producto, name='agregar_producto'),
    path('eliminar-producto/<str:codigo>/', views.eliminar_producto, name='eliminar_producto'),
    path('finalizar-venta/', views.finalizar_venta, name='finalizar_venta'),
    path('informe_ventas/', views.informe_ventas, name="informe_ventas"),
]
