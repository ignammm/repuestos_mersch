from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from inventario.models import Producto

def index(request):
    return render(request, "ingresos/index.html", {})


def ingresar_producto(request, producto_id):
    producto = Producto.objects.get(id=producto_id) 
    if request.method == "POST":
        cantidad = int(request.POST.get('cantidad'))
        if cantidad > 0:
            producto.stock += cantidad
            producto.save()
            messages.success(request, f"Se agregó {cantidad} unidades del producto ({producto.codigo}) al stock.")
        else:
            messages.error(request, "La cantidad ingresada debe ser mayor a cero.")
            
        return redirect('inventario:index')       
    return render(request, "ingresos/ingresar.html", {'producto': producto})
