from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from datetime import datetime #para mi funcion de promocion
from django.utils import timezone #obtener la fecha actual valida sin generar conflictos con la zona horaria
from django.db import transaction
# Create your models here.
Estado =[
        ('Activo','Activo'),('Inhabilitado','Inhabilitado')
]
#---------------USUARIO
class Usuario(AbstractUser):
    rol = [
        ('administrador','Administrador'),
        ('hincha','Hincha'),
    ]
    #Ya tiene por el Modelo Abstrac User
    telefono=models.CharField(max_length=9,null=True,blank=True)
    dni=models.CharField(max_length=8,null=True,blank=True)
    fechaNac=models.DateField(null=True,blank=True)
    rol = models.CharField(max_length=30, choices=rol, default='hincha') # rol del usuario, hincha o administrador
     #pass cuando no se necesita agregar mas campos
    def __str__(self):
        return self.username    

#---------------HINCHA        
class Hincha(models.Model):
    Usuario = models.ForeignKey(Usuario,on_delete=models.CASCADE)
    alias = models.CharField(max_length=40) 
    def __str__(self):
        return self.alias
    

#---------------TIPO DE ADMINISTRADOR    
class TipoAdministrador(models.Model):
    id=models.AutoField(primary_key=True)
    tipo=models.CharField(max_length=40)
    def __str__(self):
        return self.tipo
    

 #---------------ADMINISTRADOR       
class Administrador(models.Model):
    id = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    tipo_admin=models.ForeignKey(TipoAdministrador,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id.username}: {self.tipo_admin.tipo}"
    

#---------------CATEGORIAS   
class Categoria(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre
    

#---------------PROVEEDORES       
class Proveedor(models.Model):
    id = models.AutoField(primary_key=True)
    nombreProveedor = models.CharField(max_length=100)
    razonSocial = models.CharField(max_length=100)
    ruc = models.CharField(max_length=20)
    nombreContacto = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=9)
    estado = models.CharField(max_length=40,choices=Estado,default='Activo')
    #estado = models.CharField(max_length=50)

    def __str__(self):
        return self.nombreProveedor
    

#---------------ALMACENES       
class Almacen(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    tipo_almacen = models.CharField(max_length=50)
    descripcion = models.TextField()
    direccion = models.CharField(max_length=150)
    estado = models.CharField(max_length=40,choices=Estado,default='Activo')
    def __str__(self):
        return self.nombre
    

#---------------PROMOCIONES       
class Promocion(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30)
    descripcion = models.TextField()
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    #estado = models.CharField(max_length=40,choices=Estado,default='Inhabilitado')
    descuento = models.DecimalField(max_digits=5, decimal_places=2)
    @property # propidad para que el estado de mi promocion se actualice automaticamente
    def estado(self):
        hoy = timezone.now()  # obtener la fecha actual
        if self.fecha_inicio <= hoy <= self.fecha_fin:
            return 'Activo'
            #self.estado = 'Activo'
        return 'Inhabilitado'
            #self.estado = 'Inahibilitado'  

    def __str__(self):
        return self.nombre
    

#---------------PRODCUTOS        
class Producto(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen_url = models.ImageField(upload_to='imagenes_productos/',null=True,blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE) # relacion con categoria 1:M
    almacen = models.ManyToManyField(Almacen, through='Stock')  # M:M relacion con almacen
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)  # relacion con proveedor 1:M
    promocion = models.ForeignKey(Promocion, on_delete=models.SET_NULL,null=True,blank=True)  # relacion con promocion 1:M
    # Funcion de descuento
    @property
    def precio_final(self):
        if self.promocion and self.promocion.estado == 'Activo': # condicional para ver el estado de mi promocion
            hoy = timezone.now()  # obtener la fecha actual
            #hoy = datetime.date.today() # obtener la fecha como un objeto
            if self.promocion.fecha_inicio <= hoy <= self.promocion.fecha_fin: # verifica si la fecha actual esta dentro del rango de la promocion
                precioTotal = round(self.precio * (1 - self.promocion.descuento / 100),2)
                return precioTotal
        return self.precio
    def __str__(self):
        return self.nombre
    

# UNIDAD DE MEDIDA, para definir tallas
class UnidadMedida(models.Model):
    id = models.AutoField(primary_key=True)
    unidad = models.CharField(max_length=30)
    def __str__(self):
        return self.unidad
    

#------STOCK de la relacion de M-M ALMACEN-PRODUCTO    
# control de concurrencia
class Stock(models.Model):
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE) 
    unidadMedida = models.ForeignKey(UnidadMedida,on_delete=models.CASCADE)
    cantidad = models.BigIntegerField(default=0)  # cantidad de stock
    fecha = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together=[['almacen','producto','unidadMedida']] # no permite iguales



#_--------------KARDEX
class Kardex(models.Model):
    id = models.AutoField(primary_key=True)
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    unidadMedida = models.ForeignKey(UnidadMedida,on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=[('entrada', 'Entrada'), ('salida', 'Salida')])
    fecha = models.DateTimeField(auto_now_add=True)
    cantidad = models.IntegerField() # entrada o salida
    # CONTROL DE CONCURRENCIA
    #Metodo para actualizar el stock por el kardex

    def save(self, *args,**kwargs):
        super().save(*args,**kwargs)
        stock_obj, creado = Stock.objects.get_or_create(producto=self.producto,almacen = self.almacen,unidadMedida=self.unidadMedida)
        #super().save(*args, **kwargs) 
        # condicional para la entrada y salida del stock
        if self.tipo == 'entrada':
            stock_obj.cantidad += self.cantidad
        elif self.tipo == 'salida':
            if stock_obj.cantidad < self.cantidad:
                raise ValueError("No hay suficiente stock para realizar la salida.")
            stock_obj.cantidad -= self.cantidad
        stock_obj.save()


#---------------CARRITOS        
class Carrito(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    #producto = models.ManyToManyField(Producto, through='Carrito_Producto')
    fecha_creacion = models.DateField(auto_now=True)
    #monto_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    #estado = models.CharField(choices=Estado, default='Activo')
    @property
    def total(self):
        return sum(cp.producto.precio_final * cp.cantidad for cp in self.carrito_producto_set.all())
    def __str__(self):
        return f"Carrito #{self.id} de {self.usuario.username}"
    

#---------------CARRITO-PRODUCTO        
# relacion de muchos a muchos pero contiene datos adicionales, se usa through
class Carrito_Producto(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    unidadMedida = models.ForeignKey(UnidadMedida,on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    imagen_url = models.ImageField(upload_to='imagenes_productos/',null=True,blank=True)
    class Meta:
        unique_together=[['carrito','producto','unidadMedida']]

    def __str__(self):
        return f"Carrito ID: {self.carrito}"
    

#---------------PEDIDOS   
# aca se guardan todos los datos de una compra, una vez pagado desde el carrito
class Pedido(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fecha_pedido = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Pedido #{self.id}"
    


class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    unidadMedida = models.ForeignKey(UnidadMedida, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    class Meta:
        unique_together=[['carrito','producto','unidadMedida']]


class Pasarela(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    url_api = models.CharField(max_length=200)
    tipo = models.CharField(max_length=50)
    estado = models.CharField(max_length=40,choices=Estado,default='Activo')
    
    def __str__(self):
        return self.nombre
    
class Pago(models.Model):
    id = models.AutoField(primary_key=True)
    fecha_pago = models.DateTimeField(auto_now=True)
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    #pasarela = models.ForeignKey(Pasarela, on_delete=models.CASCADE)
    def __str__(self):
        return f"Pago ID#{self.id}"



class Noticia(models.Model):
    id = models.AutoField(primary_key=True)
    nombreHistoria = models.CharField(max_length=100)  
    descripcion = models.TextField()                  
    imagen = models.ImageField(upload_to='noticias/', null=True, blank=True)  
    fecha_publicacion = models.DateField(auto_now_add=True)
    administrador = models.ForeignKey('Administrador', on_delete=models.CASCADE)

    def __str__(self):
        return self.nombreHistoria
    

    
class Jugador(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    edad = models.IntegerField()
    posicion = models.CharField(max_length=50)
    dorsal = models.IntegerField()
    peso = models.FloatField()
    altura = models.FloatField()
    nacionalidad = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='jugadores/', blank=True, null=True)
    administrador = models.ForeignKey(Administrador, on_delete=models.CASCADE)
 


class Partido(models.Model):
    id = models.AutoField(primary_key=True)
    administrador = models.ForeignKey(Administrador, on_delete=models.CASCADE,blank=True, null=True)  
    nombre_partido = models.CharField(max_length=100) 
    lugar_partido = models.CharField(max_length=50)     
    fecha_partido = models.DateField()
    hora_partido = models.TimeField()
    resultado = models.CharField(max_length=50, null=True,blank=True)

    def __str__(self):
        return self.nombre_partido
    



class Historia(models.Model):
    id = models.AutoField(primary_key=True)
    nombreHistoria = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='historias/', null=True, blank=True)
    administrador = models.ForeignKey('Administrador', on_delete=models.CASCADE)

    def __str__(self):
        return self.nombreHistoria
    

    
class Post_Historia(models.Model):
    id = models.AutoField(primary_key=True)
    historia = models.ForeignKey(Historia, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    contexto = models.TextField()
    imagen = models.ImageField(upload_to='imagenes_posthistoria/', null=True, blank=True) 
    fecha_publicacion = models.DateField(auto_now_add=True)  

    def __str__(self):
        return self.titulo

