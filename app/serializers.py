from rest_framework import serializers

from app.models import (Producto, Alerta,Presentacion,Producto_presentacions)

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        #fields = ('__all__')
        fields = ('id','nombre', 'codigo', 'imagen','precio')

class AlertaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alerta
        fields = ('__all__')

class PresentacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presentacion
        fields = ('nombre', 'codigo')

class Producto_presentacionsSerializer(serializers.ModelSerializer):
    presentacion = PresentacionSerializer(read_only=True,many=False)
    class Meta:
        model = Producto_presentacions
        fields = ('id', 'presentacion', 'precio_compra', 'precio_venta', 'favorito')

