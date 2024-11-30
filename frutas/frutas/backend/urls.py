from django.http import JsonResponse
from django.urls import path, include
from django.contrib import admin

# Configuración de rutas principales
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('tienda.urls')),
]

# Manejador global para rutas no configuradas
def custom_404_view(request, exception=None):
    return JsonResponse({'error': 'Esta ruta no está configurada.'}, status=404)

# Asignar el manejador de error 404
handler404 = custom_404_view

