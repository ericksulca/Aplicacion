from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from app.models import *
 
class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = ('nombre','direccion','longitud','latitud','numerodocumento')
        #widgets = {
        #    'password': forms.PasswordInput(),
        #}

