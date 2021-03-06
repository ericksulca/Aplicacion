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
from app.views import *
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
import json
from datetime import datetime

def nuevoVenta(request):
    if request.method == 'GET':
        Datos = request.POST
        return render(request, 'venta/nuevo.html', {})

def ListarVentas(request):

    ot=[]
    if request.method == 'POST':
        return render(request, 'venta/listar.html')
    else:
        oVenta = Venta.objects.filter(estado = True).order_by('-id')

        for o in oVenta:
            oVentas = Venta.objects.get(id=o.id)
            pedid = oVentas.pedido
            amb = pedid.pedidoproductospresentacions_set.all()
            for a in amb:
                h=a.productopresentacions_id
                n=Productopresentacions.objects.get(id=h)
                m=n.producto.nombre
                oNuevo={}
                oNuevo['id']=o.id
                oNuevo['producto']=m
                ot.append(oNuevo)
        return render(request, 'venta/listar.html', {"oVenta": oVenta,"ot":ot})


class FiltrarVentas(ListView):
    template_name = 'venta/listar.html'

    def post(self, request, *args, **kwargs):
        #producto = request.POST['producto']
        producto_b = request.POST['producto_b']
        dni = request.POST['buscando']
        fecha_inicio = request.POST['desde']
        fecha_fin = request.POST['hasta']
        os=[]
        ot=[]
        oVentapr = Venta.objects.filter(estado = True).order_by('-id')

        for o in oVentapr:
            oVentas = Venta.objects.get(id=o.id)
            pedid = oVentas.pedido
            amb = pedid.pedidoproductospresentacions_set.all()
            for a in amb:
                h=a.productopresentacions_id
                n=Productopresentacions.objects.get(id=h)
                m=n.producto.nombre
                oNuevo={}
                oNuevo['id']=o.id
                oNuevo['producto']=m
                os.append(oNuevo)

        for bus in os:
            if bus['producto'] == producto_b:
                ot.append(bus)

        fecha1=datetime.strftime(datetime.strptime(fecha_inicio,'%d-%m-%Y'),'%Y-%m-%d')
        fecha2=datetime.strftime(datetime.strptime(fecha_fin,'%d-%m-%Y'),'%Y-%m-%d')
        oVenta = []
        if dni != '':
            try:
                iden=Cliente.objects.get(numerodocumento=dni)
                oVenta = iden.venta_set.filter(fecha__range=[fecha1,fecha2])
                return render(request,'venta/listar.html',{'oVenta':oVenta,'ot':ot}, )
            except Cliente.DoesNotExist:
                 return render(request,'venta/listar.html',{'oVenta':oVenta}, )
        else:
            oVenta = Venta.objects.filter(fecha__range=[fecha1,fecha2])
            return render(request,'venta/listar.html',{'oVenta':oVenta}, )

"""
@csrf_exempt
def ListarVenta(request):
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

"""
