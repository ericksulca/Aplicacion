# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from app.models import *

# Register your models here.
admin.site.register(Proveedor)
admin.site.register(Presentacion)
admin.site.register(Producto)
admin.site.register(Producto_presentacions)
admin.site.register(Categoria)
admin.site.register(Cliente)
admin.site.register(Venta)
admin.site.register(Pedido)
admin.site.register(Empleado)
admin.site.register(Almacen)
admin.site.register(Caja)
