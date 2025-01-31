from . import views
from django.urls import path

app_name = 'ingresos'


urlpatterns = [
    path('', views.index, name="index"),
    path("ingresar_producto/<int:producto_id>/", views.ingresar_producto, name="ingresar_producto"),

]