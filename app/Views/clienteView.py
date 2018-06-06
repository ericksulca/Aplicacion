# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from ferreteria import settings
from django.contrib.auth.decorators import login_required
# Create your views here.
from app.models import *
from django.views.decorators.csrf import csrf_exempt
import json
from app.fomularios.clienteForm import *

@csrf_exempt
def buscarCliente(request):
    if request.method == 'POST':
        Datos = json.loads(request.body)
        # usuario= BuscarUsuario(Datos["idUsuario"])
        nombreCliente = Datos["nombreCliente"]
        if usuario==True:
          jsonfinal = {}
          jsonfinal["clientes"] = []
           try:
              oClientes = Cliente.objects.filter(nombre__icontains=nombreCliente,estado = 1)
                for oCliente in oClientes:
                  jsonCliente = {}
                  jsonCliente["id"] = oCliente.id
                  jsonCliente["direccion"] = oCliente.direccion
                  jsonCliente["nombre"] = oCliente.nombre
                  jsonCliente["numerodocumento"] = oCliente.numerodocumento
                  jsonfinal["clientes"].append(jsonCliente)

                return HttpResponse(json.dumps(jsonfinal), content_type="application/json")
           except Exception as e:
               return HttpResponse(json.dumps({'exito':0}), content_type="application/json")

def detalleCliente(request,cliente_id):
    oCliente = Cliente.objects.get(id=cliente_id,estado=True)
    oPresentaciones = Presentacion.objects.filter(estado=True)
    return render(request, 'cliente/detalle.html', {'oCliente':oCliente})            

@csrf_exempt
def detalleClienteWS(request):
    if request.method == 'POST':
        Datos = json.loads(request.body)
        #try:
          oCliente = Cliente.objects.get(id=idCliente,estado = 1)
          jsonCliente = {}
          jsonCliente["id"] = oCliente.id
          jsonCliente["direccion"] = oCliente.direccion
          jsonCliente["nombre"] = oCliente.nombre
          jsonCliente["numerodocumento"] = oCliente.numerodocumento
          jsonCliente["latitud"] = oCliente.latitud
          jsonCliente["longitud"] = oCliente.longitud
        ############### Calcular ##################
          jsonCliente["LimiteCredito"] = 1200
          jsonCliente["MontoCredito"] = 980.50
          jsonCliente["Pedidos"] = []
          oPedidos = Pedido.objects.filter(cliente=oCliente,estado = True)
         for oPedido in oPedidos:
             jsonPedido = {}
             jsonPedido["fecha"] = oPedido.fecha
             jsonPedido["monto"] = "S/. 251.00"
             jsonCliente["Pedidos"].append(jsonPedido)

           return HttpResponse(json.dumps(jsonCliente), content_type="application/json")
        #except Exception as e:
        #    return HttpResponse(json.dumps({'exito':0}), content_type="application/json")
            

def editarCliente(request,cliente_id):
    oCliente = Cliente.objects.get(id = cliente_id)
    if request.method == 'POST':
        Datos = request.POST
        form = ClienteForm(request.POST or None, instance=oCliente)
        if form.is_valid():
            form = form.save()
            return redirect('/Cliente/listar/')
            
        else:
            return render(request, '/Cliente/error.html')
    else:
        form = ClienteForm(request.POST or None, instance=oCliente)
        return render(request, 'cliente/nuevo.html', {'form': form})

def nuevoCliente(request):
    if request.method == 'POST':
        Datos = request.POST
        form = ClienteForm(request.POST)
        if form.is_valid():
            form = form.save()
            return redirect('/Cliente/listar/')
            
        else:
            return render(request, 'cliente/error.html')
    else:
        form = ClienteForm()
        return render(request, 'cliente/nuevo.html', {'form': form})

def listarCliente(request):
    if request.method == 'GET':
        oClientes = Cliente.objects.filter(estado=True)
        try:
            return render(request, 'cliente/listar.html',{'oClientes':oClientes})
        except Exception as e:
                return render(request, 'cliente/error.html')
    else:
        return render(request, 'cliente/nuevo.html', {})