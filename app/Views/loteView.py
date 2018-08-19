from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from ferreteria import settings
from django.contrib.auth.decorators import login_required
# Create your views here.
from app.models import *
from app.views import *
from ferreteria.urls import *
from django.views.decorators.csrf import csrf_exempt
import json
from app.fomularios.productoForm import *

def nuevoLote(request):

    if request.method == 'POST':
        Datos = request.POST
        form = ProductoForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            oProducto = form
            oPresentacion = Presentacion.objects.get(id = int(Datos['cmbPresentacionPrincipal']))
            oProducto.presentacions.add(oPresentacion)
            oProductopresentacions = Productopresentacions.objects.get(producto=oProducto, presentacion=oPresentacion)
            oProductopresentacions.valor = 1
            oProductopresentacions.unidadprincipal = True
            oProductopresentacions.save()
            oPrecios = Precio.objects.filter(estado=1)
            for oPrecio in oPrecios:
                oProductoPresentacionsprecios = Productopresentacionsprecios()
                oProductoPresentacionsprecios.precio = oPrecio
                oProductoPresentacionsprecios.productopresentacions = oProductopresentacions
                idPrecio = str(oPrecio.id)
                oProductoPresentacionsprecios.valor = Datos[idPrecio]
                oProductoPresentacionsprecios.save()
            return render(request, 'lote/lote.html')


    else:
        form = ProductoForm()
        oPrecios = Precio.objects.filter(estado=True)
        oPresentaciones = Presentacion.objects.filter(estado=True)
    return render(request, 'lote/lote.html', {'form': form,'precios':oPrecios,'presentaciones':oPresentaciones})


