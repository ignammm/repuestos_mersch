from rest_framework import serializers
from apps.articulos.models import ArticuloRSF

class ArticuloSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticuloRSF
        fields = '__all__'
