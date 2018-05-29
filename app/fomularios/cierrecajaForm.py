from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from app.models import *

class CierrecajaForm(ModelForm):
    class Meta:
        model = Cierrecaja
        fields = ('monto',)
        #widgets = {
        #    'password': forms.PasswordInput(),
        #}

