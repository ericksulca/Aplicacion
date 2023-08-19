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
from app.Views.presentacionView import *
from app.Views.precioView import *
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
    path('Caja/imprimir/', imprimir_prueba, name='imprimir_caja'),
    path('Caja/apertura/', registrarAperturacaja, name='apertura_caja'),
    path('Caja/cierre/', registrarCierrecaja, name='cierre_caja'),
    path('Caja/operacion/', registrarOperacion, name='operacion_caja'),
    path('Caja/operacion/detalle/<int:id_operacion>', detalleOperacion, name='operaciones_detalle'),
    path('Caja/operaciones/listar', listarOperacions, name='operaciones_listar'),

    ################## Venta #######################
    path('Venta/nuevo/', registrarPedido, name='registrar_venta'),

    ################## Producto #######################
    path('Producto/listar/', ListarProductos, name ='listar_producto'),
    path('Producto/nuevo/', registrarProducto, name ='registrar_producto'),
    path('Producto/detalle/<int:producto_id>/', detalleProducto, name ='ver_producto'),
    path('Producto/editar/<int:producto_id>/', editarProducto, name ='editar_producto'),
    path('Producto/eliminar/<int:pk>/', eliminar_producto, name='eliminar_producto'),

    ################## Catalogo #######################
    #path('Presentacion/Listar/<int:producto_id>/', presentacion_detalle, name ='listar_presentacion'),
    #path('Presentacion/registrar/', registrarPresentacionProducto, name ='registrar_presentacion'),
    #path('Presentacion/eliminar/<int:presentacion_id>/<int:producto_id>/', eliminarPresentacionProducto, name ='eliminar_presentacion'),
    #path('Presentacion/getPresentaciones/', getPresentaciones, name ='get_presentacion'),
#
    #path('Precios/getPrecios/', getPrecios, name ='get_precios'),
    #path('pruebaExcel/', IngresarPrecios),

    ################## Cliente #######################
    path('Cliente/nuevo/', nuevoCliente, name='nuevo_cliente'),
    path('Cliente/detalle/<int:cliente_id>/', detalleCliente, name='detalle_cliente'),
    path('Cliente/editar/<int:cliente_id>/', editarCliente, name='editar_cliente'),
    path('Cliente/listar/', listarCliente, name='listar_cliente'),
    #path('Cliente/buscar/', IngresarPrecios),
    path('Cliente/actualizar/', IngresarPrecios, name='actualiza_cliente'),
    path('Cliente/eliminar/<int:pk>/', eliminar_cliente, name='eliminar_cliente'),
    
    ################## Lote #######################
    path('Lote/nuevo/', nuevoLote, name='nuevo_lote'),
    path('Lote/listar/', listarLote, name='listar_lote'),
    path('Lote/detalle/<int:lote_id>/', detalleLote, name ='ver_lote'),
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
    path('pedido/alerta/listar/',Listar_PedidoAlertaView.as_view(),name = 'listar_pedidoalertas'),

    path('pago/nuevo/', IngresarPrecios),


    path('producto/buscar/', BuscarProducto, name='buscar_producto'),
    path('producto/json_listar/', get_Productos.as_view(), name='listar_productos'),
    
    #path('producto/presentacion/listar/', ListarPresentacionesProducto),
    path('producto/presentacion/listar/', get_PresentacionProducto.as_view()),

    path('detalletipooperacion/lista/',get_detalleTipoOperacion.as_view(),name ='listar_detalletipooperacio'),


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

    

    #####################################################

#######################Rutas##############################

    #path('Ruta/nuevo/$', nuevoVenta),
    #path('Ruta/listar/$', ListarVenta),

#######################Información y Reportes##############################

    #path('Reporte/almacen/$', reporteAlmacen),
    #path('Reporte/caja/$', reporteCaja),
    #path('Reporte/ventas/$', reporteVentas),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
