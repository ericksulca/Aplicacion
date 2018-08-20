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
        producto_b = request.POST['inpt-producto']
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
                oNuevo={}
                oNuevo['id']=bus['id']
                oNuevo['producto']=bus['producto']
                ot.append(oNuevo)

        fecha1=''
        fecha2=''

        if fecha_inicio!='' and fecha_fin!='':
            try:
                fecha1=datetime.strftime(datetime.strptime(fecha_inicio,'%d/%m/%Y'),'%Y-%m-%d')
                fecha2=datetime.strftime(datetime.strptime(fecha_fin,'%d/%m/%Y'),'%Y-%m-%d')
            except:
                fecha1=''
                fecha2=''
        elif fecha_inicio=='' and fecha_fin!='':
            try:
                fecha2=datetime.strftime(datetime.strptime(fecha_fin,'%d/%m/%Y'),'%Y-%m-%d')
            except:
                fecha1=''
                fecha2=''
        elif fecha_inicio!='' and fecha_fin=='':
            try:
                fecha1=datetime.strftime(datetime.strptime(fecha_inicio,'%d/%m/%Y'),'%Y-%m-%d')
            except:
                fecha1=''
                fecha2=''
        fechaIni = Venta.objects.get(id=1)
        primerFecha = datetime.strftime(fechaIni.fecha,'%Y-%m-%d')

        oVenta = []
        if producto_b != '' and dni!='' and fecha1!='' and fecha2!='':
            iden=Cliente.objects.get(numerodocumento=dni)
            oVenta = iden.venta_set.filter(fecha__range=[fecha1,fecha2])
            return render(request,'venta/listar.html',{'oVenta':oVenta,'ot':ot}, )
        elif producto_b == '' and dni!='' and fecha1!='' and fecha2!='':
            try:
                iden=Cliente.objects.get(numerodocumento=dni)
                oVenta = iden.venta_set.filter(fecha__range=[fecha1,fecha2])
                return render(request,'venta/listar.html',{'oVenta':oVenta,'ot':os}, )
            except Cliente.DoesNotExist:
                 return render(request,'venta/listar.html',{'oVenta':oVenta}, )
        elif producto_b != '' and dni=='' and fecha1!='' and fecha2!='':
            try:
                dem = Venta.objects.filter(fecha__range=[fecha1,fecha2])
                for d in dem:
                    for i in ot:
                        if(d.id == i['id']):
                            idb = i['id']
                            busca = Venta.objects.get(id=idb,estado = True)
                            oVenta.append(busca)

                #oVenta = Venta.objects.filter(estado = True).order_by('-id')
                return render(request,'venta/listar.html',{'oVenta':oVenta,'ot':ot}, )
            except Producto.DoesNotExist:
                 return render(request,'venta/listar.html',{'oVenta':oVenta}, )
        elif producto_b == '' and dni=='' and fecha1!='' and fecha2!='':
            oVenta = Venta.objects.filter(fecha__range=[fecha1,fecha2]).order_by('-id')
            return render(request,'venta/listar.html',{'oVenta':oVenta,'ot':os},  )
        ##########################################################################
        elif producto_b != '' and dni!='' and fecha1!='' and fecha2=='':
            iden=Cliente.objects.get(numerodocumento=dni)
            fecha2=date.today()
            oVenta = iden.venta_set.filter(fecha__range=[fecha1,fecha2])
            return render(request,'venta/listar.html',{'oVenta':oVenta,'ot':ot}, )
        elif producto_b == '' and dni!='' and fecha1!='' and fecha2=='':
            try:
                fecha2=date.today()
                iden=Cliente.objects.get(numerodocumento=dni)
                oVenta = iden.venta_set.filter(fecha__range=[fecha1,fecha2])
                return render(request,'venta/listar.html',{'oVenta':oVenta,'ot':os}, )
            except Cliente.DoesNotExist:
                 return render(request,'venta/listar.html',{'oVenta':oVenta}, )
        elif producto_b != '' and dni=='' and fecha1!='' and fecha2=='':
            try:
                fecha2= date.today()
                dem = Venta.objects.filter(fecha__range=[fecha1,fecha2])
                for d in dem:
                    for i in ot:
                        if(d.id == i['id']):
                            idb = i['id']
                            busca = Venta.objects.get(id=idb,estado = True)
                            oVenta.append(busca)

                #oVenta = Venta.objects.filter(estado = True).order_by('-id')
                return render(request,'venta/listar.html',{'oVenta':oVenta,'ot':ot}, )
            except Producto.DoesNotExist:
                 return render(request,'venta/listar.html',{'oVenta':oVenta}, )
        elif producto_b == '' and dni=='' and fecha1!='' and fecha2=='':
            fecha2=date.today()
            oVenta = Venta.objects.filter(fecha__range=[fecha1,fecha2]).order_by('-id')
            return render(request,'venta/listar.html',{'oVenta':oVenta,'ot':os},  )
        ##########################################################################
        elif producto_b != '' and dni!='' and fecha1=='' and fecha2!='':
            iden=Cliente.objects.get(numerodocumento=dni)
            fecha1=primerFecha
            oVenta = iden.venta_set.filter(fecha__range=[fecha1,fecha2])
            return render(request,'venta/listar.html',{'oVenta':oVenta,'ot':ot}, )
        elif producto_b == '' and dni!='' and fecha1=='' and fecha2!='':
            try:
                fecha1=primerFecha
                iden=Cliente.objects.get(numerodocumento=dni)
                oVenta = iden.venta_set.filter(fecha__range=[fecha1,fecha2])
                return render(request,'venta/listar.html',{'oVenta':oVenta,'ot':os}, )
            except Cliente.DoesNotExist:
                 return render(request,'venta/listar.html',{'oVenta':oVenta}, )
        elif producto_b != '' and dni=='' and fecha1=='' and fecha2!='':
            try:
                fecha1=primerFecha
                dem = Venta.objects.filter(fecha__range=[fecha1,fecha2])
                for d in dem:
                    for i in ot:
                        if(d.id == i['id']):
                            idb = i['id']
                            busca = Venta.objects.get(id=idb,estado = True)
                            oVenta.append(busca)

                #oVenta = Venta.objects.filter(estado = True).order_by('-id')
                return render(request,'venta/listar.html',{'oVenta':oVenta,'ot':ot}, )
            except Producto.DoesNotExist:
                 return render(request,'venta/listar.html',{'oVenta':oVenta}, )
        elif producto_b == '' and dni=='' and fecha1=='' and fecha2!='':
            fecha1=primerFecha
            oVenta = Venta.objects.filter(fecha__range=[fecha1,fecha2]).order_by('-id')
            return render(request,'venta/listar.html',{'oVenta':oVenta,'ot':os},  )
        ##########################################################################
        elif producto_b != '' and dni!='' and fecha1=='' and fecha2=='':
            iden=Cliente.objects.get(numerodocumento=dni)
            fecha1=date.today()
            fecha2=date.today()
            oVenta = iden.venta_set.filter(fecha__range=[fecha1,fecha2])
            return render(request,'venta/listar.html',{'oVenta':oVenta,'ot':ot}, )
        elif producto_b == '' and dni!='' and fecha1=='' and fecha2=='':
            try:
                fecha1=date.today()
                fecha2=date.today()
                iden=Cliente.objects.get(numerodocumento=dni)
                oVenta = iden.venta_set.filter(fecha__range=[fecha1,fecha2])
                return render(request,'venta/listar.html',{'oVenta':oVenta,'ot':os}, )
            except Cliente.DoesNotExist:
                 return render(request,'venta/listar.html',{'oVenta':oVenta}, )
        elif producto_b != '' and dni=='' and fecha1=='' and fecha2=='':
            try:
                fecha1=date.today()
                fecha2=date.today()
                dem = Venta.objects.filter(fecha__range=[fecha1,fecha2])
                for d in dem:
                    for i in ot:
                        if(d.id == i['id']):
                            idb = i['id']
                            busca = Venta.objects.get(id=idb,estado = True)
                            oVenta.append(busca)

                #oVenta = Venta.objects.filter(estado = True).order_by('-id')
                return render(request,'venta/listar.html',{'oVenta':oVenta,'ot':ot}, )
            except Producto.DoesNotExist:
                 return render(request,'venta/listar.html',{'oVenta':oVenta}, )
        elif producto_b == '' and dni=='' and fecha1=='' and fecha2=='':
            fecha1=date.today()
            fecha2=date.today()
            oVenta = Venta.objects.filter(fecha__range=[fecha1,fecha2]).order_by('-id')
            return render(request,'venta/listar.html',{'oVenta':oVenta,'ot':os},  )
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
