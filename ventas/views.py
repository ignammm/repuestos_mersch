from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from datetime import datetime
from django.core.paginator import Paginator

from inventario.models import Producto
from ventas.forms import VentaForm
from .models import Venta


def index(request):
    ventas_list = Venta.objects.all().order_by('-id')

    estado_str = request.GET.get('estado', '')
    estado = int(estado_str) if estado_str.isdigit() else None

    codigo = request.GET.get('codigo', '')
    fecha_inicio = request.GET.get('fecha_inicio', '')
    fecha_fin = request.GET.get('fecha_fin', '')

    if estado is not None:
        ventas_list = ventas_list.filter(reposicion=estado)
    if codigo:
        ventas_list = ventas_list.filter(producto__codigo__icontains=codigo)
    if fecha_inicio and fecha_fin:
        ventas_list = ventas_list.filter(fecha__range=[fecha_inicio, fecha_fin])
    elif fecha_inicio:
        ventas_list = ventas_list.filter(fecha__gte=fecha_inicio)
    elif fecha_fin:
        ventas_list = ventas_list.filter(fecha__lte=fecha_fin)

    productos = Producto.objects.all()
    paginator = Paginator(ventas_list, 7)
    page_number = request.GET.get('page')
    ventas = paginator.get_page(page_number)

    return render(request, "ventas/index.html", {
        'ventas': ventas,
        'productos': productos,
        'fecha_actual': datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    })

    

def crear(request):
    
    if request.method == 'POST':  
        cantidad = int(request.POST.get('cantidad'))
        producto_id = request.POST.get('producto_id')
        monto = request.POST.get('monto')
        fecha_actual = request.POST.get('fecha')
        
        if cantidad <= 0:
            messages.error(request, "No puede vender 0 cantidades.")
            return redirect('ventas:index')
        
        if producto_id:  
            
            try:
                producto = Producto.objects.get(id=producto_id) 
                
                if producto.stock < int(cantidad):
                    messages.error(request, "No puede vender una cantidad mayor a la que tiene en stock.")
                    return redirect('ventas:index')
                
                producto.stock -= int(cantidad) 
                producto.save()
                
            except Producto.DoesNotExist:
                messages.error(request, "Producto no encontrado.") 
                return redirect('ventas:index')

            venta = Venta(
                cantidad=cantidad,
                producto=producto,
                monto=monto,
                fecha=fecha_actual
            )
            venta.save()  
            messages.success(request, "Se ha registrado la venta correctamente.")
            return redirect('ventas:index')
        
        else:
            messages.error(request, "Debe seleccionar un producto.")
            return redirect('ventas:index')

    return render(request, "ventas/index.html", {})

def buscar_productos(request):
    codigo = request.GET.get("codigo", "").strip()
    productos = Producto.objects.filter(codigo__icontains=codigo)[:5]  # Ajusta el filtro según tu modelo
    productos_data = [
        {"id": p.id, "codigo": p.codigo, "marca": p.marca, "cantidad": p.stock}
        for p in productos
    ]
    return JsonResponse({"productos": productos_data})

def reponer_producto(request, venta_id):
    if request.method == "POST":
        estado_reposicion = request.POST.get('reposicion')
        venta = Venta.objects.get(id=venta_id)
        venta.reposicion = int(estado_reposicion) 
        venta.save()
        return JsonResponse({"success": True}) 
    
    return JsonResponse({"success": False, "error": "Método no permitido"}, status=400)
    


    
    
    