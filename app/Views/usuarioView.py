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

@csrf_exempt
def validarUsuario(request):
    if request.method == 'POST':
        Datos = json.loads(request.body)
        print (Datos)
        
        usuario=True:
        # usuario= BuscarUsuario(Datos["idUsuario"])
        
        if usuario==True:
            idEmpleado = Datos["idEmpleado"]
            imei = Datos["imei"]
            Longitud = Datos["coord"]["x"]
            Latitud = Datos["coord"]["y"]
            try:
                oEmpleado = Empleado.objects.get(imei=imei)
                return HttpResponse(json.dumps({'exito':1,"nombre":oEmpleado.nombre,"idEmpleado":oEmpleado.id,"perfil":oEmpleado.perfil}), content_type="application/json")
            except Exception as e:
                return HttpResponse(json.dumps({'exito':0}), content_type="application/json")
            

        #except Exception as e:
        #    return HttpResponse(json.dumps({'exito':0}), content_type="application/json")


