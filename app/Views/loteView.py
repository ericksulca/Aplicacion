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
            #oPresentacion = Presentacion.objects.get(id = int(Datos['cmbPresentacionPrincipal']))
            #oProducto.presentacions.add(oPresentacion)
            return render(request, 'lote/nuevo.html')
    else:
        form = ProductoForm()
        #oPrecios = Precio.objects.filter(estado=True)
        oAlmacens = Almacen.objects.filter(estado=True)
        oProveedors = Proveedor.objects.filter(estado=True)
    return render(request, 'lote/nuevo.html', {'form': form,'oAlmacens':oAlmacens, 'oProveedors':oProveedors})


