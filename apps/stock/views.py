from django.shortcuts import render, get_object_or_404
from apps.stock.models import ArticuloRSFStock
from apps.articulos.models import ArticuloRSF
from django.core.paginator import Paginator

def consultar_articuloRSF(request):
    return render(request, 'apps/stock/consultar_articuloRSF.html', {})

def consultar_articulo(request):
    articulos = ArticuloRSFStock.objects.all().order_by('-id')
    codigo_barras = request.GET.get('codigo_barras', '')
    nombre_articulo = request.GET.get('nombre_articulo', '')
    stock = request.GET.get('stock', '')

    if codigo_barras:
        articulos = articulos.filter(codigo_barras__icontains=codigo_barras)
    if nombre_articulo:
        articulos = articulos.filter(articulo__icontains=nombre_articulo)  # Ajusta si el campo es diferente
    if stock:
        articulos = articulos.filter(stock__lte=stock)  # Filtra por stock mayor o igual

    # Paginación
    paginator = Paginator(articulos, 10)  # 10 artículos por página
    page = request.GET.get('page')
    articulos_paginados = paginator.get_page(page)

    return render(request, 'apps/stock/consultar_articulo.html', {'articulos': articulos_paginados})
