from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from datetime import datetime #para mi funcion de promocion
from django.utils import timezone #obtener la fecha actual valida sin generar conflictos con la zona horaria
# Create your models here.
Estado =[
        ('Activo','Activo'),('Inhabilitado','Inhabilitado')
]
#---------------USUARIO
class Usuario(AbstractUser):
    #Ya tiene por el Modelo Abstrac User
    #id=models.AutoField(primary_key=True)
    #nombreCompleto=models.CharField(max_length=70)
    #email=models.EmailField()
    #password=models.CharField(max_length=30)
    telefono=models.CharField(max_length=9,null=True,blank=True)
    dni=models.CharField(max_length=8,null=True,blank=True)
    fechaNac=models.DateField(null=True,blank=True)
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
    talla = models.CharField(max_length=40,null=True)
    stock = models.IntegerField()
    imagen_url = models.CharField(max_length=200)
    usuario = models.ManyToManyField(Usuario, through='Reseña') # se agrega para tener mas atributos
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE) # relacion con categoria 1:M
    almacen = models.ManyToManyField(Almacen, through='Kardex')  # M:M relacion con almacen
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
#_--------------KARDEX
class Kardex(models.Model):
    id = models.AutoField(primary_key=True)
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    cantidad = models.IntegerField()
    stock_actual = models.IntegerField()

#---------------CARRITOS        
class Carrito(models.Model):

    id = models.AutoField(primary_key=True)
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    producto = models.ManyToManyField(Producto, through='Carrito_Producto')
    fecha_creacion = models.DateField(auto_now=True)

    #monto_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    #estado = models.CharField(choices=Estado, default='Activo')
    @property
    def total(self):
        return sum(cp.producto.precio * cp.cantidad for cp in self.carrito_producto_set.all())
    def __str__(self):
        return f"Carrito #{self.id} de {self.usuario.username}"
#---------------CARRITOPRODUCTO        
# relacion de muchos a muchos pero contiene datos adicionales, se usa through
class Carrito_Producto(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    class Meta:
        unique_together=[['carrito','producto']]

    def __str__(self):
        return f"Carrito ID: {self.carrito}"
#---------------PEDIDOS   
class Pedido(models.Model):
    EstadoPedido =[
        ('Activo','Activo'),('En proceso','En proceso'),('Finalizado','Finalizado')
    ]
    id = models.AutoField(primary_key=True)
    carrito = models.OneToOneField(Carrito,on_delete=models.CASCADE)
    fecha_pedido = models.DateField(auto_now=True)
    estado = models.CharField(max_length=40,choices=EstadoPedido, default='Activo')
    
    def __str__(self):
        return f"Pedido #{self.id}"

class Pasarela(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    url_api = models.CharField(max_length=200)
    tipo = models.CharField(max_length=50)
    estado = models.CharField(max_length=40,choices=Estado,default='Activo')
    
    def __str__(self):
        return self.nombre

class Pago(models.Model):
   # EstadoPago =[
    #    ('Validado'),('En Proceso')
     #]
    id = models.AutoField(primary_key=True)
    fecha_pago = models.DateField(auto_now=True)
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE)
    pasarela = models.ForeignKey(Pasarela, on_delete=models.CASCADE)
    #estado = models.CharField(choices=Estado, default='Validado')
    #monto = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f"Pago ID#{self.id}"
    
class Noticia(models.Model):
    id = models.AutoField(primary_key=True)
    administrador = models.ForeignKey(Administrador, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    contenido = models.TextField()
    fecha_publicacion = models.DateField()
    imagen_url = models.CharField(max_length=200)

    def __str__(self):
        return self.titulo
    
class Comentario(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    noticia = models.ForeignKey(Noticia, on_delete=models.CASCADE)
    descripcion = models.TextField()
    fechaComentario = models.DateField(auto_now=True)

    def __str__(self):
        return f"Comentario ID#{self.id} de {self.usuario.username}"

class Reseña(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_publicacion = models.DateField(auto_now=True)
    valoracion = models.CharField(max_length=10)
    class Meta:
        unique_together=[['usuario','producto']]

    def __str__(self):
        return f"Reseña #{self.producto.id} de {self.usuario.username}"
    
class Jugador(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    edad = models.IntegerField()
    posicion = models.CharField(max_length=50)
    dorsal = models.IntegerField()
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    altura = models.DecimalField(max_digits=5, decimal_places=2)
    nacionalidad = models.CharField(max_length=25)
    administrador = models.ForeignKey(Administrador, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
    
class Partido(models.Model):
    id = models.AutoField(primary_key=True)
    administrador = models.ForeignKey(Administrador, on_delete=models.CASCADE)  
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
    administrador = models.ForeignKey(Administrador, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombreHistoria
    
class Post_Historia(models.Model):
    id = models.AutoField(primary_key=True)
    historia = models.ForeignKey(Historia, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    contexto = models.TextField()
    url = models.CharField(max_length=200)
    fecha_publicacion = models.DateField()

    def __str__(self):
        return self.titulo
    
"""""
CODIGO POR CONFIRMAR DE PARTE LA AUTENTICACION
    #Prueba Unitaria de Seguridad
class UsuarioManager(BaseUserManager):
    def create_user(self,username,email,password=None,**extra_fields):
        #Creamos un usario en base a nombre de usuario, contraseña y correo
        if not email: #verifica que se proporcione correo
            raise ValueError('Correo es obligatorio')
        email = self.normalize_email(email) #convierte en minusculas 
        user = self.model(username=username,email=email,**extra_fields)
        user.set_password(password) #encripta la contraseña
        user.save(using=self._db)
        return user
    
    def create_superuser(self,username,email,password=None,**extra_fields):
        #Creamos un superusario en base a nombre de usuario, contraseña y correo
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El campo staff debe ser True')
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El campo superusuario debe ser True')
        
        return self.create_user(username,email,password,**extra_fields)
    


     #distinguir con mi otra tabla usuario
    #objects = UsuarioManager()

    #def __str__(self):
    #    return self.username
"""