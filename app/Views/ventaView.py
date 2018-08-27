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
from datetime import datetime,date

##paginacion
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def nuevoVenta(request):
    if request.method == 'GET':
        Datos = request.POST
        return render(request, 'venta/nuevo.html', {})

def ListarVentas(request):
    oProductos=[]
    if request.method == 'POST':
        return render(request, 'venta/listar.html')
    else:
        oVenta = Venta.objects.filter(estado = True).order_by('-id')[:50]
        paginator = Paginator(oVenta,2)

        page = request.GET.get('page')
        try:
            ventaPagina = paginator.page(page)
        except PageNotAnInteger:
            ventaPagina = paginator.page(1)
        except EmptyPage:
            ventaPagina = paginator.page(paginator.num_pages)

        for o in oVenta:
            pedido = Pedido.objects.filter(id=o.pedido_id,estado=True)
            pedidoproductospresentacions = Pedidoproductospresentacions.objects.filter(pedido_id__in=[p.id for p in pedido])
            for ope in pedidoproductospresentacions:
                oNuevo={}
                oNuevo['id']=o.id
                oNuevo['producto']=ope.productopresentacions.producto.nombre
                oProductos.append(oNuevo)

        return render(request, 'venta/listar.html', {"oVenta": ventaPagina,"oProductos":oProductos})

def FiltrarVentas(request, *args, **kwargs):
    producto_b = request.POST['inpt-producto']
    dni = request.POST['buscando']
    fecha_inicio = request.POST['desde']
    fecha_fin = request.POST['hasta']
    oProductos=[]
    oVentas=[]
    if producto_b != '':
        presentacion = Productopresentacions.objects.filter(producto=producto_b)
        pedidoproductopresentacion = Pedidoproductospresentacions.objects.filter(productopresentacions_id__in=[p.id for p in presentacion])
        pedido = Pedido.objects.filter(estado=True,id__in=[s.pedido_id for s in pedidoproductopresentacion])
        venta = Venta.objects.filter(pedido_id__in=[p.id for p in pedido])
        productonombre = Producto.objects.get(id=producto_b).nombre
        for v in venta:
            oNuevo={}
            oNuevo['id']=v.id
            oNuevo['producto']=productonombre
            oProductos.append(oNuevo)
        oVentas = venta.order_by('-id')
    if dni != '':
        venta = Venta.objects.filter(estado=True,cliente_id=3).order_by('-id')
        for oVenta in venta:
            pedido = Pedido.objects.filter(estado=True,id=oVenta.pedido_id)
            pedidoproductospresentacions = Pedidoproductospresentacions.objects.filter(pedido_id__in=[p.id for p in pedido])
            for oPedidopedidoproductopresentacion in pedidoproductospresentacions:
                oNuevo={}
                oNuevo['id']=oVenta.id
                oNuevo['producto']=oPedidopedidoproductopresentacion.productopresentacions.producto.nombre
                oProductos.append(oNuevo)
        oVentas = venta
    if fecha_inicio!='' and fecha_fin!='':
        fecha1=datetime.strftime(datetime.strptime(fecha_inicio,'%d/%m/%Y'),'%Y-%m-%d')
        fecha2=datetime.strftime(datetime.strptime(fecha_fin,'%d/%m/%Y'),'%Y-%m-%d')
        #fecha2=date.today()
        oVentas = Venta.objects.filter(estado=True,fecha__range=[fecha1,fecha2]).order_by('-id')[:50]
        for oVenta in oVentas:
            pedido = Pedido.objects.filter(estado=True,id=oVenta.pedido_id)
            pedidoproductospresentacions = Pedidoproductospresentacions.objects.filter(pedido_id__in=[p.id for p in pedido])
            for oPedidopedidoproductopresentacion in pedidoproductospresentacions:
                oNuevo={}
                oNuevo['id']=oVenta.id
                oNuevo['producto']=oPedidopedidoproductopresentacion.productopresentacions.producto.nombre
                oProductos.append(oNuevo)
    elif fecha_inicio!='' and fecha_fin=='':
        fecha1=datetime.strftime(datetime.strptime(fecha_inicio,'%d/%m/%Y'),'%Y-%m-%d')
        fecha2=date.today()
        oVentas = Venta.objects.filter(estado=True,fecha__range=[fecha1,fecha2]).order_by('-id')[:50]
        for oVenta in oVentas:
            pedido = Pedido.objects.filter(estado=True,id=oVenta.pedido_id)
            pedidoproductospresentacions = Pedidoproductospresentacions.objects.filter(pedido_id__in=[p.id for p in pedido])
            for oPedidopedidoproductopresentacion in pedidoproductospresentacions:
                oNuevo={}
                oNuevo['id']=oVenta.id
                oNuevo['producto']=oPedidopedidoproductopresentacion.productopresentacions.producto.nombre
                oProductos.append(oNuevo)
    elif fecha_inicio=='' and fecha_fin!='':
        fecha2=datetime.strftime(datetime.strptime(fecha_fin,'%d/%m/%Y'),'%Y-%m-%d')
        #fecha2=date.today()
        oVentas = Venta.objects.filter(estado=True,fecha__lte=fecha2).order_by('-id')[:50]
        for oVenta in oVentas:
            pedido = Pedido.objects.filter(estado=True,id=oVenta.pedido_id)
            pedidoproductospresentacions = Pedidoproductospresentacions.objects.filter(pedido_id__in=[p.id for p in pedido])
            for oPedidopedidoproductopresentacion in pedidoproductospresentacions:
                oNuevo={}
                oNuevo['id']=oVenta.id
                oNuevo['producto']=oPedidopedidoproductopresentacion.productopresentacions.producto.nombre
                oProductos.append(oNuevo)
    else:
        oVentas = []
        oProductos = []

    return render(request, 'venta/listar.html', {"oVenta": oVentas,"oProductos":oProductos})


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
            ToProductosalPedidos = 0

            #oPedidos = Pedido.objects.filter(estado = True,fecha = fecha, empleado = idEmpleado)
            oPedidos = Pedido.objects.filter(estado = True, empleado = idEmpleado)
            for oPedido in oPedidos:
                jsonPedido = {}
                jsonPedido["idPedido"] = oPedido.id
                jsonPedido["fecha"] = str(oPedido.fecha)
                jsonPedido["cliente"] = oPedido.cliente.nombre
                jsonPedido["productos"] = []
                oPedidoproductospresentacions = Pedidoproductospresentacions.objects.filter(pedido=oPedido)
                ToProductosalPedido = 0
                for oPedidoproductospresentacion in oPedidoproductospresentacions:
                    jsonPedidoProductoPresentacion = {}
                    jsonPedidoProductoPresentacion["cantidad"] = oPedidoproductospresentacion.cantidad
                    jsonPedidoProductoPresentacion["valor"] = oPedidoproductospresentacion.valor
                    jsonPedidoProductoPresentacion["presentacion"] = oPedidoproductospresentacion.productopresentacions.presentacion.nombre
                    jsonPedidoProductoPresentacion["producto"] = oPedidoproductospresentacion.productopresentacions.producto.nombre
                    ToProductosalPedido = ToProductosalPedido + (jsonPedidoProductoPresentacion["cantidad"]*jsonPedidoProductoPresentacion["valor"])
                    jsonPedido["productos"].append(jsonPedidoProductoPresentacion)


                ToProductosalPedidos = ToProductosalPedidos +ToProductosalPedido
                jsonPedido["ToProductosalPedido"] = ToProductosalPedido

                jsonPedidos["pedidos"].append(jsonPedido)
            jsonPedidos["ToProductosalPedidos"] = ToProductosalPedidos
            return HttpResponse(json.dumps(jsonPedidos), content_type="application/json")

"""
