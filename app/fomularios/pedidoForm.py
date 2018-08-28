from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from app.models import *
#from django.forms.models import inlineformset_factory, modelform_factory



class PedidoproductospresentacionsForm(ModelForm):
    class Meta:
        model = Pedidoproductospresentacions
        fields=['cantidad', 'pedido']
        def __str__(self):
            return '%s' % self.pedido.cliente

class ProductopresentacionsForm(ModelForm):
    class Meta:
        model = Productopresentacions
        fields=['producto', 'presentacion']