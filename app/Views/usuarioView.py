# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from ferreteria import settings
from django.contrib.auth.decorators import login_required
# Create your views here.
from app.models import *
from app.views import *
from django.views.decorators.csrf import csrf_exempt
import json
from app.fomularios.aperturacajaForm import *

###########################################################
#   Usuario: Erick Sulca, Ulises Bejar
#   Fecha: 05/06/18
#   Última modificación:
#   Descripción:
#   servicio de busqueda de usuario para la app movil
###########################################################

@csrf_exempt
def validarUsuario(request):
   

    if request.method == 'POST':
        Datos = json.loads(request.body)
        print (Datos)
        usuario=True
        # usuario= BuscarUsuario(Datos["idUsuario"])
        
        if usuario==True:
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
            

def errorView(request):

        if request.method == 'POST':
            form = errorForm(request.Post)
            if form.is_valid():
                form.save()
            return redirect('error : index')

        else:
            form = errorForm()
        return  render(request, 'login.html', {'form':form})
