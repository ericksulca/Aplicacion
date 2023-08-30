# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from app.models import *

# Register your models here.
admin.site.register(Negocio)
admin.site.register(Proveedor)
admin.site.register(Presentacion)
admin.site.register(Producto)
admin.site.register(Producto_presentacions)
#admin.site.register(Categoria)
admin.site.register(Cliente)
admin.site.register(Venta)
admin.site.register(Pedido)
admin.site.register(Pedido_productopresentacions)
#admin.site.register(Almacen)
#admin.site.register(Caja)
admin.site.register(Aperturacaja)
admin.site.register(Cierrecaja)
admin.site.register(Lote)
admin.site.register(Lote_productopresentacions)
admin.site.register(Operacion)
admin.site.register(Tipooperacion)
admin.site.register(Detalletipooperacion)
