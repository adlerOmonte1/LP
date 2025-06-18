from django.shortcuts import render
from . import models, serializer
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


#Seguridad
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = models.Usuario.objects.all()
    serializer_class = serializer.UsuarioSerializer

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
            return Response({"token": token.key})
        else:
            return Response({"error": "Credenciales Invalidas"}, status=400)

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
    queryset = models.Administrador.objects.all()
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

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = models.Pedido.objects.all()
    serializer_class = serializer.PedidoSerializer

class PasarelaViewSet(viewsets.ModelViewSet):
    queryset = models.Pasarela.objects.all()
    serializer_class = serializer.PasarelaSerializer

class PagoViewSet(viewsets.ModelViewSet):
    queryset = models.Pago.objects.all()
    serializer_class = serializer.PagoSerializer

class NoticiaViewSet(viewsets.ModelViewSet):
    queryset = models.Noticia.objects.all()
    serializer_class = serializer.NoticiaSerializer

class ComentarioViewSet(viewsets.ModelViewSet):
    queryset = models.Comentario.objects.all()
    serializer_class = serializer.ComentarioSerializer

class ReseñaViewSet(viewsets.ModelViewSet):
    queryset = models.Reseña.objects.all()
    serializer_class = serializer.ReseñaSerializer

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
