from django.shortcuts import redirect, render
from django.http import HttpResponse

from inventario.forms import CategoriasForm, ProductoForm


def create_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crear_producto')  
    else:
        form = ProductoForm()
    return render(request, 'inventario/productos/create.html', {'form': form})
    

def create_categoria(request):
    if request.method == 'POST':
        form = CategoriasForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_categorias')
    else:
        form = CategoriasForm()
    return render(request, 'inventario/categorias/create.html', {'form': form})