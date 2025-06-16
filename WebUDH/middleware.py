from django.http import JsonResponse
from django.conf import settings
# validar mi clave API key
class APIKeyMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self,request):
        api_key = request.headers.get('x-api-key') 

        if api_key and api_key == settings.API_KEY:
            return self.get_response(request)
        
        return JsonResponse({"error" : "API Key Inválida"},status=403)