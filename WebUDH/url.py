from rest_framework import routers
from . import views
from django.urls import path,include

router = routers.DefaultRouter()

router.register('miusuarios',views.MiUsuarioViewset)

urlpatterns = [
    path('',include(router.urls)),
    #Anterior login
    #path('login/', views.ObtenerToken.as_view(),name='token-auth'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('registro/', views.RegistroView.as_view(), name='registro'),

]