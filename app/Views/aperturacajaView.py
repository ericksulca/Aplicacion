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
from app.fomularios.aperturacajaForm import *

def registrarAperturacaja(request):
    if request.method == 'POST':
        Datos = request.POST
        form = AperturacajaForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            oCaja = Caja()
            oCaja.id = Datos['cmbCaja']
            form.caja = oCaja
            form.save()
            return render(request, 'caja/aperturaRegistrada.html')
        else:
            return render(request, 'caja/apertura.html')
    else:
        oCajas = Caja.objects.filter(estado=True)
        form = AperturacajaForm()
        try:
            oAperturacaja = Aperturacaja.objects.latest('id')
            if  oAperturacaja.activo==True:
                return render(request, 'caja/aperturaRegistrada.html', {'Aperturacaja': oAperturacaja})
        except Exception as e:
            return render(request, 'caja/apertura.html', {'form': form,'cajas':oCajas})