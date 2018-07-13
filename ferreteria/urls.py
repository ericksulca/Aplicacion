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
from django.conf.urls import url
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

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', Home),
    url(r'^login/$', Login),
    url(r'^logout/$', Logout),
    url(r'^home/$', Home),
    url(r'^Home/$', Home),
    url(r'^prueba/$', Prueba),
    url(r'^Caja/apertura/$', registrarAperturacaja),
    url(r'^Caja/cierre/$', registrarCierrecaja),
    url(r'^Caja/movimiento/$', registrarOperacion),

    url(r'^Venta/nuevo/$', registrarPedido),

    url(r'^Producto/listar/$', ListarProductos),
    url(r'^Producto/nuevo/$', registrarProducto),

    url(r'^Presentacion/Listar/(?P<producto_id>\d+)/$', presentacion_detalle),
    url(r'^Presentacion/registrar/$', registrarPresentacionProducto),
    url(r'^Presentacion/eliminar/(?P<presentacion_id>\d+)/(?P<producto_id>\d+)/$', eliminarPresentacionProducto),
    url(r'^Presentacion/getPresentaciones/$', getPresentaciones),
    
    url(r'^Precios/getPrecios/$', getPrecios),
    #url(r'^pruebaExcel/$', IngresarPrecios),
    ################## Cliente #######################
    url(r'^Cliente/nuevo/$', nuevoCliente),
    url(r'^Cliente/detalle/(?P<cliente_id>\d+)/$', detalleCliente),
    url(r'^Cliente/editar/(?P<cliente_id>\d+)/$', editarCliente),
    url(r'^Cliente/listar/$', listarCliente),
    url(r'^Cliente/buscar/$', IngresarPrecios),
    url(r'^Cliente/actualizar/$', IngresarPrecios),
    
    ################## Pedidos #######################

    url(r'^Pedido/nuevo/$', IngresarPrecios),
    url(r'^Pedido/listar/$', ListarPedidos),
    url(r'^Pedido/resumen/$', ResumenPedidos),
    url(r'^Pedido/detalle/(?P<pedido_id>\d+)/$', DetallePedido),
    url(r'^Pedido/actualizar/$', IngresarPrecios),
    url(r'^Pedido/reporte/$', IngresarPrecios),
    url(r'^Pedido/buscar/$', IngresarPrecios),
    url(r'^Pedido/imprimir/$', IngresarPrecios),
    
    ################## APP Movil #######################
    
    url(r'^usuario/validar/$', validarUsuario),
    url(r'^usuario/ruta/$', rutaUsuario),

    url(r'^usuario/visita/cancelar/$', cancelarVisita),
    url(r'^usuario/visita/reiniciar/$', reiniciarVisita),

    url(r'^cliente/buscar/$', buscarCliente),
    url(r'^cliente/detalle/$', detalleClienteWS),

    url(r'^pedido/insertar/$', InstarPedido),
    url(r'^pedido/listar/$', ListarPedido),
    url(r'^pedido/detalle/$', DetallePedidoMovil),
    url(r'^pedido/editar/$', DetallePedidoMovil),

    url(r'^pago/nuevo/$', IngresarPrecios),

    url(r'^producto/buscar/$', BuscarProducto),
    url(r'^producto/presentacion/listar/$', ListarPresentacionesProducto),
    url(r'^producto/presentacion/cantidad/$', CantidadPresentacionesProducto),

    url(r'^error/registrar/$', registrarError),
    #####################################################
]
