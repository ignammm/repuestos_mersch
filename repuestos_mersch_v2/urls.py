from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('articulos/', include('apps.articulos.urls')),
    path('ingresos/', include('apps.ingresos.urls')),
    path('stock/', include('apps.stock.urls')),
    path('ventas/', include('apps.ventas.urls')),
    path('', views.index, name='index'),
]
