from django.utils import translation
from django.conf import settings

class ForceSpanishMiddleware:
    """
    Middleware para forzar el idioma español en toda la aplicación
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Forzar el idioma español
        translation.activate('es')
        request.LANGUAGE_CODE = 'es'
        
        response = self.get_response(request)
        
        # Asegurar que el idioma se mantiene
        response['Content-Language'] = 'es'
        
        return response
