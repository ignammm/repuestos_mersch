from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from apps.articulos.models import ArticuloRSF
from apps.stock.models import ArticuloRSFStock
from .serializers import ArticuloSerializer

def ingersosRSF(request):
    return render(request, 'apps/ingresos/ingresosRSF.html', {})

# 📌 Buscar un artículo por código de barras
@api_view(['GET'])
@permission_classes([AllowAny]) 
def buscar_articulo(request, codigo):
    try:
        if str(codigo).startswith('R'):
            articulo = ArticuloRSF.objects.get(CodigoRSF=codigo)
        else:
            articulo = ArticuloRSF.objects.get(CodigoBarra=codigo)
        serializer = ArticuloSerializer(articulo)
        return Response(serializer.data)
    except ArticuloRSF.DoesNotExist:
        return Response({"error": "Artículo no encontrado"}, status=404)

@api_view(['POST'])
@permission_classes([AllowAny]) 
def guardar_ingreso(request):
    articulos = request.data.get("articulos", [])
    for item in articulos:
        codigoRSF = item.get("CodigoRSF")
        codigo = item.get("CodigoBarra")
        cantidad = int(item.get("cantidad", 1))  # Obtener la cantidad o usar 1 por defecto
        articulo = ArticuloRSF.objects.get(CodigoRSF=codigoRSF).Articulo

        articulo, creado = ArticuloRSFStock.objects.get_or_create(
            codigo_barrasRSF=codigoRSF,
            codigo_barras=codigo,
            articulo=articulo
        )
        articulo.stock += cantidad  # Incrementar en la cantidad especificada
        articulo.save()
        
    return Response({"mensaje": "Ingreso guardado exitosamente"})