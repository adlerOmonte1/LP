from django.http import JsonResponse
from django.conf import settings
# validar mi clave API key
class APIKeyMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response


    def __call__(self,request):
        #print("Ruta:", request.path)
        # rutas permitidas sin necesidad de API Key
        rutas_permitidas = [ '/api/registro/']
        if request.path in rutas_permitidas:
            return self.get_response(request)
        
        # permitir también las rutas que comienzan con /media/ o /static/
        if request.path.startswith('/media/') or request.path.startswith('/static/'):
            return self.get_response(request)
        
        api_key = request.headers.get('x-api-key') 

        if api_key and api_key == settings.API_KEY:
            return self.get_response(request)
        
        return JsonResponse({"error" : "API Key Inválida"},status=403)