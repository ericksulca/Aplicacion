# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from ferreteria import settings
from django.contrib.auth.decorators import login_required

#from rest_framework.views import APIView, ListAPIView

from rest_framework.generics import (
	ListAPIView,
	CreateAPIView,
)
#from django.views.generic import (ListView, ListAPIView)
# Create your views here.
from app.models import *
from app.views import *
from django.views.decorators.csrf import csrf_exempt
import json

from app.serializers import AlertaSerializer
from app.fomularios.cierrecajaForm import *
from app.fomularios.pedidoForm import *

###########################################################
#   Usuario: Erick Sulca, Ulises Bejar
#   Fecha: 05/06/18
#   Última modificación:
#   Descripción:
#   servicio de busqueda de usuario para la app movil
###########################################################

def registrarPedido(request):
    if request.method == 'POST':
        return render(request, 'caja/cierre.html')
    else:
        return render(request, 'pedido/nuevo.html', {})
        #return render(request, 'venta/prueba.html', {})
        #
def ListarPedidos(request):
    if request.method == 'POST':
        return render(request, 'pedido/listar.html')
    else:
        oPedidos = Pedido.objects.filter(estado = True)
        return render(request, 'pedido/listar.html', {"oPedidos": oPedidos})
        #return render(request, 'venta/prueba.html', {})

def ResumenPedidos(request):
    if request.method == 'POST':
        return render(request, 'pedido/listar.html')
    else:
        oPedidos = Pedido.objects.filter(estado = True)
        oProductos = []
            #oPedidoproductospresentacions = Pedidoproductospresentacions.objects.filter(pedido = oPedido)
            #for oPedidoproductospresentacion in oPedidoproductospresentacions:

        return render(request, 'pedido/resumen.html', {"oProductos": oProductos})

@csrf_exempt
def DetallePedidoMovil(request):
    if request.method == 'POST':
        Datos = json.loads(request.body)
        usuario=True
        # usuario= BuscarUsuario(Datos["idUsuario"])
        if usuario==True:
            idPedido = Datos["idPedido"]
            oPedido = Pedido.objects.get(id = idPedido)
            jsonPedidos = {}
            jsonPedidos["productos"] = []
             
            return HttpResponse(json.dumps(jsonPedidos), content_type="application/json")

def DetallePedido(request,pedido_id):
    if request.method == 'GET':
        idPedido = int(pedido_id)
        oPedido = Pedido.objects.get(id = idPedido)
        #oPedidoproductospresentacions = Pedidoproductospresentacions.objects.filter(pedido = oPedido)
        oProductos = []
        
        return render(request, 'pedido/detalle.html', {"oCliente": oPedido.cliente, "oProductos": oProductos})
    else:
        oPedidos = Pedido.objects.filter(estado = True)
        return render(request, 'pedido/listar.html',{"oPedidos": oPedidos})

@csrf_exempt
def InstarPedido(request):
    if request.method=='POST':
        Datos = json.loads(request.body)
        # usuario= BuscarUsuario(Datos["idUsuario"])
        idEmpleado = Datos["idEmpleado"]
        oEmpleado = Empleado.objects.get(id= idEmpleado)
        idCliente = Datos["idCliente"]
        oCliente = Cliente.objects.get(id= idCliente)

        oPedido = Pedido()
        oPedido.empleado = oEmpleado
        oPedido.cliente = oCliente
        oPedido.save()
        oPedidoProductos = Datos["oPedidoProductos"]
        #for oPedidoProducto in oPedidoProductos:
            #oPedidoproductospresentacions = Pedidoproductospresentacions()
            #oPedidoproductospresentacions.valor = oPedidoProducto["valor"]
            #oPedidoproductospresentacions.cantidad = oPedidoProducto["cantidad"]
            #oPedidoproductospresentacions.pedido = oPedido
            #oPedidoproductospresentacions.productopresentacions = oProductopresentacions
            #oPedidoproductospresentacions.save()
        return HttpResponse(json.dumps({'exito':1,"idPedido": oPedido.id}), content_type="application/json")


@csrf_exempt
def ListarPedido(request):
    if request.method == 'POST':
        Datos = json.loads(request.body)
        usuario=True
        # usuario= BuscarUsuario(Datos["idUsuario"])
        if usuario==True:
            fecha = Datos["fecha"]
            idEmpleado = Datos["idEmpleado"]
            jsonPedidos = {}
            jsonPedidos["pedidos"] = []
            TotalPedidos = 0

            #oPedidos = Pedido.objects.filter(estado = True,fecha = fecha, empleado = idEmpleado)
            oPedidos = Pedido.objects.filter(estado = True, empleado = idEmpleado)
            for oPedido in oPedidos:
                jsonPedido = {}
                jsonPedido["idPedido"] = oPedido.id
                jsonPedido["fecha"] = str(oPedido.fecha)
                jsonPedido["cliente"] = oPedido.cliente.nombre
                jsonPedido["productos"] = []
                #oPedidoproductospresentacions = Pedidoproductospresentacions.objects.filter(pedido=oPedido)
                TotalPedido = 0
                #for oPedidoproductospresentacion in oPedidoproductospresentacions:

                TotalPedidos = TotalPedidos +TotalPedido
                jsonPedido["TotalPedido"] = TotalPedido

                jsonPedidos["pedidos"].append(jsonPedido)
            jsonPedidos["TotalPedidos"] = TotalPedidos
            return HttpResponse(json.dumps(jsonPedidos), content_type="application/json")

#def Listar_PedidoAlerta(request):
class Listar_PedidoAlertaView(ListAPIView):
	serializer_class = AlertaSerializer
	
	def get_queryset(self):
		kword = self.request.query_params.get('kword', '')
		oAlertas = Alerta.objects.filter()
		return oAlertas

#    return HttpResponse(json.dumps(jsonPedidos), content_type="application/json")

def editarPedido(request,pedido_id):
    oPedido = Pedido.objects.get(id = pedido_id)
    if request.method == 'POST':
        Datos = request.POST
        form = PedidoForm(request.POST, instance=oPedido)
        if form.is_valid():
            form = form.save()
            return redirect('/Pedido/listar/')
        else:
            return render(request, '/Pedido/error.html')
    else:
        form = PedidoForm(request.POST or None, instance=oPedido)
        print(form)
        return render(request, 'Pedido/editar.html', {'form': form})


def eliminarPedido(request, pedido_id):
     oPedido = Pedido.objects.get(id = pedido_id)
     if  request.method == 'POST':
        oPedido.delete()
        return redirect('/Pedido/listar/')
     return render(request, 'Pedido/eliminar.html', {'oPedido': oPedido})
