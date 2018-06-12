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
#from app.fomularios.erroForm import errorForm

###########################################################
#   Usuario: Erick Sulca, Ulises Bejar
#   Fecha: 01/06/18
#   Última modificación:
#   Descripción: Registra un error en la App Móvil
###########################################################
@csrf_exempt
def registrarError(request):
        if request.method == 'POST':
        	try:
	        	Datos = json.loads(request.body)
	        	usuario=True
       			# usuario= BuscarUsuario(Datos["idUsuario"])
        
        		if usuario==True:
			        oError = Error()
			        oError.descripcion = Datos["descripcion"]
			        oError.actividad = Datos["actividad"]
			        oError.save()
			        return HttpResponse(json.dumps({'exito':1}), content_type="application/json")
        	except Exception as e:
        		print (e)
	        	return HttpResponse(json.dumps({'exito':0}), content_type="application/json")
        else:
	        return HttpResponse(json.dumps({'exito':0}), content_type="application/json")