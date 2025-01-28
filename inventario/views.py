from django.shortcuts import redirect, render
from django.http import HttpResponse

from inventario.forms import ProductoForm


def create(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            # return redirect('listar_productos')  
    else:
        form = ProductoForm()
    return render(request, 'inventario/create.html', {'form': form})
    


