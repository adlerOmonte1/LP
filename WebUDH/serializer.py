from rest_framework import serializers
from . models import *
from . import models
from . models import Administrador, Jugador


#Seguridad 
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = "__all__"

    def create(self, validated_data):
        user = Usuario(
            email = validated_data['email'],
            username = validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
class HinchaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hincha
        fields = ['usuario','alias']
class TipoAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoAdministrador
        fields = ['id', 'tipo']

        
class AdministradorSerializer(serializers.ModelSerializer):  
    username = serializers.CharField(source='id.username', read_only=True)
    tipo_nombre = serializers.CharField(source='tipo_admin.tipo', read_only=True)

    class Meta:
        model = Administrador
        fields = ['id', 'tipo_admin', 'username', 'tipo_nombre']
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = "__all__"
class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = "__all__"
class AlmacenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Almacen
        fields = "__all__"
class PromocionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promocion
        fields = ['id', 'nombre', 'descripcion', 'fecha_inicio', 'fecha_fin', 'descuento', 'estado']
        def get_estado(self, obj):
            return obj.estado
class ProductoSerializer(serializers.ModelSerializer):
    nombre_categoria = serializers.ReadOnlyField(source='categoria.nombre')
    nombre_proveedor = serializers.ReadOnlyField(source='proveedor.nombreProveedor')
    nombre_almacen = serializers.ReadOnlyField(source='almacen.nombre')
    nombre_promocion = serializers.ReadOnlyField(source='promocion.nombre')
    class Meta:
        model = Producto
        #fields = '__all__'
        fields = ['id', 'nombre', 'descripcion', 'precio', 'imagen_url',
                  'categoria', 'proveedor', 'almacen', 'promocion',
                  'nombre_categoria', 'nombre_proveedor', 'nombre_almacen',
                  'nombre_promocion', 'precio_final']
    def get_precio_final(self,obj):
            return obj.precio_final
class CarritoSerializer(serializers.ModelSerializer):
    #producto = ProductoSerializer()
    class Meta:
        model = Carrito
        fields = ['id', 'usuario', 'fecha_creacion', 'producto', 'total']
        def get_total(self, obj):
            return obj.total
class CarritoProductoSerializer(serializers.ModelSerializer):
    producto_imagen = serializers.ImageField(source='producto.imagen_url', read_only=True)
    producto_precio = serializers.ReadOnlyField(source='producto.precio')
    producto_nombre = serializers.ReadOnlyField(source='producto.nombre')
    class Meta:
        model = Carrito_Producto
        fields = "__all__"
class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = "__all__"
class PasarelaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pasarela
        fields = "__all__"
class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = "__all__"
class NoticiaSerializer(serializers.ModelSerializer):
    admin_nombre = serializers.ReadOnlyField(source='administrador.') # nombre campo con el otro campo de que yo quiero
    class Meta:
        model = Noticia
        fields = "__all__"
class ComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields = "__all__"
class ReseñaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reseña
        fields = "__all__"
class JugadorSerializer(serializers.ModelSerializer): 
    tipo_param = serializers.CharField(source='administrador.id', read_only=True)
    class Meta:
        model = Jugador
        fields = [
            'id', 'nombre', 'apellido', 'edad', 'posicion',
            'dorsal', 'peso', 'altura', 'nacionalidad',
            'imagen', 'administrador','tipo_param'
        ]
class PartidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partido
        fields = "__all__"
class HistoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historia
        fields = "__all__"
class PostHistoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post_Historia
        fields = "__all__"
class StockSerializer(serializers.ModelSerializer):
    nombre_producto = serializers.ReadOnlyField(source='producto.nombre')
    nombre_almacen = serializers.ReadOnlyField(source='almacen.nombre')
    nombre_talla = serializers.ReadOnlyField(source = 'unidadMedida.unidad')
    #producto = ProductoSerializer()
    #almacen = AlmacenSerializer()
    class Meta:
        model = models.Stock
        fields = "__all__"
class KardexSerializer(serializers.ModelSerializer):
    nombre_producto = serializers.ReadOnlyField(source='producto.nombre')
    nombre_almacen = serializers.ReadOnlyField(source='almacen.nombre')
    nombre_talla = serializers.ReadOnlyField(source = 'unidadMedida.unidad')
    class Meta:
        model = Kardex
        fields = "__all__"
class UnidadMedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadMedida
        fields = "__all__"
class DetallePedidoSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer()
    class Meta:
        model = DetallePedido
        fields = "__all__"

class StockSerializer2(serializers.ModelSerializer):
    producto = ProductoSerializer()
    almacen = AlmacenSerializer()
    unidadMedida = UnidadMedidaSerializer
    class Meta:
        model = models.Stock
        fields = "__all__"

""""
class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields= "__all__"

class UnidadMedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadMedida
        fields= "__all__"

class StockSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer()
    almacen = AlmacenSerializer()
    class Meta:
        model = models.Stock
        fields = ['producto','almacen','cantidad']
"""