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
        print user
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
    print oCaja
    return HttpResponse(json.dumps({'exito':1}), content_type="application/json")

