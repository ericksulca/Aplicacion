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
            pedido = Pedido.objects.filter(id=o.pedido_id)
            pedidoproductospresentacions = Pedidoproductospresentacions.objects.filter(pedido_id__in=[p.id for p in pedido])
            productoPresentacion = Productopresentacions.objects.filter(id__in=[p.productopresentacions_id for p in pedidoproductospresentacions])
            for a in productoPresentacion:
                producto=Producto.objects.get(id=a.producto_id)
                nombre=producto.nombre
                oNuevo={}
                oNuevo['id']=o.id
                oNuevo['producto']=nombre
                oProductos.append(oNuevo)
        return render(request, 'venta/listar.html', {"oVenta": ventaPagina,"oProductos":oProductos})


# class FiltrarVentas(ListView):
#     template_name = 'venta/listar.html'
#
#     def filtrarProducto(producto_b):
#         oProductos=[]
#         if producto_b != '':
#             presentacion = Productopresentacions.objects.filter(producto=producto_b)
#             pedidoproductopresentacion = Pedidoproductospresentacions.objects.filter(productopresentacions_id__in=[p.id for p in presentacion])
#             pedido = Pedido.objects.filter(id__in=[s.pedido_id for s in pedidoproductopresentacion])
#             venta = Venta.objects.filter(pedido_id__in=[p.id for p in pedido])
#             productonombre = Producto.objects.get(id=producto_b).nombre
#             for v in venta:
#                 oNuevo={}
#                 oNuevo['id']=v.id
#                 oNuevo['producto']=productonombre
#                 oProductos.append(oNuevo)
#         return venta, oProductos
#
#     def filtrarDni(dni):
#         oProductos=[]
#         if dni != '':
#             cliente = Venta.objects.filter(cliente_id=3)
#             for c in cliente:
#                 pedido = Pedido.objects.filter(id=c.pedido_id)
#                 pedidopre = Pedidoproductospresentacions.objects.filter(pedido_id__in=[p.id for p in pedido])
#                 presentacion = Productopresentacions.objects.filter(id__in=[p.productopresentacions_id for p in pedidopre])
#                 producto = Producto.objects.filter(id__in=[n.producto_id for n in presentacion])
#                 for p in producto:
#                     oNuevo={}
#                     oNuevo['id']=c.id
#                     oNuevo['producto']=p.nombre
#                     oProductos.append(oNuevo)

def FiltrarVentas(request, *args, **kwargs):
    producto_b = request.POST['inpt-producto']
    dni = request.POST['buscando']
    fecha_inicio = request.POST['desde']
    fecha_fin = request.POST['hasta']

    # oVenta = FiltrarVentas.filtrarProducto(producto_b)
    # oVentas = {oVenta}
    # oProductos = FiltrarVentas.filtrarProducto(producto_b)
    # oProductos = {oProductos}

    oProductos=[]
    if producto_b != '':
        presentacion = Productopresentacions.objects.filter(producto=producto_b)
        pedidoproductopresentacion = Pedidoproductospresentacions.objects.filter(productopresentacions_id__in=[p.id for p in presentacion])
        pedido = Pedido.objects.filter(id__in=[s.pedido_id for s in pedidoproductopresentacion])
        venta = Venta.objects.filter(pedido_id__in=[p.id for p in pedido])
        productonombre = Producto.objects.get(id=producto_b).nombre
        for v in venta:
            oNuevo={}
            oNuevo['id']=v.id
            oNuevo['producto']=productonombre
            oProductos.append(oNuevo)
        oVenta = venta.order_by('-id')
    if dni != '':
        cliente = Venta.objects.filter(cliente_id=3).order_by('-id')
        for c in cliente:
            pedido = Pedido.objects.filter(id=c.pedido_id)
            pedidopre = Pedidoproductospresentacions.objects.filter(pedido_id__in=[p.id for p in pedido])
            presentacion = Productopresentacions.objects.filter(id__in=[p.productopresentacions_id for p in pedidopre])
            producto = Producto.objects.filter(id__in=[n.producto_id for n in presentacion])
            for p in producto:
                oNuevo={}
                oNuevo['id']=c.id
                oNuevo['producto']=p.nombre
                oProductos.append(oNuevo)
        oVenta = cliente
    if fecha_inicio!='':
        fecha1=datetime.strftime(datetime.strptime(fecha_inicio,'%d/%m/%Y'),'%Y-%m-%d')
        fecha2=date.today()
        oVenta = Venta.objects.filter(fecha__range=[fecha1,fecha2]).order_by('-id')
        for o in oVenta:
            pedido = Pedido.objects.filter(id=o.pedido_id)
            pedidoproductospresentacions = Pedidoproductospresentacions.objects.filter(pedido_id__in=[p.id for p in pedido])
            productoPresentacion = Productopresentacions.objects.filter(id__in=[p.productopresentacions_id for p in pedidoproductospresentacions])
            for a in productoPresentacion:
                producto=Producto.objects.get(id=a.producto_id)
                nombre=producto.nombre
                oNuevo={}
                oNuevo['id']=o.id
                oNuevo['producto']=nombre
                oProductos.append(oNuevo)
    if fecha_fin!='':
        fecha2=datetime.strftime(datetime.strptime(fecha_fin,'%d/%m/%Y'),'%Y-%m-%d')
        #fecha2=date.today()
        oVenta = Venta.objects.filter(fecha__lte=fecha2).order_by('-id')
        for o in oVenta:
            pedido = Pedido.objects.filter(id=o.pedido_id)
            pedidoproductospresentacions = Pedidoproductospresentacions.objects.filter(pedido_id__in=[p.id for p in pedido])
            productoPresentacion = Productopresentacions.objects.filter(id__in=[p.productopresentacions_id for p in pedidoproductospresentacions])
            for a in productoPresentacion:
                producto=Producto.objects.get(id=a.producto_id)
                nombre=producto.nombre
                oNuevo={}
                oNuevo['id']=o.id
                oNuevo['producto']=nombre
                oProductos.append(oNuevo)
    return render(request, 'venta/listar.html', {"oVenta": oVenta,"oProductos":oProductos})




        # if dni != '':
        #
        #
        # for o in oVentapr:
        #     oVentas = Venta.objects.get(id=o.id)
        #     pedid = oVentas.pedido
        #     amb = pedid.pedidoproductospresentacions_set.all()
        #     for a in amb:
        #         h=a.productopresentacions_id
        #         n=Productopresentacions.objects.get(id=h)
        #         m=n.producto.nombre
        #         oNuevo={}
        #         oNuevo['id']=o.id
        #         oNuevo['producto']=m
        #         oVentaProducto.append(oNuevo)
        #
        # for bus in os:
        #     if bus['producto'] == producto_b:
        #         oNuevo={}
        #         oNuevo['id']=bus['id']
        #         oNuevo['producto']=bus['producto']
        #         oProductos.append(oNuevo)
        #
        # fecha1=''
        # fecha2=''
        #
        # if fecha_inicio!='' and fecha_fin!='':
        #     try:
        #         fecha1=datetime.strftime(datetime.strptime(fecha_inicio,'%d/%m/%Y'),'%Y-%m-%d')
        #         fecha2=datetime.strftime(datetime.strptime(fecha_fin,'%d/%m/%Y'),'%Y-%m-%d')
        #     except:
        #         fecha1=''
        #         fecha2=''
        # elif fecha_inicio=='' and fecha_fin!='':
        #     try:
        #         fecha2=datetime.strftime(datetime.strptime(fecha_fin,'%d/%m/%Y'),'%Y-%m-%d')
        #     except:
        #         fecha1=''
        #         fecha2=''
        # elif fecha_inicio!='' and fecha_fin=='':
        #     try:
        #         fecha1=datetime.strftime(datetime.strptime(fecha_inicio,'%d/%m/%Y'),'%Y-%m-%d')
        #     except:
        #         fecha1=''
        #         fecha2=''
        # fechaIni = Venta.objects.get(id=1)
        # primerFecha = datetime.strftime(fechaIni.fecha,'%Y-%m-%d')
        #
        # oVenta = []
        # if producto_b != '' and dni!='' and fecha1!='' and fecha2!='':
        #     iden=Cliente.objects.get(numerodocumento=dni)
        #     oVenta = iden.venta_set.filter(fecha__range=[fecha1,fecha2])
        #     return render(request,'venta/listar.html',{'oVenta':oVenta,'oProductos':oProductos}, )
        # elif producto_b == '' and dni!='' and fecha1!='' and fecha2!='':
        #     try:
        #         iden=Cliente.objects.get(numerodocumento=dni)
        #         oVenta = iden.venta_set.filter(fecha__range=[fecha1,fecha2])
        #         return render(request,'venta/listar.html',{'oVenta':oVenta,'oProductos':oVentaProducto}, )
        #     except Cliente.DoesNoProductosExist:
        #          return render(request,'venta/listar.html',{'oVenta':oVenta}, )
        # elif producto_b != '' and dni=='' and fecha1!='' and fecha2!='':
        #     try:
        #         dem = Venta.objects.filter(fecha__range=[fecha1,fecha2])
        #         for d in dem:
        #             for i in oProductos:
        #                 if(d.id == i['id']):
        #                     idb = i['id']
        #                     busca = Venta.objects.get(id=idb,estado = True)
        #                     oVenta.append(busca)
        #
        #         #oVenta = Venta.objects.filter(estado = True).order_by('-id')
        #         return render(request,'venta/listar.html',{'oVenta':oVenta,'oProductos':oProductos}, )
        #     except Producto.DoesNoProductosExist:
        #          return render(request,'venta/listar.html',{'oVenta':oVenta}, )
        # elif producto_b == '' and dni=='' and fecha1!='' and fecha2!='':
        #     oVenta = Venta.objects.filter(fecha__range=[fecha1,fecha2]).order_by('-id')
        #     return render(request,'venta/listar.html',{'oVenta':oVenta,'oProductos':os},  )
        # ##########################################################################
        # elif producto_b != '' and dni!='' and fecha1!='' and fecha2=='':
        #     iden=Cliente.objects.get(numerodocumento=dni)
        #     fecha2=date.today()
        #     oVenta = iden.venta_set.filter(fecha__range=[fecha1,fecha2])
        #     return render(request,'venta/listar.html',{'oVenta':oVenta,'oProductos':oProductos}, )
        # elif producto_b == '' and dni!='' and fecha1!='' and fecha2=='':
        #     try:
        #         fecha2=date.today()
        #         iden=Cliente.objects.get(numerodocumento=dni)
        #         oVenta = iden.venta_set.filter(fecha__range=[fecha1,fecha2])
        #         return render(request,'venta/listar.html',{'oVenta':oVenta,'oProductos':os}, )
        #     except Cliente.DoesNoProductosExist:
        #          return render(request,'venta/listar.html',{'oVenta':oVenta}, )
        # elif producto_b != '' and dni=='' and fecha1!='' and fecha2=='':
        #     try:
        #         fecha2= date.today()
        #         dem = Venta.objects.filter(fecha__range=[fecha1,fecha2])
        #         for d in dem:
        #             for i in oProductos:
        #                 if(d.id == i['id']):
        #                     idb = i['id']
        #                     busca = Venta.objects.get(id=idb,estado = True)
        #                     oVenta.append(busca)
        #
        #         #oVenta = Venta.objects.filter(estado = True).order_by('-id')
        #         return render(request,'venta/listar.html',{'oVenta':oVenta,'oProductos':oProductos}, )
        #     except Producto.DoesNoProductosExist:
        #          return render(request,'venta/listar.html',{'oVenta':oVenta}, )
        # elif producto_b == '' and dni=='' and fecha1!='' and fecha2=='':
        #     fecha2=date.today()
        #     oVenta = Venta.objects.filter(fecha__range=[fecha1,fecha2]).order_by('-id')
        #     return render(request,'venta/listar.html',{'oVenta':oVenta,'oProductos':os},  )
        # ##########################################################################
        # elif producto_b != '' and dni!='' and fecha1=='' and fecha2!='':
        #     iden=Cliente.objects.get(numerodocumento=dni)
        #     fecha1=primerFecha
        #     oVenta = iden.venta_set.filter(fecha__range=[fecha1,fecha2])
        #     return render(request,'venta/listar.html',{'oVenta':oVenta,'oProductos':oProductos}, )
        # elif producto_b == '' and dni!='' and fecha1=='' and fecha2!='':
        #     try:
        #         fecha1=primerFecha
        #         iden=Cliente.objects.get(numerodocumento=dni)
        #         oVenta = iden.venta_set.filter(fecha__range=[fecha1,fecha2])
        #         return render(request,'venta/listar.html',{'oVenta':oVenta,'oProductos':os}, )
        #     except Cliente.DoesNoProductosExist:
        #          return render(request,'venta/listar.html',{'oVenta':oVenta}, )
        # elif producto_b != '' and dni=='' and fecha1=='' and fecha2!='':
        #     try:
        #         fecha1=primerFecha
        #         dem = Venta.objects.filter(fecha__range=[fecha1,fecha2])
        #         for d in dem:
        #             for i in oProductos:
        #                 if(d.id == i['id']):
        #                     idb = i['id']
        #                     busca = Venta.objects.get(id=idb,estado = True)
        #                     oVenta.append(busca)
        #
        #         #oVenta = Venta.objects.filter(estado = True).order_by('-id')
        #         return render(request,'venta/listar.html',{'oVenta':oVenta,'oProductos':oProductos}, )
        #     except Producto.DoesNoProductosExist:
        #          return render(request,'venta/listar.html',{'oVenta':oVenta}, )
        # elif producto_b == '' and dni=='' and fecha1=='' and fecha2!='':
        #     fecha1=primerFecha
        #     oVenta = Venta.objects.filter(fecha__range=[fecha1,fecha2]).order_by('-id')
        #     return render(request,'venta/listar.html',{'oVenta':oVenta,'oProductos':os},  )
        # ##########################################################################
        # elif producto_b != '' and dni!='' and fecha1=='' and fecha2=='':
        #     iden=Cliente.objects.get(numerodocumento=dni)
        #     fecha1=date.today()
        #     fecha2=date.today()
        #     oVenta = iden.venta_set.filter(fecha__range=[fecha1,fecha2])
        #     return render(request,'venta/listar.html',{'oVenta':oVenta,'oProductos':oProductos}, )
        # elif producto_b == '' and dni!='' and fecha1=='' and fecha2=='':
        #     try:
        #         fecha1=date.today()
        #         fecha2=date.today()
        #         iden=Cliente.objects.get(numerodocumento=dni)
        #         oVenta = iden.venta_set.filter(fecha__range=[fecha1,fecha2])
        #         return render(request,'venta/listar.html',{'oVenta':oVenta,'oProductos':os}, )
        #     except Cliente.DoesNoProductosExist:
        #          return render(request,'venta/listar.html',{'oVenta':oVenta}, )
        # elif producto_b != '' and dni=='' and fecha1=='' and fecha2=='':
        #     try:
        #         fecha1=date.today()
        #         fecha2=date.today()
        #         dem = Venta.objects.filter(fecha__range=[fecha1,fecha2])
        #         for d in dem:
        #             for i in oProductos:
        #                 if(d.id == i['id']):
        #                     idb = i['id']
        #                     busca = Venta.objects.get(id=idb,estado = True)
        #                     oVenta.append(busca)
        #
        #         #oVenta = Venta.objects.filter(estado = True).order_by('-id')
        #         return render(request,'venta/listar.html',{'oVenta':oVenta,'oProductos':oProductos}, )
        #     except Producto.DoesNoProductosExist:
        #          return render(request,'venta/listar.html',{'oVenta':oVenta}, )
        # elif producto_b == '' and dni=='' and fecha1=='' and fecha2=='':
        #     fecha1=date.today()
        #     fecha2=date.today()
        #     oVenta = Venta.objects.filter(fecha__range=[fecha1,fecha2]).order_by('-id')
        #     return render(request,'venta/listar.html',{'oVenta':oVenta,'oProductos':os},  )
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
