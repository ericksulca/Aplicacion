from __future__ import unicode_literals

from django.shortcuts import render
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

def nuevoLote(request):
    if request.method == 'POST':
        Datos = request.POST
        data = json.loads(request.body.decode('utf-8'))
        print(data)

        # PRODUCTO ALMACENS REQUIRED: | CANTIDAD | PRODUCTO_PRESENTACION | ALMACEN | LOTE
        oAlmacen = Almacen.objects.filter(estado=True)
        oAlmacen = oAlmacen[0]
        oLote = Lote()
        oAlmacen = Almacen.objects.get(id=data['almacen'])
        oProveedor = Proveedor.objects.get(id=data['proveedor'])
        oLote.proveedor= oProveedor
        oLote.almacen= oAlmacen
        oLote.save()

        for item in data['productos']:
            oLote_productopresentacions = Lote_productopresentacions()
            oLote_productopresentacions.cantidad = int(item['cantidad_producto'])
            oLote_productopresentacions.cnt_cantidad = int(item['cantidad_producto'])
            oLote_productopresentacions.precio_lote = float(item['precio_producto'])
            oPresentacion = Presentacion.objects.get(codigo=item['presentacion_producto'])
            oProducto = Producto.objects.get(id= item['id'],nombre = item['nombre_producto'] )
            oProducto_presentacions = Producto_presentacions.objects.get(producto=oProducto,presentacion=oPresentacion)
            oLote_productopresentacions.producto_presentacions = oProducto_presentacions
            oLote_productopresentacions.lote = oLote
            oLote_productopresentacions.save()
        


        #'nombre_producto': 'Producto 01', 'presentacion_producto': 'CA', 'cantidad_producto': '10', 'precio_producto': '3.00', 'fechaVenc_producto': ''

        print("############ log POST function nuevo_Lote #############")

        #print(Datos)
        jsonProductos= {}
        
        #oPresentacion = Presentacion.objects.get(id = int(Datos['cmbPresentacionPrincipal']))
        #oProducto.presentacions.add(oPresentacion)
        return HttpResponse(json.dumps(jsonProductos), content_type="application/json")
        #return render(request, 'lote/nuevo.html')
    else:
        form = ProductoForm()
        #oPrecios = Precio.objects.filter(estado=True)
        oAlmacens = Almacen.objects.filter(estado=True)
        oProveedors = Proveedor.objects.filter(estado=True)
        oProductosTop = Producto.objects.filter(estado=True).order_by('-valor')[:9]
    return render(request, 'lote/nuevo.html', {'form': form,'oAlmacens':oAlmacens, 'oProveedors':oProveedors, 'oProductosTop': oProductosTop})


