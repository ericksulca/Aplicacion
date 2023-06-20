"""ferreteria URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
#from django.conf.urls import url
from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from app.views import *
from app.Views.productoView import *
from app.Views.precioView import *
from app.Views.presentacionView import *
from app.Views.aperturacajaView import *
from app.Views.cierrecajaView import *
from app.Views.operacionView import *
from app.Views.pedidoView import *
from app.Views.usuarioView import *
from app.Views.clienteView import *
from app.Views.rutaView import *
from app.Views.visitaView import *
from app.Views.errorView import *

from app.Views.ventaView import *

from app.Views.loteView import *
###########################################################
#   Usuario: Erick Sulca, Ulises Bejar
#   Fecha: 05/06/18
#   Última modificación:
#   Descripción: url registrarError
###########################################################

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home, name='Home'),
    path('login/', Login, name='Login'),
    path('logout/', Logout, name='Logout'),
    path('prueba/', Prueba, name='prueba'),

    ################## Caja #######################
    path('Caja/apertura/', registrarAperturacaja),
    path('Caja/cierre/', registrarCierrecaja),
    path('Caja/movimiento/', registrarOperacion),

    ################## Venta #######################
    path('Venta/nuevo/', registrarPedido),

    ################## Producto #######################
    path('Producto/listar/', ListarProductos),
    path('Producto/nuevo/', registrarProducto),
    path('Producto/detalle/<int:producto_id>/', detalleProducto),
    path('Producto/editar/<int:producto_id>/', editarProducto),

    ################## Catalogo #######################
    path('Presentacion/Listar/<int:producto_id>/', presentacion_detalle),
    path('Presentacion/registrar/', registrarPresentacionProducto),
    path('Presentacion/eliminar/<int:presentacion_id>/<int:producto_id>/', eliminarPresentacionProducto),
    path('Presentacion/getPresentaciones/', getPresentaciones),

    path('Precios/getPrecios/', getPrecios),
    #path('pruebaExcel/', IngresarPrecios),

    ################## Cliente #######################
    path('Cliente/nuevo/', nuevoCliente, name='nuevo_cliente'),
    path('Cliente/detalle/<int:cliente_id>/', detalleCliente, name='detalle_cliente'),
    path('Cliente/editar/<int:cliente_id>/', editarCliente, name='editar_cliente'),
    path('Cliente/listar/', listarCliente, name='listar_cliente'),
    #path('Cliente/buscar/', IngresarPrecios),
    path('Cliente/actualizar/', IngresarPrecios, name='actualiza_cliente'),
    path('Cliente/eliminar/<int:pk>/', eliminar_cliente, name='eliminar_cliente'),

    ################## Pedidos #######################

    path('Pedido/nuevo/', registrarPedido),
    path('Pedido/listar/', ListarPedidos),
    path('Pedido/resumen/', ResumenPedidos),
    path('Pedido/detalle/<int:pedido_id>/', DetallePedido),
    path('Pedido/editar/<int:pedido_id>/', editarPedido),
    path('Pedido/eliminar/<int:pedido_id>/', eliminarPedido),
    path('Pedido/actualizar/', IngresarPrecios),
    path('Pedido/reporte/', IngresarPrecios),
    path('Pedido/buscar/', IngresarPrecios),
    path('Pedido/imprimir/', IngresarPrecios),


    ################## APP Movil #######################

    path('usuario/validar/', validarUsuario),
    path('usuario/ruta/', rutaUsuario),

    path('usuario/visita/cancelar/', cancelarVisita),
    path('usuario/visita/reiniciar/', reiniciarVisita),

    path('cliente/buscar/', buscarCliente),
    path('cliente/detalle/', detalleClienteWS),

    path('pedido/insertar/', InstarPedido),
    path('pedido/listar/', ListarPedido),
    path('pedido/detalle/', DetallePedidoMovil),
    path('pedido/editar/', DetallePedidoMovil),

    path('pago/nuevo/', IngresarPrecios),


    path('producto/buscar/', BuscarProducto),
    path('producto/presentacion/listar/', ListarPresentacionesProducto),
    path('producto/presentacion/cantidad/', CantidadPresentacionesProducto),

    path('error/registrar/', registrarError),


#######################Ventas##############################

    path('venta/nuevo/', nuevoVenta),
    path('venta/listar/', ListarVentas, name="venta_listar"),
    # path('venta/listar/<int:<producto_buscado>\d+)/<int:<dni>\d+)/<int:<fecha_ini>[0-9]{2}-?[0-9]{2}-?[0-9]{4})/<int:<fecha_f>[0-9]{2}-?[0-9]{2}-?[0-9]{4})/', Fentas),
    # path('venta/listar/<int:<producto_buscado>\d+)/<int:<dni>\d+)/', Fentas),
    #
    # path('venta/listar/<int:<producto_buscado>)/$', Fentas,name="listar_productoid"),
    # path('venta/listar/<int:<dni>\d+)/$', Fentas),
    # path('venta/listar/<int:<fecha_ini>[0-9]{2}-?[0-9]{2}-?[0-9]{4})/<int:<fecha_f>[0-9]{2}-?[0-9]{2}-?[0-9]{4})/$', Fentas),
    # path('venta/listar/<int:<fecha_f>[0-9]{2}-?[0-9]{2}-?[0-9]{4})/$', Fentas),
    path('venta/filtrar/', Ventas, name = "filtra_ventas"),
    #path('venta/listar/<int:<producto>\d+)$', FiltrarVentas.as_view, name="filtra_ventas"),
    #path('Producto/detalle/<int:<producto_id>\d+)/$', detalleProducto),
    #path('Producto/editar/<int:<producto_id>\d+)/$', editarProducto),

    path('Lote/nuevo/', nuevoLote),
    #####################################################

#######################Rutas##############################

    #path('Ruta/nuevo/$', nuevoVenta),
    #path('Ruta/listar/$', ListarVenta),

#######################Información y Reportes##############################

    #path('Reporte/almacen/$', reporteAlmacen),
    #path('Reporte/caja/$', reporteCaja),
    #path('Reporte/ventas/$', reporteVentas),

]
