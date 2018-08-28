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
from app.fomularios.rutaForm import *
###########################################################
#   Usuario: Erick Sulca, Ulises Bejar
#   Fecha: 05/06/18
#   Última modificación:
#   Descripción: 
#   servicio de busqueda de usuario para la app movil
###########################################################

@csrf_exempt
def rutaUsuario(request):
    if request.method == 'POST':
        Datos = json.loads(request.body)
        print (Datos)
        usuario=True
       # usuario= BuscarUsuario(Datos["idUsuario"])
        
        if usuario==True:
            idEmpleado = Datos["idEmpleado"]
            #try:
            oEmpleado = Empleado.objects.get(id=idEmpleado)
            oVisitas = Visita.objects.filter(estado = True, empleado = oEmpleado, nivel=oEmpleado.perfil)
            jsonfinal = {}
            jsonfinal["rutas"] = []
            for oVisita in oVisitas:
                rutasJson = {}
                rutasJson["x"]= oVisita.rutacliente.cliente.longitud
                rutasJson["y"]= oVisita.rutacliente.cliente.latitud
                rutasJson["activo"]= oVisita.activo
                rutasJson["idCliente"]= oVisita.rutacliente.cliente.id
                rutasJson["idVisita"]= oVisita.id
                rutasJson["idPedido"]= 4
                jsonfinal["rutas"].append(rutasJson)
            return HttpResponse(json.dumps(jsonfinal), content_type="application/json")


def nuevaRuta(request):
    if request.method == 'POST':
        Datos = request.POST
        form = RutaForm(request.POST)
        if form.is_valid():
            form = form.save()
            return redirect('/ruta/listar/')
            
        
    else:
        form = RutaForm()
        return render(request, 'ruta/nuevo.html', {'form': form})

def listarRuta(request):
    if request.method == 'GET':
        oRuta = Rutaclientes.objects.filter(estado=True)

        return render(request, 'ruta/listar.html',{'oRuta':oRuta})

    else:
        return render(request, 'ruta/nuevo.html', {})