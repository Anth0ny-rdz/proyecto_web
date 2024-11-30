from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Usuario, Alergia, Carrito, Producto, CarritoItem, Pedido, Envio
from .serializers import ProductoSerializer, UsuarioSerializer, AlergiaSerializer, PedidoSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics
from django.http import JsonResponse
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view,permission_classes
from django.http import JsonResponse

class ProductosInseguros(APIView):
    def get(self, request, user_id):
        try:
            usuario = Usuario.objects.get(id=user_id)
            productos_alergicos = Producto.objects.filter(alergias__in=usuario.alergias.all()).distinct()
            return JsonResponse({
                'user_id': user_id,
                'productos_inseguros': list(productos_alergicos.values('id', 'nombre'))
            })
        except Usuario.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
        
# CRUD para Productos
class ProductoRegistrarView(APIView):
    def post(self, request):
        # Usar el serializador para validar y guardar el nuevo producto
        serializer = ProductoSerializer(data=request.data)
        if serializer.is_valid():
            # Guardamos el producto y devolvemos una respuesta de éxito
            serializer.save()
            return Response({
                'message': 'Producto registrado con éxito.',
                'producto': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [AllowAny]

class UsuarioCreateView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        username = self.request.data.get('username')
        email = self.request.data.get('email')

        # Verificar si el nombre de usuario ya existe
        if Usuario.objects.filter(username=username).exists():
            raise ValidationError({"username": "Este nombre de usuario ya está en uso."})

        # Verificar si el email ya existe
        if Usuario.objects.filter(email=email).exists():
            raise ValidationError({"email": "Este correo electrónico ya está registrado."})

        serializer.save()

# Listar Alergias
class AlergiaListCreateView(generics.ListCreateAPIView):
    queryset = Alergia.objects.all()
    serializer_class = AlergiaSerializer
    permission_classes = [AllowAny]

class ProductoListView(APIView):
    permission_classes = [AllowAny]  # Permitir acceso a todos los usuarios

    def get(self, request):
        productos = Producto.objects.all()
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data)

class UsuarioRegistroAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Usuario registrado con éxito."}, status=201)
        return Response(serializer.errors, status=400)

class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error": "Usuario y contraseña son requeridos."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Credenciales inválidas."}, status=status.HTTP_401_UNAUTHORIZED)
        
class RefreshTokenAPIView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Verifica si el refresh token es válido
            refresh = RefreshToken(refresh_token)
            access_token = refresh.access_token
            return Response({"access_token": str(access_token)}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET', 'POST', 'DELETE'])
def carrito_view(request):
    usuario = request.user
    try:
        carrito, created = Carrito.objects.get_or_create(usuario=usuario)
    except Carrito.DoesNotExist:
        return Response({"detail": "Carrito no encontrado."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # Obtener los productos del carrito
        carrito_items = CarritoItem.objects.filter(carrito=carrito)
        items = []
        for item in carrito_items:
            items.append({
                "producto_id": item.producto.id,
                "nombre": item.producto.nombre,
                "cantidad": item.cantidad,
                "precio": item.producto.precio,
            })

        # Obtener valores calculados
        total = carrito.total()
        impuestos = carrito.impuestos()
        envio = carrito.envio()
        total_final = carrito.total_final()

        # Devolver los datos, incluidos los valores calculados
        return Response({
            "items": items,
            "total": str(total),  # Convertir a string para evitar problemas de precisión con Decimals en JSON
            "impuestos": str(impuestos),
            "envio": str(envio),
            "total_final": str(total_final),
        }, status=status.HTTP_200_OK)

    if request.method == 'POST':
        # Agregar un producto al carrito
        producto_id = request.data.get('producto_id')
        cantidad = request.data.get('cantidad', 1)

        try:
            producto = Producto.objects.get(id=producto_id)
        except Producto.DoesNotExist:
            return Response({"detail": "Producto no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        # Verificar si el producto ya está en el carrito
        carrito_item, created = CarritoItem.objects.get_or_create(
            carrito=carrito, producto=producto,
            defaults={'cantidad': cantidad}
        )

        if not created:
            # Si ya existe, actualizamos la cantidad
            carrito_item.cantidad += cantidad
            carrito_item.save()

        return Response({"message": "Producto agregado al carrito."}, status=status.HTTP_201_CREATED)

    if request.method == 'DELETE':
        # Eliminar un producto del carrito
        producto_id = request.data.get('producto_id')

        try:
            producto = Producto.objects.get(id=producto_id)
        except Producto.DoesNotExist:
            return Response({"detail": "Producto no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        # Buscar el producto en el carrito
        try:
            carrito_item = CarritoItem.objects.get(carrito=carrito, producto=producto)
            carrito_item.delete()
            return Response({"message": "Producto eliminado del carrito."}, status=status.HTTP_204_NO_CONTENT)
        except CarritoItem.DoesNotExist:
            return Response({"detail": "Producto no está en el carrito."}, status=status.HTTP_404_NOT_FOUND)
        
@api_view(['POST'])
def crear_pedido(request):
    usuario = request.user
    print(f"Usuario autenticado: {usuario}")

    carrito = Carrito.objects.filter(usuario=usuario).first()
    if not carrito:
        print("No hay carrito asociado para este usuario.")
        return Response({"detail": "No hay carrito para este usuario."}, status=status.HTTP_400_BAD_REQUEST)

    total_pedido = carrito.total_final()
    metodo_pago = request.data.get('metodo_pago')
    envio_data = request.data.get('envio')

    if not metodo_pago or not envio_data:
        print(f"Datos incompletos: metodo_pago={metodo_pago}, envio_data={envio_data}")
        return Response({"detail": "Faltan datos necesarios para completar el pedido."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Crear el pedido
        pedido = Pedido.objects.create(
            usuario=usuario,
            total=total_pedido,
            metodo_pago=metodo_pago,
        )

        # Crear el envío asociado al pedido
        envio = Envio.objects.create(
            pedido=pedido,
            direccion_calle_1=envio_data.get('direccion_calle_1'),
            direccion_calle_2=envio_data.get('direccion_calle_2', ''),
            estado='Pendiente',
            codigo_postal=envio_data.get('codigo_postal'),
            ciudad=envio_data.get('ciudad'),
            pais=envio_data.get('pais'),
        )

        serializer = PedidoSerializer(pedido)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except Exception as e:
        print(f"Error al crear el pedido o el envío: {e}")
        return Response({"detail": "Error al procesar el pedido."}, status=status.HTTP_400_BAD_REQUEST)

# Vista para verificar el token en el backend
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verificar_token(request):
    return Response({"message": "Token válido"}, status=status.HTTP_200_OK)
