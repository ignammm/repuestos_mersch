from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from apps.stock.models import ArticuloRSFStock
from apps.articulos.models import ArticuloRSF

def detalle_articulo(request, codigo_barras):
    
    try:    
        if str(codigo_barras).startswith('R'): #Ingresa por codigoRSF
            articuloRSF = get_object_or_404(ArticuloRSF, CodigoRSF=codigo_barras)
            articulo_stock = get_object_or_404(ArticuloRSFStock, codigo_barrasRSF=codigo_barras)
            return render(request, "apps/articulos/detalle_articulo.html", {"articulo_stock": articulo_stock, "articuloRSF": articuloRSF})
        
        #Codigo de barras original
        articulo_stock = get_object_or_404(ArticuloRSFStock, codigo_barras=codigo_barras)
        articuloRSF = get_object_or_404(ArticuloRSF, CodigoBarra=codigo_barras)
        return render(request, "apps/articulos/detalle_articulo.html", {"articulo_stock": articulo_stock, "articuloRSF": articuloRSF})
    except Http404:
        return HttpResponse("Error: Articulo no encontrado")