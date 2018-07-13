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


###########################################################
#   Usuario: Erick Sulca, ulises bejar
#   Fecha: 31/08/18
#   Última modificación: 31/08/18
#   Descripción: autentica al usuario
###########################################################
def Login(request):
    next = request.GET.get('next', '/Home/')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
<<<<<<< HEAD
=======
        print (user)
>>>>>>> 3b62b76c741e4e54513c1ff5261d721910778a2f
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(next)
            else:
                return HttpResponse("Inactive user.")
        else:
            return HttpResponseRedirect(settings.LOGIN_URL)

    return render(request, "login/login.html", {'redirect_to': next})

def Logout(request):
    logout(request)
    return HttpResponseRedirect(settings.LOGIN_URL)

@login_required
def Home(request):
    return render(request, "inicio/index.html", {'redirect_to': next})

def Prueba(request):
    oCaja = Caja.objects.filter(estado=1)
    print (oCaja)
    return HttpResponse(json.dumps({'exito':1}), content_type="application/json")


def BucarUsuario(idUsuario):
    oUsuario = Empleado.objects.filter(id = idUsuario)
    if oUsuario.count():
        resultado = True
    else:
        resultado = False
    return resultado

def BucarUsuario(id):
    oUsuario = Empleado.objects.filter(id = id)
    if oUsuario.count():
        resultado = True
    else:
        resultado = False
    return resultado


