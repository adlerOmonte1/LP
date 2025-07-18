from django.shortcuts import render
from . import models, serializer
from . serializer import UsuarioSerializer
from rest_framework import viewsets, permissions
from rest_framework.response import Response
#from rest_framework.authtoken.views import ObtainAuthToken
#from rest_framework.authtoken.models import Token
#Nuevo Metodo
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from django.conf import settings

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from django.db import transaction
from .models import Administrador, Carrito,Pago,Pedido,Kardex,DetallePedido


#Seguridad
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = models.Usuario.objects.all()
    serializer_class = serializer.UsuarioSerializer
    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        api_key = request.headers.get('x-api-key')
        if api_key != settings.API_KEY:
            return Response({"error": "API Key Inválida"}, status=403)

        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            
            user_data = serializer.UsuarioSerializer(user).data # obtener los datos del usuario para obtener el rol
            return Response({"token": token.key,"usuario":user_data
                             }) # agregar los datos del usuario para ver el rol
        else:
            return Response({"error": "Credenciales Invalidas"}, status=400)
        
# Registro de usuario
class RegistroView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=201)
        return Response(serializer.errors, status=400)


'''
AUTENTICACION OTRO METODO
class ObtenerToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        })
'''
class HinchaViewSet(viewsets.ModelViewSet):
    queryset = models.Hincha.objects.all()
    serializer_class = serializer.HinchaSerializer

class TipoAdminViewSet(viewsets.ModelViewSet):
    queryset = models.TipoAdministrador.objects.all()
    serializer_class = serializer.TipoAdminSerializer

class AdministradorViewSet(viewsets.ModelViewSet):
    queryset = Administrador.objects.all()
    serializer_class = serializer.AdministradorSerializer
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = models.Categoria.objects.all()
    serializer_class = serializer.CategoriaSerializer

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = models.Proveedor.objects.all()
    serializer_class = serializer.ProveedorSerializer

class AlmacenViewSet(viewsets.ModelViewSet):
    queryset = models.Almacen.objects.all()
    serializer_class = serializer.AlmacenSerializer

class PromocionViewSet(viewsets.ModelViewSet):
    queryset = models.Promocion.objects.all()
    serializer_class = serializer.PromocionSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = models.Producto.objects.all()
    serializer_class = serializer.ProductoSerializer
    permission_classes=[permissions.AllowAny]

class CarritoViewSet(viewsets.ModelViewSet):
    queryset = models.Carrito.objects.all()
    serializer_class = serializer.CarritoSerializer

class CarritoProductoViewSet(viewsets.ModelViewSet):
    queryset = models.Carrito_Producto.objects.all()
    serializer_class = serializer.CarritoProductoSerializer
    def get_queryset(self):
        usuario_id = self.request.query_params.get('usuario')
        if usuario_id:
            return models.Carrito_Producto.objects.filter(carrito__usuario__id=usuario_id)
        return super().get_queryset()

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = models.Pedido.objects.all()
    serializer_class = serializer.PedidoSerializer
    def get_queryset(self):
        usuario_id = self.request.query_params.get('usuario')
        if usuario_id:
            return models.Pedido.objects.filter(usuario_id=usuario_id).order_by('-fecha_pedido')
        return super().get_queryset()
class PasarelaViewSet(viewsets.ModelViewSet):
    queryset = models.Pasarela.objects.all()
    serializer_class = serializer.PasarelaSerializer

class PagoViewSet(viewsets.ModelViewSet):
    queryset = models.Pago.objects.all()
    serializer_class = serializer.PagoSerializer

class NoticiaViewSet(viewsets.ModelViewSet):
    queryset = models.Noticia.objects.all()
    serializer_class = serializer.NoticiaSerializer


class JugadorViewSet(viewsets.ModelViewSet):
    queryset = models.Jugador.objects.all()
    serializer_class = serializer.JugadorSerializer
        

class PartidoViewSet(viewsets.ModelViewSet):
    queryset = models.Partido.objects.all()
    serializer_class = serializer.PartidoSerializer

class HistoriaViewSet(viewsets.ModelViewSet):
    queryset = models.Historia.objects.all()
    serializer_class = serializer.HistoriaSerializer

class PostHistoriaViewSet(viewsets.ModelViewSet):
    queryset = models.Post_Historia.objects.all()
    serializer_class = serializer.PostHistoriaSerializer

class StockViewSet(viewsets.ModelViewSet):
    queryset = models.Stock.objects.all()
    serializer_class = serializer.StockSerializer 
class KardexViewSet(viewsets.ModelViewSet):
    queryset = models.Kardex.objects.all()
    serializer_class = serializer.KardexSerializer
class UnidadMedidaViewSet(viewsets.ModelViewSet):
    queryset = models.UnidadMedida.objects.all()
    serializer_class = serializer.UnidadMedidaSerializer
class DetallePedidoViewSet(viewsets.ModelViewSet):
    queryset = models.DetallePedido.objects.all()
    serializer_class = serializer.DetallePedidoSerializer
    #para el filtro por cada usuario
    def get_queryset(self):
        usuario_id = self.request.query_params.get('usuario')
        if usuario_id:
            return models.DetallePedido.objects.filter(carrito__usuario__id=usuario_id)
        return super().get_queryset()

"""""
class PersonaViewSet(viewsets.ModelViewSet):
    queryset = models.Persona.objects.all()
    serializer_class = serializer.PersonaSerilizer
    permission_classes = [permissions.AllowAny]
"""
#VISTA PERSONALIZADA Consulta
# consulta por producto,almacen y talla
class StockViewSetv2(viewsets.ModelViewSet):
    queryset = models.Stock.objects.all()
    serializer_class = serializer.StockSerializer2 
    @action(detail=False, methods=['get'],url_path='consulta') #Decorador, se usa metodo get, 
    def consultar_stock(self,request):
        producto_id = request.query_params.get('producto_id')# pregunta a la api pasando esos parametros
        almacen_id = request.query_params.get('almacen_id')        
        unidadMedida_id = request.query_params.get('unidadMedida_id')
        stock = models.Stock.objects.get(producto_id=producto_id,almacen_id=almacen_id,unidadMedida_id=unidadMedida_id) #solo quiero objeto que sea igual a los parametros que estoy consultando
        stock_serializer=serializer.StockSerializer2(stock)
        return Response(stock_serializer.data, status=status.HTTP_200_OK)

class ProcesarCompraViewSet(viewsets.ViewSet):
    
    @action(detail=False, methods=['post'], url_path='procesar')
    @transaction.atomic
    def procesar_compra(self, request):
        carrito_id = request.data.get('carrito_id')

        try:
            carrito = Carrito.objects.get(id=carrito_id)
        except Carrito.DoesNotExist:
            return Response({'error': 'Carrito no encontrado'}, status=404)

        # Validar stock
        for item in carrito.carrito_producto_set.all():
            total_stock = sum(
                stock.cantidad for stock in item.producto.stock_set.filter(unidadMedida=item.unidadMedida)
            )
            if item.cantidad > total_stock:
                return Response({
                    'error': f"No hay suficiente stock para el producto {item.producto.nombre}."
                }, status=status.HTTP_400_BAD_REQUEST)

        # Crear el pedido
        pedido = Pedido.objects.create(
            usuario=carrito.usuario,
            carrito=carrito
        )

        # Crear detalle de pedido y actualizar el stock a través de kardex
        for item in carrito.carrito_producto_set.all():
            DetallePedido.objects.create(
                pedido=pedido,
                carrito=carrito,
                producto=item.producto,
                unidadMedida=item.unidadMedida,
                cantidad=item.cantidad
            )

            cantidad_restante = item.cantidad
            stocks = item.producto.stock_set.filter(unidadMedida=item.unidadMedida).order_by('fecha')

            for stock in stocks:
                if cantidad_restante <= 0:
                    break
                salida = min(cantidad_restante, stock.cantidad)
                Kardex.objects.create(
                    producto=item.producto,
                    almacen=stock.almacen,
                    unidadMedida=item.unidadMedida,
                    tipo='salida',
                    cantidad=salida
                )
                cantidad_restante -= salida

        # Limpiar el carrito del usuario
        carrito.carrito_producto_set.all().delete()

        return Response({'mensaje': 'Compra realizada con éxito'}, status=status.HTTP_200_OK)