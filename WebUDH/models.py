from django.db import models

# Create your models here.
Estado =[
        ('Activo','Activo'),('Inhabilitado','Inhabilitado')
]
#---------------USUARIO
class Usuario(models.Model):
    id_usuario=models.AutoField(primary_key=True)
    nombreCompleto=models.CharField(max_length=70)
    email=models.EmailField()
    telefono=models.CharField(max_length=9)
    password=models.CharField(max_length=30)
    dni=models.CharField(max_length=8)
    fechaNac=models.DateField()
    
    def __str__(self):
        return self.nombreCompleto
#---------------HINCHA        
#class Hincha(Usuario):
#    alias = models.CharField(max_length=40)
#    def __str__(self):
#        return self.alias
#---------------TIPO DE ADMINISTRADOR    
class TipoAdministrador(models.Model):
    id=models.AutoField(primary_key=True)
    tipo=models.CharField(max_length=40)
    def __str__(self):
        return self.tipo
 #---------------ADMINISTRADOR       
class Administrador(models.Model):
    id_administrador = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    tipo_admin=models.ForeignKey(TipoAdministrador,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id_administrador.nombreCompleto}: {self.tipo_admin.tipo}"
#---------------CATEGORIAS   
class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre
#---------------PROVEEDORES       
class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
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
    id_almacen = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    tipo_almacen = models.CharField(max_length=50)
    descripcion = models.TextField()
    direccion = models.CharField(max_length=150)
    estado = models.CharField(max_length=40,choices=Estado,default='Activo')
    def __str__(self):
        return self.nombre
#---------------PROMOCIONES       
class Promocion(models.Model):
    id_promocion = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30)
    descuento = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.nombre
#---------------PRODCUTOS        
class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    talla = models.CharField(max_length=40,null=True)
    stock = models.IntegerField()
    imagen_url = models.CharField(max_length=200)
    usuario = models.ManyToManyField(Usuario, through='Reseña')
    id_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE) # relacion con categoria 1:M
    id_almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE)  # relacion con almacen 1:M
    id_proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)  # relacion con proveedor 1:M
    id_promocion = models.ForeignKey(Promocion, on_delete=models.SET_NULL,null=True,blank=True)  # relacion con promocion 1:M
    def __str__(self):
        return self.nombre
#---------------CARRITOS        
class Carrito(models.Model):

    id_carrito = models.AutoField(primary_key=True)
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    producto = models.ManyToManyField(Producto, through='Carrito_Producto')
    fecha_creacion = models.DateField(auto_now=True)
    #monto_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    #estado = models.CharField(choices=Estado, default='Activo')
    @property
    def total(self):
        return sum(cp.producto.precio * cp.cantidad for cp in self.carrito_producto_set.all())
    #def __str__(self):
    #    return f"Carrito #{self.id_carrito} de {self.usuario.nombreCompleto}"
#---------------CARRITOPRODUCTO        
# relacion de muchos a muchos pero contiene datos adicionales, se usa through
class Carrito_Producto(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    class Meta:
        unique_together=[['carrito','producto']]

    def __str__(self):
        return f"Carrito ID: {self.carrito.id_carrito}"
#---------------PEDIDOS   
class Pedido(models.Model):
    EstadoPedido =[
        ('Activo','Activo'),('En proceso','En proceso'),('Finalizado','Finalizado')
    ]
    id_pedido = models.AutoField(primary_key=True)
    carrito = models.OneToOneField(Carrito,on_delete=models.CASCADE)
    fecha_pedido = models.DateField(auto_now=True)
    estado = models.CharField(max_length=40,choices=EstadoPedido, default='Activo')
    
    def __str__(self):
        return f"Pedido #{self.id_pedido}"

class Pasarela(models.Model):
    id_pasarela = models.AutoField(primary_key=True)
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
    id_pago = models.AutoField(primary_key=True)
    fecha_pago = models.DateField(auto_now=True)
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE)
    pasarela = models.ForeignKey(Pasarela, on_delete=models.CASCADE)
    #estado = models.CharField(choices=Estado, default='Validado')
    #monto = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f"Pago ID#{self.id_pago}"
    
class Noticia(models.Model):
    id_noticia = models.AutoField(primary_key=True)
    administrador = models.ForeignKey(Administrador, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    contenido = models.TextField()
    fecha_publicacion = models.DateField()
    imagen_url = models.CharField(max_length=200)

    def __str__(self):
        return self.titulo
    
class Comentario(models.Model):
    id_comentario = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    noticia = models.ForeignKey(Noticia, on_delete=models.CASCADE)
    descripcion = models.TextField()
    fechaComentario = models.DateField(auto_now=True)

    def __str__(self):
        return f"Comentario ID#{self.id_comentario} de {self.usuario.nombreCompleto}"

class Reseña(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_publicacion = models.DateField(auto_now=True)
    valoracion = models.CharField(max_length=10)
    class Meta:
        unique_together=[['usuario','producto']]

    def __str__(self):
        return f"Reseña #{self.producto.id_producto} de {self.usuario.nombreCompleto}"
    
class Jugador(models.Model):
    id_jugador = models.AutoField(primary_key=True)
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
    id_partido = models.AutoField(primary_key=True)
    administrador = models.ForeignKey(Administrador, on_delete=models.CASCADE)  
    nombre_partido = models.CharField(max_length=100) 
    lugar_partido = models.CharField(max_length=50)     
    fecha_partido = models.DateField()
    hora_partido = models.TimeField()
    resultado = models.CharField(max_length=50, null=True,blank=True)

    def __str__(self):
        return self.nombre_partido

class Historia(models.Model):
    id_historia = models.AutoField(primary_key=True)
    nombreHistoria = models.CharField(max_length=100)
    descripcion = models.TextField()
    administrador = models.ForeignKey(Administrador, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombreHistoria
    
class Post_Historia(models.Model):
    id_postHistoria = models.AutoField(primary_key=True)
    historia = models.ForeignKey(Historia, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    contexto = models.TextField()
    url = models.CharField(max_length=200)
    fecha_publicacion = models.DateField()

    def __str__(self):
        return self.titulo