# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals
 
from django.db import models
from django.contrib.auth.models import User
from django_resized import ResizedImageField

class Almacen(models.Model):
    nombre = models.CharField(max_length=45)
    estado = models.BooleanField(blank=True,default=True)
    def __str__(self):
        return str(self.nombre)
    
class Caja(models.Model):
    nombre = models.CharField(max_length=45)
    estado = models.BooleanField(blank=True,default=True)
    def __str__(self):
        return str(self.nombre)
    
class Aperturacaja(models.Model):
    fecha = models.DateTimeField(auto_now_add=True, blank=False)
    monto = models.FloatField()
    activo = models.BooleanField(blank=True,default=True)
    estado = models.BooleanField(blank=True,default=True)
    caja = models.ForeignKey(Caja, on_delete=models.CASCADE)

class Categoria(models.Model):
    nombre = models.CharField(max_length=45)
    estado = models.BooleanField(blank=True,default=True)
    def __str__(self):
        return str(self.nombre)
    
class Cierrecaja(models.Model):
    fecha = models.DateTimeField(auto_now_add=True, blank=True)
    monto = models.FloatField()
    estado = models.BooleanField(blank=True,default=True)
    aperturacaja = models.ForeignKey(Aperturacaja, on_delete=models.CASCADE, related_name='apertura_cierrecaja')  # Field name made lowercase.

class Cliente(models.Model):
    nombre = models.CharField(max_length=45)
    direccion = models.CharField(max_length=45,blank=True, null=True)
    numerodocumento = models.CharField(max_length=11, blank=True, null=True)
    telefono = models.CharField(max_length=15,blank=True, null=True)
    imagen = ResizedImageField(size=[100, None],upload_to='clientes/', default="/imagen/default_cliente.jpg", blank=True, null=True)#upload_to='%Y/%m/%d',
    longitud = models.CharField(max_length=25, blank=True, null=True)
    latitud = models.CharField(max_length=25, blank=True, null=True)
    estado = models.BooleanField(blank=True,default=True)

    def __str__(self):
        return str(self.nombre)

class Cobro(models.Model):
    fecha = models.DateTimeField(auto_now_add=True, blank=True)
    monto = models.FloatField()
    estado = models.BooleanField(blank=True,default=True)
    venta = models.ForeignKey('Venta', on_delete=models.CASCADE)  # Field name made lowercase.
    #recibo = models.ForeignKey('Recibo', blank=True, null=True, on_delete=models.CASCADE)  # Field name made lowercase.

class Detalletipooperacion(models.Model):
    nombre = models.CharField(max_length=45)
    estado = models.BooleanField(blank=True,default=True)
    tipooperacion = models.ForeignKey('Tipooperacion', on_delete=models.CASCADE)  # Field name made lowercase.
    def __str__(self):
        return self.nombre

class Lote(models.Model):
    fecha = models.DateTimeField(auto_now_add=True, blank=True)
    modificado = models.DateTimeField(auto_now=True, blank=True)
    proveedor = models.ForeignKey('Proveedor', on_delete=models.CASCADE)  # Field name made lowercase.
    nro_documento = models.CharField(max_length=45, blank=True, null=True)
    almacen = models.ForeignKey('Almacen', on_delete=models.CASCADE, blank=True,null=True)  # Field name made lowercase.
    monto = models.FloatField(blank=True, null=True)
    estado = models.BooleanField(blank=True,default=True)

    def __str__(self):
        str_return = 'Fecha : '+str(self.fecha) + ' - Monto S/. ' + str(self.monto)
        return str_return
    
class Operacion(models.Model):
    fecha = models.DateTimeField(auto_now_add=True, blank=True)
    monto = models.FloatField()
    descripcion = models.TextField(blank=True, null=True)
    aperturacaja = models.ForeignKey(Aperturacaja, on_delete=models.CASCADE)  # Field name made lowercase.
    detalletipooperacion = models.ForeignKey(Detalletipooperacion, on_delete=models.CASCADE)  # Field name made lowercase.
    venta = models.ForeignKey('Venta', blank=True, null=True, on_delete=models.CASCADE, related_name='venta_operacions')  # Field name made lowercase.
    lote = models.ForeignKey('Lote', blank=True, null=True, on_delete=models.CASCADE, related_name='lote_operacions')  # Field name made lowercase.
    estado = models.BooleanField(blank=True,default=True)
    def __str__(self):
        str_return = 'Fecha : '+str(self.fecha) + ' - Monto S/. ' + str(self.monto)
        return str_return
    
class Pedido(models.Model):
    fecha = models.DateTimeField(auto_now_add=True, blank=True)
    usuario = models.OneToOneField(User, on_delete= models.DO_NOTHING, related_name='usuario_pedidos', blank=True, null=True)
    cliente = models.ForeignKey(Cliente, blank=True, null=True, on_delete=models.CASCADE)  # Field name made lowercase.
    estado = models.BooleanField(blank=True,default=True)
    def __str__(self):
        return str(self.fecha)

class Empleado(models.Model):
    nombre = models.CharField(max_length=45)
    imei = models.CharField(max_length=45, blank=True, null=True)
    imagen = models.ImageField(blank=True, null=True)#upload_to='%Y/%m/%d',
    perfil = models.IntegerField(blank=True, null=True,default=1)
    estado = models.BooleanField(blank=True,default=True)

    def __str__(self):
        return str(self.nombre)
    
class Producto(models.Model):
    nombre = models.CharField(max_length=45)
    codigo = models.CharField(max_length=45, blank=True, null=True)
    cantidad = models.FloatField(default=0,blank=True, null=True)
    imagen = ResizedImageField(size=[100, None],upload_to='productos/', default="/imagen/default.jpg", blank=True, null=True)#upload_to='%Y/%m/%d',
    #ResizedImageField(size=[500, 300], upload_to=get_image_path, blank=True, null=True)

    url = models.CharField(max_length=100, blank=True, null=True)
    valor = models.FloatField(default=1,blank=True)
    precio = models.FloatField(default=1,blank=True)
    estado = models.BooleanField(blank=True,default=True)

    def __str__(self):
        return str(self.nombre)
    
class Presentacion(models.Model):
    nombre = models.CharField(max_length=45)
    codigo = models.CharField(max_length=45, blank=True, null=True, unique=True)
    estado = models.BooleanField(blank=True,default=True)

    def __str__(self):
        return str(self.nombre)
    
class Producto_presentacions(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)  # Field name made lowercase.
    presentacion = models.ForeignKey(Presentacion, on_delete=models.CASCADE)  # Field name made lowercase.
    precio_compra = models.FloatField(default=0,blank=True)
    precio_venta = models.FloatField(default=0,blank=True)
    valor = models.FloatField(default=1,blank=True)
    favorito = models.BooleanField(blank=True,default=False)
    estado = models.BooleanField(blank=True,default=True)
    
    def __str__(self):
        str_producto_presentacions = 'Producto: '+self.producto.nombre+' | Presentación: '+self.presentacion.nombre
        return str(str_producto_presentacions)
    
class Pedido_productopresentacions(models.Model):
    cantidad = models.FloatField(blank=True,null=True)
    producto_presentacions = models.ForeignKey(Producto_presentacions, on_delete=models.CASCADE)  # Field name made lowercase.
    pedido = models.ForeignKey(Pedido, on_delete=models.DO_NOTHING, related_name='pedido_presentacions')
    precio_pedido = models.FloatField(default=0,blank=True)
    #fecha_caducidad = models.DateTimeField(null=True, blank=True)
    estado = models.BooleanField(blank=True,default=True)
    def __str__(self):
        str_pedido_productos = 'Producto: '+self.producto_presentacions.producto.nombre+' | Presentación: '+self.producto_presentacions.presentacion.nombre
        return str(str_pedido_productos)

class Lote_productopresentacions(models.Model):
    cantidad = models.FloatField(blank=True,null=True)
    cnt_cantidad = models.FloatField(blank=True,null=True) # descuento respectoa ventas 
    producto_presentacions = models.ForeignKey(Producto_presentacions, on_delete=models.CASCADE)  # Field name made lowercase.
    precio_lote = models.FloatField(default=0,blank=True, )
    lote = models.ForeignKey(Lote, on_delete=models.DO_NOTHING, related_name="lote_presentacions")
    fecha_caducidad = models.DateTimeField(null=True, blank=True)
    estado = models.BooleanField(blank=True,default=True)
    def __str__(self):
        str_lote_productos = 'Producto: '+self.producto_presentacions.producto.nombre+' | Presentación: '+self.producto_presentacions.presentacion.nombre
        return str(str_lote_productos)

    # FUNCION CANTIDAD CONTAR_STOCK() ON
class Producto_categorias(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)  # Field name made lowercase.
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)  # Field name made lowercase.

class Proveedor(models.Model):
    nombre = models.CharField(max_length=45)
    direccion = models.CharField(max_length=45)
    documento = models.CharField(max_length=45)
    estado = models.BooleanField(blank=True,default=True)

    def __str__(self):
        return str(self.nombre)

class Tipo_recibo(models.Model):
    nombre = models.CharField(max_length=45)
    estado = models.BooleanField(blank=True,default=True)

class Tipooperacion(models.Model):
    nombre = models.CharField(max_length=45)
    estado = models.BooleanField(blank=True,default=True)

    def __str__(self):
        return str(self.nombre)

class Venta(models.Model):
    fecha   = models.DateTimeField(auto_now_add=True, blank=True)
    monto   = models.FloatField()
    nrecibo = models.CharField(max_length=45, blank=True, null=True)
    pedido  = models.ForeignKey(Pedido, on_delete=models.CASCADE)  # Field name made lowercase.
    estado  = models.BooleanField(blank=True,default=True)
    #cliente = models.ForeignKey(Cliente, blank=True, null=True, on_delete=models.CASCADE)  # Field name made lowercase.

    def __str__(self):
        str_return = 'Fecha : '+str(self.fecha) + ' - Monto S/. ' + str(self.monto)
        return str_return
 
# tb1
# tb2


class Ruta(models.Model):
    nombre   = models.CharField(max_length=45)
    fecha    = models.DateTimeField(auto_now_add=True, blank=True)
    activo   = models.BooleanField(blank=True,default=True)
    estado   = models.BooleanField(blank=True,default=True)
    clientes = models.ManyToManyField(Cliente) 
    def __str__(self):
        return str(self.nombre)

class Rutaclientes(models.Model):
    ruta         = models.ForeignKey(Ruta, on_delete=models.CASCADE)
    cliente      = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha        = models.DateTimeField(auto_now_add=True, blank=True)
    modificacion = models.DateTimeField(auto_now=True, blank=True)
    activo       = models.BooleanField(blank=True,default=True)
    estado       = models.BooleanField(blank=True,default=True)

    class Meta:
        managed = False
        db_table = 'app_ruta_clientes'
    #     crear label's fecha ... estado en BD física

class Visita(models.Model):
    fecha        = models.DateTimeField(auto_now_add=True, blank=True)
    modificacion = models.DateTimeField(auto_now=True, blank=True)
    rutacliente  = models.ForeignKey(Rutaclientes, on_delete=models.CASCADE) 
    empleado     = models.ForeignKey('Empleado', on_delete=models.CASCADE)  # Field name made lowercase.
    nivel        = models.IntegerField(blank=True,null=True,default=1)
    activo       = models.BooleanField(blank=True,default=True)
    estado       = models.BooleanField(blank=True,default=True)
    clientes     = models.ManyToManyField(Cliente)

class Error(models.Model):
    fecha        = models.DateTimeField(auto_now_add=True, blank=True)
    descripcion = models.TextField(blank=True, null=True)
    actividad  = models.CharField(max_length=20)

class Alerta(models.Model):
    fecha = models.DateTimeField(auto_now_add=True, blank=True)
    usuario = models.OneToOneField(User, on_delete= models.DO_NOTHING, related_name='usuario_alertas')
    mensaje = models.TextField(blank=True, null=True)
    activo = models.BooleanField(blank=True,default=True)
    pedido  = models.ForeignKey(Pedido, on_delete=models.CASCADE, blank=True, null=True)  # Field name made lowercase.
    estado = models.BooleanField(blank=True,default=True)
    def __str__(self):
        return str(self.fecha)
class Negocio(models.Model):
    nombre   = models.CharField(max_length=45)
    ruc   = models.CharField(max_length=11)
    direccion = models.TextField(blank=True, null=True)
    imagen = ResizedImageField(size=[100, None],upload_to='negocio/', default="/imagen/default_negocio.jpg", blank=True, null=True)#upload_to='%Y/%m/%d',
    msg_cliente = models.TextField(blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    estado = models.BooleanField(blank=True,default=True)
    def __str__(self):
        return str(self.nombre)