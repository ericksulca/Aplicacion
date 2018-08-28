# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from ferreteria import settings
from django.contrib.auth.decorators import login_required
# Create your views here.
from app.models import *
from app.views import *
from ferreteria.urls import *
from django.views.decorators.csrf import csrf_exempt
import json
from app.fomularios.productoForm import *
from django.views.generic import DetailView
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
        return render(request, 'Producto/listar.html')
    else:
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
            oPresentacion = Presentacion.objects.get(id = int(Datos['cmbPresentacionPrincipal']))
            oProducto.presentacions.add(oPresentacion)
            oProductopresentacions = Productopresentacions.objects.get(producto=oProducto, presentacion=oPresentacion)
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
            return render(request, 'producto/agregarPresentacion.html')
        else:
            return render(request, 'producto/listar.html')

    else:
        form = ProductoForm()
        oPrecios = Precio.objects.filter(estado=True)
        oPresentaciones = Presentacion.objects.filter(estado=True)
    return render(request, 'producto/registrar.html', {'form': form,'precios':oPrecios,'presentaciones':oPresentaciones})

@csrf_exempt
def BuscarProducto (request):
    if request.method == 'POST':
        Datos = json.loads(request.body)
        #print Datos
        usuario=True
        #usuario= BuscarUsuario(Datos["idUsuario"])
        
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
                print ("------------------")
                print (oProducto.imagen)
                print ("------------------")
                if oProducto.imagen=="":
                    jsonProducto["imagen"] = "/imagen/default.jpg"
                else:
                    jsonProducto["imagen"] = oProducto.imagen.url
                jsonProductos["productos"].append(jsonProducto)

            return HttpResponse(json.dumps(jsonProductos), content_type="application/json")

        if request.is_ajax:
            palabra=request.GET.get('term','')

            doctores=Doctor.objects.filter(name__icontains=palabra)

            results=[]

            for doctor in doctores:
                doctor_json={}
                doctor_json['label']=doctor.name
                doctor_json['value']=doctor.name
                results.append(doctor_json)

            data_json=json.dumps(results)
        else:
            data_json='fail'
        mimetype="application/json"
        return HttpResponse(data_json,mimetype)



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

"""
def detalleProducto(request,producto_id):
    if request.method == 'GET':
        idProducto = int(producto_id)
        oProducto = Producto.objects.get(id = idProducto)
        form = ProductoForm(instance= oProducto)
        oProductospresentacions = Productopresentacions.objects.filter(producto = oProducto)
        oProductos = []

        for oProductospresentacion in oProductospresentacions:
            oProdu = {}
            oProdu["nombrePresentacions"] = oProductospresentacion.presentacion.nombre
            oProductos.append(oProdu)
            print(oProductos)
            return render(request, 'producto/detalle.html', {"form": form, "oPresentacion": oProducto.presentacions, "oProductos":oProductos})
    else:
        oPedi = Producto.objects.filter(estado = True)
        return render(request, 'producto/listar.html',{"oProductos": oPedi})
"""
def detalleProducto(request,producto_id):
    
    oProducto = Producto.objects.get(pk=producto_id)
    return render(request, 'producto/detalle.html', {'oProducto':oProducto})

def editarProducto(request,producto_id):
    oProducto = Producto.objects.get(id = producto_id)
    if request.method=='POST':
        form = ProductoForm(request.POST, request.FILES, instance=oProducto)
        if form.is_valid():
            edit_prod=form.save(commit=False)
            form.save_m2m()
            edit_prod.status=True
            edit_prod.save()
           
            return redirect('/Producto/listar/')
    else:
        form= ProductoForm(instance=oProducto)
        ctx = {'form':form}
    return render(request, 'Producto/editar.html',ctx)
   
"""
def actualizarProducto(request, producto_id):
    oProducto=Producto.objects.get(id=producto_id)
    if request.method=='POST':
        form= ProductoForm(request.POST, instance=oProducto)
        form.save()

    return 

    """