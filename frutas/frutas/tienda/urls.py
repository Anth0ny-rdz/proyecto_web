from django.urls import path, include
from .views import (
    ProductosInseguros, ProductoRegistrarView,
    ProductoRetrieveUpdateDestroyView,
    UsuarioCreateView,
    AlergiaListCreateView, ProductoListView,
    LoginAPIView,RefreshTokenAPIView               
    )
from rest_framework_simplejwt.views import TokenObtainPairView
from . import views
urlpatterns = [
    # Otras rutas aquí
    path('productos-inseguros/<int:user_id>/', ProductosInseguros.as_view(), name='productos-inseguros'),
    path('api/auth/', include('rest_framework.urls')),  # Para login
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Obtener token JWT
    path('productos/', ProductoRegistrarView.as_view(), name='productos_list_create'),
    path('productos/<int:pk>/', ProductoRetrieveUpdateDestroyView.as_view(), name='productos_detail'),
    path('usuario/registro/', UsuarioCreateView.as_view(), name='registro_usuario'),
    path('alergias/', AlergiaListCreateView.as_view(), name='alergias_list_create'),
    path('api/productos/', ProductoListView.as_view(), name='producto-list'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('api/token/refresh/', RefreshTokenAPIView.as_view(), name='token_refresh'),
    path('carrito/', views.carrito_view, name='carrito'),
    path('pedido/', views.crear_pedido, name='crear_pedido'),
]

