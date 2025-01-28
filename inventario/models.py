from django.db import models


class Producto(models.Model):
    codigo = models.CharField(max_length=50)
    stock = models.IntegerField(default=0, blank=True)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    categoria = models.CharField(max_length=50, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f'({self.codigo})' + self.nombre
    

    
        
