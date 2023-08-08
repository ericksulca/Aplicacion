from rest_framework import serializers

from app.models import (Producto, Alerta,Presentacion)

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        #fields = ('__all__')
        fields = ('id','nombre', 'codigo', 'imagen')

class AlertaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alerta
        fields = ('__all__')

class PresentacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presentacion
        fields = ('nombre', 'codigo')
