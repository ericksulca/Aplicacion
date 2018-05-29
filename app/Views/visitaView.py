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

@csrf_exempt
def cancelarVisita(request):
    if request.method == 'POST':
        Datos = json.loads(request.body)
        try:
            idEmpleado = Datos["idEmpleado"]
            oEmpleado = Empleado()
            oEmpleado.id = idEmpleado
            idVisita = Datos["idVisita"]
            oVisita = Visita.objects.get(id=idVisita,empleado = oEmpleado)
            oVisita.activo = False
            oVisita.save()

            return HttpResponse(json.dumps({'exito':1}), content_type="application/json")
        except Exception as e:
            return HttpResponse(json.dumps({'exito':0}), content_type="application/json")


def reiniciarVisita(request):
    if request.method == 'GET':
        try:
            oVisitas = Visita.objects.filter(activo = False)
            for oVisita in oVisitas:
                oVisita.activo = True
                oVisita.save()

            return HttpResponse(json.dumps({'exito':1}), content_type="application/json")
        except Exception as e:
            return HttpResponse(json.dumps({'exito':0}), content_type="application/json")
