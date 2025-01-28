from django.forms import ModelForm
from django import forms
from .models import Producto, Categorias


class ProductoForm(ModelForm):
    class Meta:
        model= Producto
        fields= '__all__'
        
    categoria = forms.ModelChoiceField(
        queryset=Categorias.objects.all(),
        empty_label="Selecciona una categoría",
        widget=forms.Select(attrs={'class': 'form-select select2', 'required': True})
    )
        
class CategoriasForm(ModelForm):
    class Meta:
        model= Categorias
        fields= '__all__'
        