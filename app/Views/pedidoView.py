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
from app.fomularios.cierrecajaForm import *

def registrarPedido(request):
    if request.method == 'POST':
        return render(request, 'caja/cierre.html')
    else:
        return render(request, 'venta/nuevo.html', {})
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
        for oPedido in oPedidos:
            oPedidoproductospresentacions = Pedidoproductospresentacions.objects.filter(pedido = oPedido)
            for oPedidoproductospresentacion in oPedidoproductospresentacions:
                oProducto = {}
                oProducto["nombreProducto"] = oPedidoproductospresentacion.productopresentacions.producto.nombre
                oProducto["nombrePresentacion"] = oPedidoproductospresentacion.productopresentacions.presentacion.nombre
                oProducto["cantidad"] = oPedidoproductospresentacion.cantidad
                oProductos.append(oProducto)
        
        return render(request, 'pedido/resumen.html', {"oProductos": oProductos})

@csrf_exempt
def DetallePedidoMovil(request):
    if request.method == 'POST':
        Datos = json.loads(request.body)
        idPedido = Datos["idPedido"]
        oPedido = Pedido.objects.get(id = idPedido)
        jsonPedidos = {}
        jsonPedidos["productos"] = []
        oPedidoproductospresentacions = Pedidoproductospresentacions.objects.filter(pedido = oPedido)
        for oPedidoproductospresentacion in oPedidoproductospresentacions:
            oProducto = {}
            oProducto["nombreProducto"] = oPedidoproductospresentacion.productopresentacions.producto.nombre
            oProducto["nombrePresentacion"] = oPedidoproductospresentacion.productopresentacions.presentacion.nombre
            oProducto["cantidad"] = oPedidoproductospresentacion.cantidad
            jsonPedidos["productos"].append(oProducto)
        return HttpResponse(json.dumps(jsonPedidos), content_type="application/json")

def DetallePedido(request,pedido_id):
    if request.method == 'GET':
        idPedido = int(pedido_id)
        oPedido = Pedido.objects.get(id = idPedido)
        oPedidoproductospresentacions = Pedidoproductospresentacions.objects.filter(pedido = oPedido)
        oProductos = []
        for oPedidoproductospresentacion in oPedidoproductospresentacions:
            oProducto = {}
            oProducto["nombreProducto"] = oPedidoproductospresentacion.productopresentacions.producto.nombre
            oProducto["nombrePresentacion"] = oPedidoproductospresentacion.productopresentacions.presentacion.nombre
            oProducto["cantidad"] = oPedidoproductospresentacion.cantidad
            oProductos.append(oProducto)
        
        return render(request, 'pedido/detalle.html', {"oCliente": oPedido.cliente, "oProductos": oProductos})
    else:
        oPedidos = Pedido.objects.filter(estado = True)
        return render(request, 'pedido/listar.html',{"oPedidos": oPedidos})

@csrf_exempt
def InstarPedido(request):
    if request.method=='POST':
        Datos = json.loads(request.body)
        idEmpleado = Datos["idEmpleado"]
        oEmpleado = Empleado.objects.get(id= idEmpleado)
        idCliente = Datos["idCliente"]
        oCliente = Cliente.objects.get(id= idCliente)

        oPedido = Pedido()
        oPedido.empleado = oEmpleado
        oPedido.cliente = oCliente
        oPedido.save()
        oPedidoProductos = Datos["oPedidoProductos"]
        for oPedidoProducto in oPedidoProductos:
            oPedidoproductospresentacions = Pedidoproductospresentacions()
            oPedidoproductospresentacions.valor = oPedidoProducto["valor"]
            oPedidoproductospresentacions.cantidad = oPedidoProducto["cantidad"]
            oPedidoproductospresentacions.pedido = oPedido
            oProductopresentacions = Productopresentacions.objects.get(id = oPedidoProducto["idPresentacion"])
            oPedidoproductospresentacions.productopresentacions = oProductopresentacions
            oPedidoproductospresentacions.save()
        return HttpResponse(json.dumps({'exito':1,"idPedido": oPedido.id}), content_type="application/json")


@csrf_exempt
def ListarPedido(request):
    if request.method == 'POST':
        Datos = json.loads(request.body)
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
            oPedidoproductospresentacions = Pedidoproductospresentacions.objects.filter(pedido=oPedido)
            TotalPedido = 0
            for oPedidoproductospresentacion in oPedidoproductospresentacions:
                jsonPedidoProductoPresentacion = {}
                jsonPedidoProductoPresentacion["cantidad"] = oPedidoproductospresentacion.cantidad
                jsonPedidoProductoPresentacion["valor"] = oPedidoproductospresentacion.valor
                jsonPedidoProductoPresentacion["presentacion"] = oPedidoproductospresentacion.productopresentacions.presentacion.nombre
                jsonPedidoProductoPresentacion["producto"] = oPedidoproductospresentacion.productopresentacions.producto.nombre
                TotalPedido = TotalPedido + (jsonPedidoProductoPresentacion["cantidad"]*jsonPedidoProductoPresentacion["valor"])
                jsonPedido["productos"].append(jsonPedidoProductoPresentacion)


            TotalPedidos = TotalPedidos +TotalPedido
            jsonPedido["TotalPedido"] = TotalPedido

            jsonPedidos["pedidos"].append(jsonPedido)
        jsonPedidos["TotalPedidos"] = TotalPedidos
        return HttpResponse(json.dumps(jsonPedidos), content_type="application/json")
