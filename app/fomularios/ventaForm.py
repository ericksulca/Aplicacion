from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from app.models import *


class VentaForm(ModelForm):
    class Meta:
        model = Venta
        fields = ('monto','recibo','pedido','cliente')