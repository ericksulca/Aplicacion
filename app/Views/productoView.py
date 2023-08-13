# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from rest_framework.generics import (ListAPIView)

from ferreteria import settings
from ferreteria.urls import *
# Create your views here.
from app.fomularios.productoForm import *
from app.models import *
from app.views import *

import json
###########################################################
#   Usuario: Erick Sulca, Ulises Bejar
#   Fecha: 05/06/18
#   Última modificación:
#   Descripción:
#   servicio de busqueda de usuario para la app movil,
#   y en buscaar producto retorno de imagen.
###########################################################

def ListarProductos(request):
    if request.method == 'POST':
        return render(request, 'pedido/listar.html')
    if request.method == 'GET':
        oProductos = Producto.objects.filter(estado = True)
        return render(request, 'producto/listar.html', {"oProductos": oProductos})

def registrarProducto(request):
    if request.method == 'POST':
        Datos = request.POST
        form = ProductoForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            oProducto = form
            #oPresentacion = Presentacion.objects.get(id = int(Datos['cmbPresentacionPrincipal']))
            #oProducto.presentacions.add(oPresentacion)
            '''oProductopresentacions = Productopresentacions.objects.get(producto=oProducto, presentacion=oPresentacion)
            oProductopresentacions.valor = 1
            oProductopresentacions.unidadprincipal = True
            oProductopresentacions.save()
            oPrecios = Precio.objects.filter(estado=1)
            for oPrecio in oPrecios:
                oProductoPresentacionsprecios = Productopresentacionsprecios()
                oProductoPresentacionsprecios.precio = oPrecio
                oProductoPresentacionsprecios.productopresentacions = oProductopresentacions
                idPrecio = str(oPrecio.id)
                oProductoPresentacionsprecios.valor = Datos[idPrecio]
                oProductoPresentacionsprecios.save()
            '''
            return redirect('/Producto/listar/')
            #return render(request, 'producto/listar.html')
            #return render(request, 'producto/agregarPresentacion.html')
        else:
            return render(request, 'producto/listar.html')

    else:
        form = ProductoForm()
        #oPrecios = Precio.objects.filter(estado=True)
        #oPresentaciones = Presentacion.objects.filter(estado=True)
    return render(request, 'producto/registrar.html', {'form': form,'precios':'','presentaciones':''})

@csrf_exempt
def BuscarProducto (request):
    if request.method == 'POST':
        Datos = json.loads(request.body)
        usuario=True

        if usuario==True:
            nombreProducto = Datos["nombreProducto"]
            oProductos = Producto.objects.filter(nombre__icontains=nombreProducto,estado = True)
            jsonProductos = {}
            jsonProductos["productos"] = []
            for oProducto in oProductos:
                jsonProducto = {}
                jsonProducto["id"] = oProducto.id
                jsonProducto["nombre"] = oProducto.nombre
                jsonProducto["codigo"] = oProducto.codigo
                jsonProducto["precio"] = oProducto.precio
                jsonProductos["productos"].append(jsonProducto)
            
            print(jsonProductos)
            return HttpResponse(json.dumps(jsonProductos), content_type="application/json")

from app.serializers import ProductoSerializer
class get_Productos(ListAPIView):
    serializer_class = ProductoSerializer
    def get_queryset(self):
        oProductos = Producto.objects.filter(estado = True)
        return oProductos

@csrf_exempt
def ListarPresentacionesProducto (request):
    if request.method == 'POST':
        Datos = json.loads(request.body)
        #print Datos
        usuario=True
        # usuario= BuscarUsuario(Datos["idUsuario"])
        if usuario==True:
            idProducto = Datos["idProducto"]
            oProuctoPresentaciones = Productopresentacions.objects.filter(producto= idProducto)
            #print oProuctoPresentaciones
            jsonPresentaciones = {}
            jsonPresentaciones["presentaciones"] = []
            for oProuctoPresentacion in oProuctoPresentaciones:
                jsonPresentacion = {}
                jsonPresentacion["id"] = oProuctoPresentacion.presentacion.id
                jsonPresentacion["nombre"] = oProuctoPresentacion.presentacion.nombre
                jsonPresentacion["codigo"] = oProuctoPresentacion.presentacion.codigo
                jsonPresentacion["valor"] = oProuctoPresentacion.valor
                OProductopresentacionsprecios = Productopresentacionsprecios.objects.filter(productopresentacions = oProuctoPresentacion.presentacion.id)
                jsonPrecios = []
                for OProductopresentacionsprecio in OProductopresentacionsprecios:
                    jsonPrecio = {}
                    jsonPrecio["id"] = OProductopresentacionsprecio.precio.id
                    jsonPrecio["nombrePrecio"] = OProductopresentacionsprecio.precio.nombre
                    jsonPrecio["precio"] = OProductopresentacionsprecio.valor
                    jsonPrecios.append(jsonPrecio)
                jsonPresentacion["valor"] =jsonPrecios
                jsonPresentaciones["presentaciones"].append(jsonPresentacion)

            return HttpResponse(json.dumps(jsonPresentaciones), content_type="application/json")

#<QueryDict: {u'imagen': [u''], u'url': [u''], u'1': [u'1'], u'3': [u'1'], u'2': [u'1'], u'nombre': [u'asd'], u'csrfmiddlewaretoken': [u'nsbA68zMnq7Ez6Gi2zEKqQQ45t5yWukYwqC9Tuo3Frl23Q9xajNt8htfhJQzWpP7'], u'codigo': [u''], u'cantidadPrincipal': [u'1']}>
#
#
@csrf_exempt
def CantidadPresentacionesProducto (request):
    if request.method == 'POST':
        Datos = json.loads(request.body)
        usuario=True
        # usuario= BuscarUsuario(Datos["idUsuario"])
        if usuario==True:
            idProducto = Datos["idProducto"]
            idPresentacion = Datos["idPresentacion"]
            jsonProducto = {}
            oProucto = Producto.objects.get(id = idProducto)
            oProductopresentacions = Productopresentacions.objects.get(producto = oProucto , presentacion = idPresentacion)
            jsonProducto["cantidad"] = (oProucto.cantidad)*(oProductopresentacions.valor)
            return HttpResponse(json.dumps(jsonProducto), content_type="application/json")


def detalleProducto(request,producto_id):
    oProducto = Producto.objects.get(id=producto_id,estado=True)
    return render(request, 'producto/detalle.html', {'oProducto':oProducto})


def editarProducto(request,producto_id):
    oProducto = Producto.objects.get(id = producto_id)
    if request.method == 'POST':
        Datos = request.POST
        form = ProductoForm(request.POST or None, instance=oProducto)
        if form.is_valid():
            form = form.save()
            return redirect('/Producto/listar/')

       # else:
        #    return render(request, '/Cliente/error.html')
    else:
        form = ProductoForm(request.POST or None, instance=oProducto)
        print(form)
        return render(request, 'producto/editar.html', {'form': form})


def eliminar_producto(request,pk):
    oProducto = Producto.objects.get(pk=pk)
    oProducto.estado = False
    oProducto.save()
    response = {'exito':1}
    #return JsonResponse(response)
    #return redirect('listar_producto', kwargs={})
    return HttpResponseRedirect(reverse("listar_producto"))
