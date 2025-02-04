from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.core.paginator import Paginator

from inventario.forms import CategoriasForm, ProductoForm
from inventario.models import Producto, Categorias


def index(request):
    
    productos_list = Producto.objects.all().order_by('-id') 

    codigo = request.GET.get('codigo', '')
    marca = request.GET.get('marca', '')
    categoria_id = request.GET.get('categoria', '')

    if codigo:
        productos_list = productos_list.filter(codigo__icontains=codigo)
    if marca:
        productos_list = productos_list.filter(marca__icontains=marca)
    if categoria_id:
        productos_list = productos_list.filter(categoria_id=categoria_id)

    paginator = Paginator(productos_list, 6)  
    page_number = request.GET.get('page')
    productos = paginator.get_page(page_number)

    categorias = Categorias.objects.all() 
    return render(request, 'inventario/productos/index.html', {
        'productos': productos,
        'categorias': categorias,
        'codigo': codigo,
        'marca': marca,
        'categoria_id': categoria_id
    })

def create_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, ("Producto creado correctamente!"))
            return redirect('inventario:crear_producto')  
    else:
        form = ProductoForm()
    return render(request, 'inventario/productos/create.html', {'form': form})
    
    
def edit_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)  

    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, ("Producto editado correctamente!"))
            return redirect('inventario:index')  
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'inventario/productos/edit.html', {'form': form, 'producto': producto})

def delete_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.delete()
    messages.success(request, "Producto eliminado correctamente.")
    return redirect('inventario:index') 

def detail_producto(request, producto_id,):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'inventario/productos/detail.html', {'producto': producto})

def create_categoria(request, return_id):
    dir_template = ''
    if request.method == 'POST':
        form = CategoriasForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, ("Categoría creada correctamente!"))
    else:
        form = CategoriasForm()
    
    if return_id == 1:
        dir_template = 'inventario/categorias/create.html'
    elif return_id == 2:
        dir_template = 'inventario/productos/create.html'
        
    
    return render(request, dir_template, {'form': form})