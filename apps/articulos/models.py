from django.db import models

class ArticuloRSF(models.Model):
    MarcaRSF = models.CharField(max_length=50, null=True)
    Articulo = models.CharField(max_length=50, null=True)
    Fabrica = models.CharField(max_length=50, null=True)
    Descripcion = models.TextField(null=True)
    TipoTxt = models.CharField(max_length=50, null=True)
    MarcaOriginal = models.CharField(max_length=50, null=True)
    PrecioLista = models.CharField(max_length=50, null=True)
    PrecioNeto = models.CharField(max_length=50, null=True)
    StockFinal = models.IntegerField(null=True)
    ModuloVenta = models.IntegerField(null=True)
    Rubro =  models.CharField(max_length=50, null=True)
    Segmento =  models.CharField(max_length=50, null=True)
    Enlace = models.CharField(max_length=50, null=True)
    OEM =  models.CharField(max_length=100, null=True)
    CodigoBarra =  models.CharField(max_length=50, null=True)
    CodigoRSF =  models.CharField(max_length=50, null=True)
    
    def __str__(self):
        return f"{self.CodigoRSF} - {self.MarcaOriginal} - {self.Rubro}"
