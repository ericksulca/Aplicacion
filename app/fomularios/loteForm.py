from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from app.models import *
 
class LoteForm(ModelForm):
    class Meta:
        model = Lote
        fields = ('proveedor')
        #widgets = {
        #    'password': forms.PasswordInput(),
        #}

