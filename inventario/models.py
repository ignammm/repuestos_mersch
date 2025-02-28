from django.db import models


class Categorias(models.Model):
    nombre = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nombre
    
    
class Producto(models.Model):
    codigo = models.CharField(max_length=50)
    stock = models.IntegerField(default=0, blank=True)
    marca = models.CharField(max_length=50, default="---", blank=False, null=False)
    categoria = models.ForeignKey(Categorias, on_delete=models.CASCADE)
    descripcion = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f'({self.codigo})' + self.marca