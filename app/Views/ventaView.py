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
from django.shortcuts import get_object_or_404
import json
from datetime import datetime,date

##paginacion
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.core import serializers

def detalleVenta(request,id_venta):
    oVenta = get_object_or_404(Venta,id=id_venta)
    #oVenta = serializers.serialize("json", oVenta)
    oVenta = {}
    oNegocio = Negocio.objects.filter(estado=True)[:1]
    oNegocio = serializers.serialize("json", oNegocio)
    jsonProductos= {'exito':1, 'oVenta': oVenta, 'oNegocio': oNegocio}
    return HttpResponse(json.dumps(jsonProductos), content_type="application/json")

def operacion_almacen(tipo_op,id_producto,cantidad):
    if tipo_op==1:
        oProducto = Producto.objects.get(id=id_producto)
        oProducto_presentacions = Producto_presentacions.objects.filter(producto=oProducto)
        
        oLote_productopresentacions = Lote_productopresentacions.objects.filter( producto_presentacions__in=[p.id for p in oProducto_presentacions]).order_by('id')

        bool_descontado = False
        for oLote_productopresentacion in oLote_productopresentacions:
            if bool_descontado == False and oLote_productopresentacion.cnt_cantidad>0:
                cant_almacen_lote = oLote_productopresentacion.cnt_cantidad * oLote_productopresentacion.producto_presentacions.valor

                residuo_op = cant_almacen_lote - cantidad
                oLoteAlmacen = Lote_productopresentacions.objects.get(id=oLote_productopresentacion.id)
                if residuo_op >= 0:
                    oLoteAlmacen.cnt_cantidad = (residuo_op/oLote_productopresentacion.producto_presentacions.valor)
                    bool_descontado = True
                else:
                    oLoteAlmacen.cnt_cantidad = 0
                    cantidad = residuo_op * -1
                oLoteAlmacen.save()
        oProducto.valor += 1
        oProducto.save()
        return True

def nuevoVenta(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        oPedido = Pedido()
        if data['oCliente']!={}:
            oCliente = Cliente.objects.get(id= data['oCliente']['id'])
            oPedido.cliente = oCliente
        oPedido.save()

        total_precio_pedido = 0

        for item in data['productos']:
            oPedido_productopresentacions = Pedido_productopresentacions()
            oPedido_productopresentacions.precio_pedido = float(item['precio_producto'])
            oPedido_productopresentacions.cantidad = float(item['cantidad_producto'])
            total_precio_pedido += float(item['precio_producto'])*float(item['cantidad_producto'])
            oPresentacion = Presentacion.objects.get(codigo=item['presentacion_producto'])
            oProducto = Producto.objects.get(id= item['id'],nombre = item['nombre_producto'] )
            oProducto_presentacions = Producto_presentacions.objects.get(producto=oProducto,presentacion=oPresentacion)
            oPedido_productopresentacions.producto_presentacions = oProducto_presentacions
            oPedido_productopresentacions.pedido = oPedido
            oPedido_productopresentacions.save()

            #descuento de productos en Almacén
            cant_descontar = oProducto_presentacions.valor * float(item['cantidad_producto'])

            operacion_almacen(1,oProducto_presentacions.producto.id,cant_descontar)

        #oLote.monto = total_precio_lote
        print(total_precio_pedido)
        oVenta= Venta()
        oVenta.monto = total_precio_pedido
        oVenta.pedido = oPedido
        oVenta.save()

        oOperacion = Operacion()
        oOperacion.monto = float(data['pago_cliente']) 
        oOperacion.descripcion = 'Venta de Productos'
        oAperturacaja = Aperturacaja.objects.latest('id')
        if  oAperturacaja.activo==True:
            oOperacion.aperturacaja = oAperturacaja
        else:
            return redirect('apertura_caja')
        
        # NOMBRE DE VENTA 
        oDetalletipooperacion = Detalletipooperacion.objects.get(nombre='Venta en caja')

        oOperacion.detalletipooperacion = oDetalletipooperacion
        oOperacion.venta = oVenta
        oOperacion.save()
        print("############ log POST function nueva_Venta #############")
        #print(Datos)
        #oNegocio = serializers.serialize("json", oNegocio)
        #oVentaJson = serializers.serialize("json", oVenta)
        jsonProductos= {'exito':1, 'idVenta': oVenta.id}
        return HttpResponse(json.dumps(jsonProductos), content_type="application/json")
        #return redirect ('venta_listar')
    if request.method == 'GET':
        oAperturacaja = Aperturacaja.objects.latest('id')
        if  oAperturacaja.activo==True:
            oProductosTop = Producto.objects.filter(estado=True).order_by('-valor')[:9]
            return render(request, 'venta/nuevo.html', {'oProductosTop': oProductosTop})
        else:
            return redirect('apertura_caja')
        

def ImprimirVenta(request, venta_id):
    oVenta = get_object_or_404(Venta, id=venta_id)
    oNegocio = Negocio.objects.filter(estado=True)[:1]
    print(oNegocio)
    print(oNegocio[0])
    return render(request,'venta/ticket_imprimir.html',{'oVenta': oVenta,'oNegocio':oNegocio[0]})

def ListarVentas(request):
    oProductos=[]
    if request.method == 'POST':
        return render(request, 'venta/listar.html')
    else:
        oVenta = Venta.objects.filter(estado = True).order_by('-id')
        paginator = Paginator(oVenta,5)

        page = request.GET.get('page')
        try:
            ventaPagina = paginator.page(page)
        except PageNotAnInteger:
            ventaPagina = paginator.page(1)
        except EmptyPage:
            ventaPagina = paginator.page(paginator.num_pages)

        index = ventaPagina.number - 1
        max_index = len(paginator.page_range)
        start_index = index - 5 if index >= 5 else 0
        end_index = index + 5 if index <= max_index - 5 else max_index
        page_range = paginator.page_range[start_index:end_index]

        for o in oVenta:
            pedido = Pedido.objects.filter(id=o.pedido_id,estado=True)

        return render(request, 'venta/listar.html', {"oVenta": ventaPagina,"oProductos":oProductos,"page_range": page_range})
    
def filterVentas(request):
    oVentas = Venta.objects.filter(estado = True).order_by('-id')
    #oVentas = []
    oVentas_query = False

    nombre_producto = request.GET.get('producto_buscado')
    nombre_cliente= request.GET.get('cliente_buscado')
    fecha_inicio = request.GET.get('desde')
    fecha_fin = request.GET.get('hasta')

    print("### LOG: fun_Ventas")
    print(type(nombre_producto))
    print(nombre_producto)

    print(type(nombre_cliente))
    print(nombre_cliente)

    print(type(fecha_inicio))
    print(fecha_inicio)

    print(type(fecha_fin))
    print(fecha_fin)

    fecha_hoy = date.today()
    if nombre_producto != '' and nombre_producto !=None:
        oProducto = Producto.objects.filter(nombre= nombre_producto)
        
        oProducto_presentacions = Producto_presentacions.objects.filter(estado=True,producto__in=[p.id for p in oProducto])
        
        oPedido_productopresentacions = Pedido_productopresentacions.objects.filter(estado=True,producto_presentacions__in = [p.id for p in oProducto_presentacions])
        
        print("##LOG: oPedido_productopresentacions")
        print(oPedido_productopresentacions)
        oPedidos = []
        for oPedido_productopresentacion in oPedido_productopresentacions:
            oPedidos.append(oPedido_productopresentacion.pedido)
        
        print("##LOG: oPedidos")
        print(oPedidos)

        oVentas = Venta.objects.filter(estado=True,pedido__in=[p.id for p in oPedidos]).order_by('-id')
        oVentas_query = True

    if nombre_cliente !='' and nombre_cliente !=None:

        oCliente = get_object_or_404(Cliente,nombre=nombre_cliente)
        oPedidos = Pedido.objects.filter(cliente=oCliente)
        if oVentas_query == True:
            arr_ventas = []
            for oVenta in oVentas:
                if oVenta.pedido.cliente == oCliente:
                    print("## LOG: add item")
                    arr_ventas.append(oVenta)
                else:
                    print("## LOG: no add item")
            #oVentas = oVentas.filter(id=24)
            oVentas = arr_ventas

            #oVentas = oVentas.filter(pedido__in=[p.id for p in oPedidos]).order_by('-id')
            print("## LOG: fun filter ventas Existentes")
            print(oVentas)
        else:
            oVentas = Venta.objects.filter(pedido__in=[p.id for p in oPedidos]).order_by('-id')
            oVentas_query = True
            print("## LOG: fun filter ventas")

    if fecha_inicio !='' and fecha_inicio != None:
        print('##############')
        fecha_inicio = datetime.strptime(fecha_inicio, "%m/%d/%Y").date()
        
        if oVentas_query == True:
            print(oVentas)
            print("## LOG: fun filter fechas Existentes | fecha inicio")
            startdate = date.today()
            oVentas = oVentas.filter(estado=True,fecha__lte=fecha_inicio).order_by('-id')[:50]
        else:
            print("## LOG: fun filter fechas | fecha inicio")
            oVentas = Venta.objects.filter(estado=True,fecha__gte=fecha_inicio).order_by('-id')[:50]
            oVentas_query = True
            print(oVentas)
    
    if fecha_fin !='' and fecha_fin != None:
        print('##############')
        fecha_fin = datetime.strptime(fecha_fin, "%m/%d/%Y")
        
        if oVentas_query == True:
            print("## LOG: fun filter fechas Existentes | fecha inicio")
            print(oVentas)
            arr_ventas = []
            for oVenta in oVentas:
                if oVenta.fecha <= fecha_fin:
                    print("## LOG: add item")
                    arr_ventas.append(oVenta)
                else:
                    print("## LOG: no add item")
            #oVentas = oVentas.filter(id=24)
            oVentas = arr_ventas
        else:
            print("## LOG: fun filter fechas | fecha inicio")
            oVentas = Venta.objects.filter(estado=True,fecha__lte=fecha_fin).order_by('-id')[:50]
            oVentas_query = True

    print(oVentas)
    paginator = Paginator(oVentas,5)

    page = request.GET.get('page')
    try:
        ventaPagina = paginator.page(page)
    except PageNotAnInteger:
        ventaPagina = paginator.page(1)
    except EmptyPage:
        ventaPagina = paginator.page(paginator.num_pages)

    index = ventaPagina.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 5 if index >= 5 else 0
    end_index = index + 5 if index <= max_index - 5 else max_index
    page_range = paginator.page_range[start_index:end_index]

    return render(request, 'venta/listar.html', {"oVenta": ventaPagina,"oProductos":{},"page_range": page_range})

def Ventas(request):
    #producto = get_object_or_404(Producto, producto_buscado=producto_buscado)
    oProductos=[]
    oVentas=[]

    producto = request.GET.get('producto_buscado')
    dni= request.GET.get('cliente_buscado')
    fecha_inicio = request.GET.get('desde')
    fecha_fin = request.GET.get('hasta')

    print("### LOG: fun_Ventas")
    print(type(producto))
    print(producto)

    print(type(dni))
    print(dni)

    print(type(fecha_inicio))
    print(fecha_inicio)

    print(type(fecha_fin))
    print(fecha_fin)
    #oVentas

    if producto != '':
        #pedido = Pedido.objects.filter(estado=True,id__in=[s.pedido_id for s in ])
        pedido = Pedido.objects.filter(estado=True)
        venta = Venta.objects.filter(estado=True,pedido_id__in=[p.id for p in pedido]).order_by("-id")
        productonombre = Producto.objects.get(id=producto).nombre
        for v in venta:
            oNuevo={}
            oNuevo['id']=v.id
            oNuevo['producto']=productonombre
            oProductos.append(oNuevo)
        oVentas = venta
    if dni != '':
        if producto != '':
            cliente = Cliente.objects.get(numerodocumento=dni)
            venta = Venta.objects.filter(estado=True,id__in=[p.id for p in oVentas],cliente_id=cliente.id).order_by('-id')

        else:
            oProductos=[]
            print(dni)
            cliente = Cliente.objects.get(numerodocumento=dni)
            venta = Venta.objects.filter(estado=True,cliente_id=cliente.id).order_by('-id')
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
        fecha1=datetime.strftime(datetime.strptime(fecha_inicio,'%d-%m-%Y'),'%Y-%m-%d')
        fecha2=datetime.strftime(datetime.strptime(fecha_fin,'%d-%m-%Y'),'%Y-%m-%d')
        if producto !='' and dni!='':
            venta = Venta.objects.filter(estado=True,id__in=[p.id for p in oVentas],fecha__range=[fecha1,fecha2]).order_by('-id')
        elif producto !='':
            venta = Venta.objects.filter(estado=True,id__in=[p.id for p in oVentas],fecha__range=[fecha1,fecha2]).order_by('-id')
        elif dni !='':
            venta = Venta.objects.filter(estado=True,id__in=[p.id for p in oVentas],fecha__range=[fecha1,fecha2]).order_by('-id')
        else:
        #fecha2=date.today()
            oProductos = []
            venta = Venta.objects.filter(estado=True,fecha__range=[fecha1,fecha2]).order_by('-id')
            for oVenta in venta:
                pedido = Pedido.objects.filter(estado=True,id=oVenta.pedido_id)
                pedidoproductospresentacions = Pedidoproductospresentacions.objects.filter(pedido_id__in=[p.id for p in pedido])
                for oPedidopedidoproductopresentacion in pedidoproductospresentacions:
                    oNuevo={}
                    oNuevo['id']=oVenta.id
                    oNuevo['producto']=oPedidopedidoproductopresentacion.productopresentacions.producto.nombre
                    oProductos.append(oNuevo)
        oVentas = venta
    elif fecha_inicio!='':
        fecha1=datetime.strftime(datetime.strptime(fecha_inicio,'%d-%m-%Y'),'%Y-%m-%d')
        fecha2=date.today()
        if producto !='' and dni!='':
            venta = Venta.objects.filter(estado=True,id__in=[p.id for p in oVentas],fecha__range=[fecha1,fecha2]).order_by('-id')
        elif producto !='':
            venta = Venta.objects.filter(estado=True,id__in=[p.id for p in oVentas],fecha__range=[fecha1,fecha2]).order_by('-id')
        elif dni !='':
            venta = Venta.objects.filter(estado=True,id__in=[p.id for p in oVentas],fecha__range=[fecha1,fecha2]).order_by('-id')
        else:
            oProductos=[]
            venta = Venta.objects.filter(estado=True,fecha__range=[fecha1,fecha2]).order_by('-id')[:50]
            for oVenta in venta:
                pedido = Pedido.objects.filter(estado=True,id=oVenta.pedido_id)
                pedidoproductospresentacions = Pedidoproductospresentacions.objects.filter(pedido_id__in=[p.id for p in pedido])
                for oPedidopedidoproductopresentacion in pedidoproductospresentacions:
                    oNuevo={}
                    oNuevo['id']=oVenta.id
                    oNuevo['producto']=oPedidopedidoproductopresentacion.productopresentacions.producto.nombre
                    oProductos.append(oNuevo)
        oVentas = venta
    elif fecha_fin!='':
        fecha2=datetime.strftime(datetime.strptime(fecha_fin,'%d-%m-%Y'),'%Y-%m-%d')
        if producto !='' and dni!='':
            venta = Venta.objects.filter(estado=True,id__in=[p.id for p in oVentas],fecha__lte=fecha2).order_by('-id')
        elif producto !='':
            venta = Venta.objects.filter(estado=True,id__in=[p.id for p in oVentas],fecha__lte=fecha2).order_by('-id')
        elif dni !='':
            venta = Venta.objects.filter(estado=True,id__in=[p.id for p in oVentas],fecha__lte=fecha2).order_by('-id')
        else:
            oProductos=[]
            fecha2=datetime.strftime(datetime.strptime(fecha_fin,'%d-%m-%Y'),'%Y-%m-%d')
            #fecha2=date.today()
            venta = Venta.objects.filter(estado=True,fecha__lte=fecha2).order_by('-id')[:50]
            for oVenta in venta:
                pedido = Pedido.objects.filter(estado=True,id=oVenta.pedido_id)
                pedidoproductospresentacions = Pedidoproductospresentacions.objects.filter(pedido_id__in=[p.id for p in pedido])
                for oPedidopedidoproductopresentacion in pedidoproductospresentacions:
                    oNuevo={}
                    oNuevo['id']=oVenta.id
                    oNuevo['producto']=oPedidopedidoproductopresentacion.productopresentacions.producto.nombre
                    oProductos.append(oNuevo)
            oVentas = venta


    paginator = Paginator(oVentas,2)

    page = request.GET.get('page')
    try:
        ventaPagina = paginator.page(page)
    except PageNotAnInteger:
        ventaPagina = paginator.page(1)
    except EmptyPage:
        ventaPagina = paginator.page(paginator.num_pages)

    index = ventaPagina.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 5 if index >= 5 else 0
    end_index = index + 5 if index <= max_index - 5 else max_index
    page_range = paginator.page_range[start_index:end_index]
    return render(request,'venta/listar.html', {"oVenta": ventaPagina,"oProductos":oProductos,"page_range":page_range})



def FiltrarVentas(request, *args, **kwargs):
    producto = request.POST['producto_buscado']
    dni = request.POST['cliente_buscado']
    fecha_inicio = request.POST['desde']
    fecha_fin = request.POST['hasta']
    oProductos=[]
    oVentas=[]
    if producto != '':
        presentacion = Productopresentacions.objects.filter(producto=producto)
        pedidoproductopresentacion = Pedidoproductospresentacions.objects.filter(productopresentacions_id__in=[p.id for p in presentacion])
        pedido = Pedido.objects.filter(estado=True,id__in=[s.pedido_id for s in pedidoproductopresentacion])
        venta = Venta.objects.filter(estado=True,pedido_id__in=[p.id for p in pedido]).order_by("-id")
        productonombre = Producto.objects.get(id=producto).nombre
        for v in venta:
            oNuevo={}
            oNuevo['id']=v.id
            oNuevo['producto']=productonombre
            oProductos.append(oNuevo)
        oVentas = venta
    if dni != '':
        if producto != '':
            cliente = Cliente.objects.get(numerodocumento=dni)
            venta = Venta.objects.filter(estado=True,id__in=[p.id for p in oVentas],cliente_id=cliente.id).order_by('-id')

        else:
            oProductos=[]
            cliente = Cliente.objects.get(numerodocumento=dni)
            venta = Venta.objects.filter(estado=True,cliente_id=cliente.id).order_by('-id')
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
        fecha1=datetime.strftime(datetime.strptime(fecha_inicio,'%d-%m-%Y'),'%Y-%m-%d')
        fecha2=datetime.strftime(datetime.strptime(fecha_fin,'%d-%m-%Y'),'%Y-%m-%d')
        if producto !='' and dni!='':
            venta = Venta.objects.filter(estado=True,id__in=[p.id for p in oVentas],fecha__range=[fecha1,fecha2]).order_by('-id')
        elif producto !='':
            venta = Venta.objects.filter(estado=True,id__in=[p.id for p in oVentas],fecha__range=[fecha1,fecha2]).order_by('-id')
        elif dni !='':
            venta = Venta.objects.filter(estado=True,id__in=[p.id for p in oVentas],fecha__range=[fecha1,fecha2]).order_by('-id')
        else:
        #fecha2=date.today()
            oProductos = []
            venta = Venta.objects.filter(estado=True,fecha__range=[fecha1,fecha2]).order_by('-id')
            for oVenta in venta:
                pedido = Pedido.objects.filter(estado=True,id=oVenta.pedido_id)
                pedidoproductospresentacions = Pedidoproductospresentacions.objects.filter(pedido_id__in=[p.id for p in pedido])
                for oPedidopedidoproductopresentacion in pedidoproductospresentacions:
                    oNuevo={}
                    oNuevo['id']=oVenta.id
                    oNuevo['producto']=oPedidopedidoproductopresentacion.productopresentacions.producto.nombre
                    oProductos.append(oNuevo)
        oVentas = venta
    elif fecha_inicio!='':
        fecha1=datetime.strftime(datetime.strptime(fecha_inicio,'%d-%m-%Y'),'%Y-%m-%d')
        fecha2=date.today()
        if producto !='' and dni!='':
            venta = Venta.objects.filter(estado=True,id__in=[p.id for p in oVentas],fecha__range=[fecha1,fecha2]).order_by('-id')
        elif producto !='':
            venta = Venta.objects.filter(estado=True,id__in=[p.id for p in oVentas],fecha__range=[fecha1,fecha2]).order_by('-id')
        elif dni !='':
            venta = Venta.objects.filter(estado=True,id__in=[p.id for p in oVentas],fecha__range=[fecha1,fecha2]).order_by('-id')
        else:
            oProductos=[]
            venta = Venta.objects.filter(estado=True,fecha__range=[fecha1,fecha2]).order_by('-id')[:50]
            for oVenta in venta:
                pedido = Pedido.objects.filter(estado=True,id=oVenta.pedido_id)
                pedidoproductospresentacions = Pedidoproductospresentacions.objects.filter(pedido_id__in=[p.id for p in pedido])
                for oPedidopedidoproductopresentacion in pedidoproductospresentacions:
                    oNuevo={}
                    oNuevo['id']=oVenta.id
                    oNuevo['producto']=oPedidopedidoproductopresentacion.productopresentacions.producto.nombre
                    oProductos.append(oNuevo)
        oVentas = venta
    elif fecha_fin!='':
        fecha2=datetime.strftime(datetime.strptime(fecha_fin,'%d-%m-%Y'),'%Y-%m-%d')
        if producto !='' and dni!='':
            venta = Venta.objects.filter(estado=True,id__in=[p.id for p in oVentas],fecha__lte=fecha2).order_by('-id')
        elif producto !='':
            venta = Venta.objects.filter(estado=True,id__in=[p.id for p in oVentas],fecha__lte=fecha2).order_by('-id')
        elif dni !='':
            venta = Venta.objects.filter(estado=True,id__in=[p.id for p in oVentas],fecha__lte=fecha2).order_by('-id')
        else:
            oProductos=[]
            fecha2=datetime.strftime(datetime.strptime(fecha_fin,'%d-%m-%Y'),'%Y-%m-%d')
            #fecha2=date.today()
            venta = Venta.objects.filter(estado=True,fecha__lte=fecha2).order_by('-id')[:50]
            for oVenta in venta:
                pedido = Pedido.objects.filter(estado=True,id=oVenta.pedido_id)
                pedidoproductospresentacions = Pedidoproductospresentacions.objects.filter(pedido_id__in=[p.id for p in pedido])
                for oPedidopedidoproductopresentacion in pedidoproductospresentacions:
                    oNuevo={}
                    oNuevo['id']=oVenta.id
                    oNuevo['producto']=oPedidopedidoproductopresentacion.productopresentacions.producto.nombre
                    oProductos.append(oNuevo)
            oVentas = venta

    paginator = Paginator(oVentas,2)

    page = request.GET.get('page')
    try:
        ventaPagina = paginator.page(page)
    except PageNotAnInteger:
        ventaPagina = paginator.page(1)
    except EmptyPage:
        ventaPagina = paginator.page(paginator.num_pages)

    index = ventaPagina.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 5 if index >= 5 else 0
    end_index = index + 5 if index <= max_index - 5 else max_index
    page_range = paginator.page_range[start_index:end_index]

    return render(request, 'venta/listar.html', {"oVenta": ventaPagina,"oProductos":oProductos,"page_range":page_range})


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
