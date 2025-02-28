from django.db import models

from apps.articulos.models import ArticuloRSF


class Venta(models.Model):
    articulo = models.ForeignKey(ArticuloRSF, on_delete=models.CASCADE, null=True)
    cantidad = models.IntegerField()
    monto_total = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    reposicion = models.BooleanField(default=False)
    observacion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.articulo.codigo_barras} | {self.fecha} | {self.monto_total}"