# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum

from rest_framework.generics import (ListAPIView)
from datetime import datetime,date

from ferreteria import settings
from ferreteria.urls import *
# Create your views here.
from app.fomularios.productoForm import *
from app.models import *
from app.views import *

import json
###########################################################
#   Usuario: Erick Sulca
#   Fecha: 26/08/23
#   Última modificación:
#   Descripción:
#   Lista de operaciones de las aperturas de Caja
###########################################################
def ReporteAperturasCaja(request):
    if request.method == 'POST':
        Datos = request.POST
        fecha_reporte = datetime.strptime(Datos['fechaReporte'], "%m/%d/%Y")
        
        oTipooperacionIngreso = Tipooperacion.objects.get(id=1)
        oDetalletipooperacionIngreso = Detalletipooperacion.objects.filter(tipooperacion=oTipooperacionIngreso)
        
        oTipooperacionEgreso = Tipooperacion.objects.get(id=2)
        oDetalletipooperacionEgreso = Detalletipooperacion.objects.filter(tipooperacion=oTipooperacionEgreso)
        
        oAperturacajas = Aperturacaja.objects.filter(fecha__icontains = fecha_reporte)
        
        print(Datos)
        print(Datos['fechaReporte'])
        oOperacionesIngreso = Operacion.objects.filter(aperturacaja__in=[p.id for p in oAperturacajas], detalletipooperacion__in=[q.id for q in oDetalletipooperacionIngreso] ).aggregate(Sum('monto'))
        print("################# Ingreso ##################")
        print(oOperacionesIngreso)
        print(oOperacionesIngreso['monto__sum'])
        print(type(oOperacionesIngreso))


        oOperacionesEgreso = Operacion.objects.filter(aperturacaja__in=[p.id for p in oAperturacajas], detalletipooperacion__in=[q.id for q in oDetalletipooperacionEgreso] ).aggregate(Sum('monto'))
        print("################# Egreso ##################")
        print(oOperacionesEgreso)

        oDatosSumOperaciones = {}
        oDatosSumOperaciones['Ingreso'] = "{:.2f}".format(oOperacionesIngreso['monto__sum'])
        oDatosSumOperaciones['Egreso'] = "{:.2f}".format(oOperacionesEgreso['monto__sum'])

            
        print(oAperturacajas)

        return render(request, 'reporte/reporteAperturaCajaListar.html', {'oAperturacajas': oAperturacajas,'oDatosSumOperaciones':oDatosSumOperaciones})
    if request.method == 'GET':
        #oCierrecaja = Producto.objects.filter(estado = True)
        return render(request, 'reporte/reporteAperturaCajaForm.html', {})
    
def ReporteVentaProductos(request):
    if request.method == 'GET':
        return render(request,'reporte/reporteProductoForm.html', {})
    
    if request.method == 'POST':
        Datos = request.POST
        print("## LOG: fun_POST_reporteProductos")
        print(Datos)
        oProducto = get_object_or_404(Producto,nombre=Datos['producto_buscado'])
        print(oProducto)

        oProducto_presentacions = Producto_presentacions.objects.filter(estado=True,producto=oProducto)
        
        oPedido_productopresentacions = Pedido_productopresentacions.objects.filter(estado=True,producto_presentacions__in = [p.id for p in oProducto_presentacions])
        
        print(oPedido_productopresentacions)
        arr_Pedidos = []
        total_operacion = 0

        for oPedido_productopresentacion in oPedido_productopresentacions:
            print(oPedido_productopresentacion.pedido.id)
            print(oPedido_productopresentacion.pedido.pedido_ventas.all())
            count_ventas = oPedido_productopresentacion.pedido.pedido_ventas.all().count()
            if count_ventas >= 1:
                total_operacion += (oPedido_productopresentacion.precio_pedido*oPedido_productopresentacion.cantidad)
            arr_Pedidos.append(oPedido_productopresentacion.pedido)
        
        print(total_operacion)

        return render(request,'reporte/reporteProductoListar.html', {'oPedido_productopresentacions':oPedido_productopresentacions, 'oProducto': oProducto, 'total_operacion':total_operacion})

def ReporteIngresoProductos(request):
    if request.method == 'GET':
        return render(request,'reporte/reporteProductoForm.html', {})
    
    if request.method == 'POST':
        Datos = request.POST
        print("## LOG: fun_POST_reporteProductos")
        print(Datos)
        oProducto = get_object_or_404(Producto,nombre=Datos['producto_buscado'])
        print(oProducto)

        oProducto_presentacions = Producto_presentacions.objects.filter(estado=True,producto=oProducto)
        
        oLote_productopresentacions = Lote_productopresentacions.objects.filter(estado=True,producto_presentacions__in = [p.id for p in oProducto_presentacions])
        
        print(oLote_productopresentacions)
        total_operacion = 0

        for oLote_productopresentacion in oLote_productopresentacions:
            total_operacion += (oLote_productopresentacion.precio_lote*oLote_productopresentacion.cantidad)
        
        print(total_operacion)

        return render(request,'reporte/reporteProductoListar.html', {'oPedido_productopresentacions':oLote_productopresentacions, 'oProducto': oProducto, 'total_operacion':total_operacion})


