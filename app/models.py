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
    aperturacaja = models.ForeignKey(Aperturacaja, on_delete=models.CASCADE)  # Field name made lowercase.

class Cliente(models.Model):
    nombre = models.CharField(max_length=45)
    direccion = models.CharField(max_length=45)
    longitud = models.CharField(max_length=25, blank=True, null=True)
    latitud = models.CharField(max_length=25, blank=True, null=True)
    numerodocumento = models.CharField(max_length=11, blank=True, null=True)
    estado = models.BooleanField(blank=True,default=True)

    def __str__(self):
        return str(self.nombre)

class Cobro(models.Model):
    fecha = models.DateTimeField(auto_now_add=True, blank=True)
    monto = models.FloatField()
    estado = models.BooleanField(blank=True,default=True)
    venta = models.ForeignKey('Venta', on_delete=models.CASCADE)  # Field name made lowercase.
    recibo = models.ForeignKey('Recibo', blank=True, null=True, on_delete=models.CASCADE)  # Field name made lowercase.

class Detalletipooperacion(models.Model):
    nombre = models.CharField(max_length=45)
    estado = models.BooleanField(blank=True,default=True)
    tipooperacion = models.ForeignKey('Tipooperacion', on_delete=models.CASCADE)  # Field name made lowercase.

class Lote(models.Model):
    fecha = models.DateTimeField(auto_now_add=True, blank=True)
    modificado = models.DateTimeField(auto_now=True, blank=True)
    estado = models.BooleanField(blank=True,default=True)
    proveedor = models.ForeignKey('Proveedor', on_delete=models.CASCADE)  # Field name made lowercase.
    recibo = models.ForeignKey('Recibo', on_delete=models.CASCADE)  # Field name made lowercase.
    

class Operacion(models.Model):
    fecha = models.DateTimeField(auto_now_add=True, blank=True)
    monto = models.FloatField()
    descripcion = models.TextField(blank=True, null=True)
    estado = models.BooleanField(blank=True,default=True)
    caja = models.ForeignKey(Caja, on_delete=models.CASCADE)  # Field name made lowercase.
    detalletipooperacion = models.ForeignKey(Detalletipooperacion, on_delete=models.CASCADE)  # Field name made lowercase.
    cobro = models.ForeignKey(Cobro, blank=True, null=True, on_delete=models.CASCADE)  # Field name made lowercase.
    def __str__(self):
        str_return = 'Fecha : '+str(self.fecha) + ' - Monto S/. ' + str(self.monto)
        return str_return
    
class Pedido(models.Model):
    fecha = models.DateTimeField(auto_now_add=True, blank=True)
    estado = models.BooleanField(blank=True,default=True)
    empleado = models.ForeignKey('Empleado', on_delete=models.CASCADE)  # Field name made lowercase.
    cliente = models.ForeignKey(Cliente, blank=True, null=True, on_delete=models.CASCADE)  # Field name made lowercase.

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
    imagen = models.ImageField(upload_to='', default="/imagen/default.jpg", blank=True, null=True)#upload_to='%Y/%m/%d',
    url = models.CharField(max_length=100, blank=True, null=True)
    valor = models.FloatField(default=1,blank=True)
    precio = models.FloatField(default=1,blank=True)
    estado = models.BooleanField(blank=True,default=True)

    def __str__(self):
        return str(self.nombre)
    
class Insumo(models.Model):
    nombre = models.CharField(max_length=45)
    codigo = models.CharField(max_length=45, blank=True, null=True)
    estado = models.BooleanField(blank=True,default=True)

    def __str__(self):
        return str(self.nombre)

class Producto_almacens(models.Model):
    cantidad = models.FloatField()
    cantidadinicial = models.FloatField()
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)  # Field name made lowercase.
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE)  # Field name made lowercase.
    lote = models.ForeignKey(Lote, on_delete=models.CASCADE)  # Field name made lowercase.

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

class Recibo(models.Model):
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
    estado  = models.BooleanField(blank=True,default=True)
    pedido  = models.ForeignKey(Pedido, on_delete=models.CASCADE)  # Field name made lowercase.
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
