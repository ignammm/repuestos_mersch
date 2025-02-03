from django.db import models
from inventario.models import Producto


class Venta(models.Model):
    monto = models.FloatField(default=0, blank=True)
    fecha = models.DateTimeField()
    descripcion = models.TextField(blank=True, null=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1, blank=False, null=False)
    reposicion = models.BooleanField(default=False)

    def __str__(self):
        return f"({self.fecha}) | {self.producto} | ${self.monto}"
