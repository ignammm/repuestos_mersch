from django.forms import ModelForm
from django import forms
from .models import Venta
from inventario.models import Producto



class VentaForm(ModelForm):
    class Meta:
        model = Venta
        fields= "__all__"
        
    