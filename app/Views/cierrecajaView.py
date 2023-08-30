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
from django.shortcuts import redirect
from app.fomularios.cierrecajaForm import *

def registrarCierrecaja(request):
    if request.method == 'POST':
        Datos = request.POST
        #<QueryDict: {'csrfmiddlewaretoken': ['YKVJuIQSEcRwcEMi1svUtwfgrKnFgGtTT8gUha1kWLZF0sLtdWYlj1OxJ9r2fNqS'], 'fechaApertura': ['16 de agosto de 2023 a las 10:06'], 'idApertura': ['1'], 'monto': ['2'], 'aperturacaja': ['1']}>
        print("############# Datos Func POST: regitrarCierrecaja ###########")
        print(Datos)
        print(Datos['idApertura'])
        idApertura = int(Datos['idApertura'])
        oAperturacaja = Aperturacaja.objects.get(id= idApertura)
        oAperturacaja.activo = False
        oAperturacaja.save()
        oCierrecaja = Cierrecaja()
        oCierrecaja.aperturacaja = oAperturacaja
        oCierrecaja.monto = float(Datos['monto'])
        oCierrecaja.save()
        form = CierrecajaForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            '''try:
                passoAperturacaja = Aperturacaja.objects.get(id=Datos['idApertura'],activo=True)
                form.aperturacaja = oAperturacaja
                form.save()
                oAperturacaja.activo = False
                oAperturacaja.save()
                return render(request, 'caja/cierreRegistrado.html')
                '''
            return render(request, 'caja/cierreRegistrado.html')
        else:
            return render(request, 'caja/cierre.html')
    else:
        oCajas = Caja.objects.filter(estado=True)
        form = CierrecajaForm()
        try:
            oAperturacaja = Aperturacaja.objects.latest('id')
            oMontoCierre = 500
            if  oAperturacaja.activo==True:
                return render(request, 'caja/cierre.html', {'form': form,'Aperturacaja': oAperturacaja,'cajas':oCajas,'oMontoCierre':oMontoCierre})
            else: 
                return redirect('apertura_caja')
        except Exception as e:
            return redirect('apertura_caja')
            #return render(request, 'caja/cierreNoRegistrado.html', {'cajas':oCajas})