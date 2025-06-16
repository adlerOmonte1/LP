from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from WebUDH import views

router = routers.DefaultRouter()
router.register('usuarios', views.UsuarioViewSet)
router.register('administradores', views.AdministradorViewSet)
router.register('categorias', views.CategoriaViewSet)
router.register('proveedores', views.ProveedorViewSet)
router.register('almacenes', views.AlmacenViewSet)
router.register('promociones', views.PromocionViewSet)
router.register('productos', views.ProductoViewSet)
router.register('carritos', views.CarritoViewSet)
router.register('carritoProductos', views.CarritoProductoViewSet)
router.register('pedidos', views.PedidoViewSet)
router.register('pasarelas', views.PasarelaViewSet)
router.register('pagos', views.PagoViewSet)
router.register('noticias', views.NoticiaViewSet)
router.register('comentarios', views.ComentarioViewSet)
router.register('reseñas', views.ReseñaViewSet)
router.register('jugadores', views.JugadorViewSet)
router.register('partidos', views.PartidoViewSet)
router.register('historias', views.HistoriaViewSet)
router.register('post-historias', views.PostHistoriaViewSet)
#router.register('hinchas',views.HinchaViewSet)
router.register('tiposadmin',views.TipoAdminViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
