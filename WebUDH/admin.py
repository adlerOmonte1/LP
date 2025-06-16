from django.contrib import admin
from . models import *
# Register your models here.
admin.site.register(Usuario)
#admin.site.register(Hincha)
admin.site.register(TipoAdministrador)
admin.site.register(Administrador)
admin.site.register(Categoria)
admin.site.register(Proveedor)
admin.site.register(Almacen)
admin.site.register(Promocion)
admin.site.register(Producto)
#admin.site.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ('id_carrito', 'usuario', 'fecha_creacion','total')
    def total(self, obj):
        return obj.total
    total.short_description = 'Total calculado'

admin.site.register(Carrito, CarritoAdmin)
admin.site.register(Carrito_Producto)
admin.site.register(Pedido)
admin.site.register(Pasarela)
admin.site.register(Pago)
admin.site.register(Noticia)
admin.site.register(Comentario)
admin.site.register(Reseña)
admin.site.register(Jugador)
admin.site.register(Partido)
admin.site.register(Historia)
admin.site.register(Post_Historia)