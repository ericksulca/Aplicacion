from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from app.models import *
 
class ProductoForm(ModelForm):
    '''
    Presentacions = forms.ModelMultipleChoiceField(
        queryset=Presentacion.objects.filter(estado=True),
        widget=forms.SelectMultiple(attrs={'v-model':'presentacionesSeleccionadas'})
    )
    '''
    class Meta:
        #oPresentaciones = Producto_presentacions.objects.filter(estado=True)
        model = Producto
        fields = ('nombre','codigo','imagen')
        widgets = {
            'codigo': forms.PasswordInput(),
        }

