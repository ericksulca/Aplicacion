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

from app.serializers import ProductoSerializer, LoteSerializer

class get_Lotes(ListAPIView):
    serializer_class = LoteSerializer
    def get_queryset(self):
        oLotes = Lote.objects.filter(estado = True)
        return oLotes
    
def detalleLote(request,lote_id):
    oLote = Lote.objects.get(id=lote_id,estado=True)
    oLote_productopresentacions = Lote_productopresentacions.objects.filter(lote=oLote)
    return render(request, 'lote/detalle.html', {'oLote':oLote, 'oLote_productopresentacions':oLote_productopresentacions})
    
def listarLote(request):
    if request.method == 'POST':
        return render(request, 'lote/listar.html', {"oLotes": oLotes})
    if request.method == 'GET':
        oLotes = Lote.objects.filter(estado = True)
        return render(request, 'lote/listar.html', {"oLotes": oLotes})

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
        oLote.nro_documento= data['nroDocumento']
        oLote.almacen= oAlmacen
        oLote.save()
        total_precio_lote = 0

        for item in data['productos']:
            oLote_productopresentacions = Lote_productopresentacions()
            oLote_productopresentacions.cantidad = int(item['cantidad_producto'])
            oLote_productopresentacions.cnt_cantidad = int(item['cantidad_producto'])
            oLote_productopresentacions.precio_lote = float(item['precio_producto'])
            total_precio_lote += float(item['precio_producto'])
            oPresentacion = Presentacion.objects.get(codigo=item['presentacion_producto'])
            oProducto = Producto.objects.get(id= item['id'],nombre = item['nombre_producto'] )
            oProducto_presentacions = Producto_presentacions.objects.get(producto=oProducto,presentacion=oPresentacion)
            oLote_productopresentacions.producto_presentacions = oProducto_presentacions
            oLote_productopresentacions.lote = oLote
            oLote_productopresentacions.fecha_caducidad = item['fechaVenc_producto']
            oLote_productopresentacions.save()

        oLote.monto = total_precio_lote
        oLote.save()
        oOperacion = Operacion()
        oOperacion.monto = data['monto_pago'] #calcular monto Total Lote
        oOperacion.descripcion = 'Ingreso de Productos'
        oAperturacaja = Aperturacaja.objects.latest('id')
        if  oAperturacaja.activo==True:
            oOperacion.aperturacaja = oAperturacaja
        else:
            return redirect('apertura_caja')
        #funcion estado Caja Activo: true | false
        
        oDetalletipooperacion = Detalletipooperacion.objects.get(nombre='Pago Proveedor')

        oOperacion.detalletipooperacion = oDetalletipooperacion
        oOperacion.lote = oLote
        oOperacion.save()
        print("############ log POST function nuevo_Lote #############")
        #print(Datos)
        jsonProductos = {'exito':1}
        return HttpResponse(json.dumps(jsonProductos), content_type="application/json")
    else:
        form = ProductoForm()
        #oPrecios = Precio.objects.filter(estado=True)
        oAlmacens = Almacen.objects.filter(estado=True)
        oProveedors = Proveedor.objects.filter(estado=True)
        oProductosTop = Producto.objects.filter(estado=True).order_by('-valor')[:9]
    return render(request, 'lote/nuevo.html', {'form': form,'oAlmacens':oAlmacens, 'oProveedors':oProveedors, 'oProductosTop': oProductosTop})


