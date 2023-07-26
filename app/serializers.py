from rest_framework import serializers

from app.models import (Producto, Alerta)

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        #fields = ('__all__')
        fields = ('id','nombre', 'codigo', 'imagen')

class AlertaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alerta
        fields = ('__all__')
