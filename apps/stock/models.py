from django.db import models

class ArticuloRSFStock(models.Model):
    codigo_barrasRSF = models.CharField(max_length=50, null=True)
    codigo_barras = models.CharField(max_length=100, null=True)
    articulo = models.CharField(max_length=100, null=True)
    stock = models.IntegerField(default=0)
    
