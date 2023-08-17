# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.generics import (ListAPIView)
from ferreteria import settings
from django.contrib.auth.decorators import login_required
# Create your views here.
from app.models import *
from django.views.decorators.csrf import csrf_exempt
import json
from app.fomularios.productoForm import *
from django.shortcuts import redirect

def listarOperacions(request):
    if request.method == 'POST':
        return render(request, 'caja/operacion_listar.html')
    if request.method == 'GET':
        oOperacions = Operacion.objects.filter(estado = True).order_by('-id')
        return render(request, 'caja/operacion_listar.html', {"oOperacions": oOperacions})


def registrarOperacion(request):
    if request.method == 'POST':
        Datos = request.POST
        print(Datos)
        oOperacion = Operacion()
        oOperacion.monto = float(Datos['txtMontoOperacion'])
        oOperacion.descripcion = Datos['txtDesoperacion']
        #funcion estado Caja Activo: true | false
        oAperturacaja = Aperturacaja.objects.latest('id')
        if  oAperturacaja.activo==True:
                return render(request, 'caja/aperturaRegistrada.html', {'Aperturacaja': oAperturacaja})
        if  oAperturacaja.activo==False:
            return redirect('apertura_caja')
        idTipoOP = int(Datos['cmbDetalleTipoOperacion'])
        oDetalletipooperacion = Detalletipooperacion.objects.get(id=idTipoOP)

        oOperacion.detalletipooperacion = oDetalletipooperacion
        oOperacion.save()
        return redirect('listar_lote')
    else:
        try:
            oTipooperacion = Tipooperacion.objects.filter(estado=1)
            return render(request, 'caja/operacion.html', {'oTipooperacion':oTipooperacion})
        except Exception as e:
            return render(request, 'caja/operacion2.html', {})

from app.serializers import detalleTipoOperacionSerializer
class get_detalleTipoOperacion(ListAPIView):
    serializer_class = detalleTipoOperacionSerializer
    def get_queryset(self,*args, **kwargs):
        kword = self.request.query_params.get('pk', '')
        oPresentaciones = Detalletipooperacion.objects.filter(estado = True,tipooperacion=kword)
        return oPresentaciones