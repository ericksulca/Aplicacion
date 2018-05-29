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
from app.fomularios.cierrecajaForm import *

def registrarCierrecaja(request):
    if request.method == 'POST':
        Datos = request.POST
        form = CierrecajaForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            try:
                passoAperturacaja = Aperturacaja.objects.get(id=Datos['idApertura'],activo=True)
                form.aperturacaja = oAperturacaja
                form.save()
                oAperturacaja.activo = False
                oAperturacaja.save()
                return render(request, 'caja/cierreRegistrado.html')
            except Exception as e:
                return render(request, 'caja/cierreNoRegistrado.html')
        else:
            return render(request, 'caja/cierre.html')
    else:
        oCajas = Caja.objects.filter(estado=True)
        form = CierrecajaForm()
        try:
            oAperturacaja = Aperturacaja.objects.latest('id')
            if  oAperturacaja.activo==True:
                return render(request, 'caja/cierre.html', {'form': form,'Aperturacaja': oAperturacaja,'cajas':oCajas})
        except Exception as e:
            return render(request, 'caja/cierreNoRegistrado.html', {'cajas':oCajas})