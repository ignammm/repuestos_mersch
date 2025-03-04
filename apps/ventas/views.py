from datetime import datetime, timezone
import math
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from apps.articulos.models import ArticuloRSF
from apps.stock.models import ArticuloRSFStock
from apps.ventas.models import Venta
from django.db.models import Sum
from django.shortcuts import render
from django.utils import timezone
from datetime import datetime

def index(request):
    ventas_list = Venta.objects.all().order_by('-fecha')

    # Filtros
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    codigo = request.GET.get('codigo')
    reposicion = request.GET.get('reposicion')

    if fecha_inicio:
        ventas_list = ventas_list.filter(fecha__gte=datetime.strptime(fecha_inicio, '%Y-%m-%d'))
    if fecha_fin:
        ventas_list = ventas_list.filter(fecha__lte=datetime.strptime(fecha_fin, '%Y-%m-%d'))
    if codigo:
        ventas_list = ventas_list.filter(articulo__Articulo__icontains=codigo)
    if reposicion == "Sí":
        ventas_list = ventas_list.filter(reposicion=True)
    elif reposicion == "No":
        ventas_list = ventas_list.filter(reposicion=False)

    # Paginación
    paginator = Paginator(ventas_list, 7)  # 10 ventas por página
    page_number = request.GET.get('page')
    ventas = paginator.get_page(page_number)

    # Mantener parámetros de consulta en la paginación
    query_params = "&".join([f"{k}={v}" for k, v in request.GET.items() if k != 'page'])

    return render(request, 'apps/ventas/index.html', {
        'ventas': ventas,
        'query_params': query_params
    })

def carrito_ventas(request):
    carrito = request.session.get('carrito', [])
    total = sum(math.trunc(item['precio'] * int(item['cantidad'])) for item in carrito)
    return render(request, 'apps/ventas/carrito_ventas.html', {'carrito': carrito, 'total': total})


def agregar_producto(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo_barra')
        cantidad = int(request.POST.get('cantidad', 1))

        # Verificar si el artículo existe según el código
        try:
            if str(codigo).startswith('R'):
                articulo = get_object_or_404(ArticuloRSF, CodigoRSF=codigo)
                articulo_stock = get_object_or_404(ArticuloRSFStock, codigo_barrasRSF=codigo)
            else:
                articulo = get_object_or_404(ArticuloRSF, CodigoBarra=codigo)
                articulo_stock = get_object_or_404(ArticuloRSFStock, codigo_barras=codigo)
        except Exception as e:
            return HttpResponse("El artículo no existe o no tiene stock.", status=404)

        # Verificar que haya stock suficiente
        if articulo_stock.stock < cantidad:
            return HttpResponse("No hay stock suficiente para este artículo.", status=400)

        precio_iva = float(str(articulo.PrecioNeto).replace(',', '.')) + float(str(articulo.PrecioNeto).replace(',', '.'))*0.21
        precio_bruto = precio_iva + precio_iva*0.40
        
        # Cargar o actualizar el carrito
        carrito = request.session.get('carrito', [])
        if isinstance(carrito, dict):
            carrito = list(carrito.values())
            
        for item in carrito:
            if item['codigo'] == articulo.CodigoBarra or item['codigo'] == articulo.CodigoRSF:
                item['cantidad'] += cantidad
                item['articulo_total'] = float(item['precio']) * item['cantidad']
                break
        
        else:   
            carrito.append({
                'codigo': codigo,
                'nombre': articulo.TipoTxt,
                'precio': math.trunc(precio_bruto),
                'cantidad': cantidad,
                'articulo_total': math.trunc(precio_bruto * cantidad),
            })
            
        articulo_stock.stock -= cantidad
        articulo_stock.save()

        request.session['carrito'] = carrito
        return redirect('ventas:carrito_ventas')


def eliminar_producto(request, codigo):
    carrito = request.session.get('carrito', [])

    # Buscar el producto en el carrito
    for item in carrito:
        if item['codigo'] == codigo:
            cantidad_eliminada = item['cantidad']  # Asegúrate de que 'cantidad' está en el carrito
            
            # Obtener el producto en la base de datos y actualizar stock
            if str(codigo).startswith('R'):
                articulo_stock = get_object_or_404(ArticuloRSFStock, codigo_barrasRSF=codigo)
            else:
                articulo_stock = get_object_or_404(ArticuloRSFStock, codigo_barras=codigo)
      
            articulo_stock.stock += cantidad_eliminada
            articulo_stock.save()
            break  # Salir después de encontrar el producto

    # Filtrar el carrito para eliminar el producto
    carrito = [item for item in carrito if item['codigo'] != codigo]
    request.session['carrito'] = carrito

    return redirect('ventas:carrito_ventas')

def finalizar_venta(request):
    carrito = request.session.get('carrito', {})
    if not carrito:
        return JsonResponse({"error": "El carrito está vacío"}, status=400)

    try:
        for item in carrito:
            codigo = item['codigo']

            if str(codigo).startswith('R'):
                articulo = ArticuloRSF.objects.get(CodigoRSF=codigo)
                articulo_stock = ArticuloRSFStock.objects.get(codigo_barrasRSF=codigo)
            else:
                articulo = ArticuloRSF.objects.get(CodigoBarra=codigo)
                articulo_stock = ArticuloRSFStock.objects.get(codigo_barras=codigo)
                
                
            precio_iva = float(str(articulo.PrecioNeto).replace(',', '.')) + float(str(articulo.PrecioNeto).replace(',', '.'))*0.21
            precio_bruto = precio_iva + precio_iva*0.40
        
            # Guardar la venta
            Venta.objects.create(
                articulo=articulo,
                cantidad=int(item['cantidad']),
                monto_total=int(item['cantidad']) * precio_bruto,
            )

            # Descontar del stock
            articulo_stock.stock -= int(item['cantidad'])
            articulo.save()

        # Vaciar el carrito
        request.session['carrito'] = {}
        return redirect('ventas:carrito_ventas')  # Redirige al carrito o a donde quieras
    except ArticuloRSFStock.DoesNotExist:
        return JsonResponse({"error": "Un artículo del carrito no existe"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    


def informe_ventas(request):
    total_ventas = 0  # Inicializa la variable para evitar errores en la plantilla

    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    if fecha_inicio and fecha_fin:
        try:
            # Convertir string a datetime
            fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')

            # Hacer las fechas "timezone-aware" para evitar el warning
            fecha_inicio = timezone.make_aware(fecha_inicio)
            fecha_fin = timezone.make_aware(fecha_fin)

            # Obtener la suma total del monto_total de las ventas en el rango de fechas
            total_ventas = Venta.objects.filter(fecha__range=[fecha_inicio, fecha_fin]).aggregate(Sum('monto_total'))['monto_total__sum']
            
            # Si no hay ventas, evitar que devuelva None y en su lugar devolver 0
            total_ventas = total_ventas if total_ventas is not None else 0

        except ValueError:
            total_ventas = 0  # En caso de error en la conversión

    return render(request, 'apps/ventas/informe_ventas.html', {'total_ventas': total_ventas})
