# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from ferreteria import settings
from django.contrib.auth.decorators import login_required
# Create your views here.
from app.models import *
from django.views.decorators.csrf import csrf_exempt
import json
from app.fomularios.productoForm import *

def registrarOperacion(request):
    if request.method == 'POST':
        Datos = request.POST
        print (Datos)
        form = request.POST
        if form:
            return render(request, 'caja/aperturaRegistrada.html')
        else:
            return render(request, 'caja/apertura.html')
    else:
        try:
            oTipooperacion = Tipooperacion.objects.filter(estado=1)
            oDetalletipooperacion = Detalletipooperacion.objects.filter(tipooperacion=2)
            print (oTipooperacion)
            print (oDetalletipooperacion)
            return render(request, 'caja/operacion.html', {'oTipooperacion':oTipooperacion,'oDetalletipooperacions':oDetalletipooperacion})
        except Exception as e:
            return render(request, 'caja/operacion2.html', {})