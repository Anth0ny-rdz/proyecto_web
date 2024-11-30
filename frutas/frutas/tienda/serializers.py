from rest_framework import serializers
from .models import Usuario, Producto, Alergia, Carrito, CarritoItem, Pedido, Envio

class AlergiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alergia
        fields = ['id', 'nombre']


class ProductoSerializer(serializers.ModelSerializer):
    alergias = serializers.PrimaryKeyRelatedField(queryset=Alergia.objects.all(), many=True, required=False)  # Asegura que se puedan asociar alergias opcionales

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'precio', 'descripcion', 'stock', 'tipo', 'alergias']

    def validate_precio(self, value):
        """Asegura que el precio sea positivo."""
        if value <= 0:
            raise serializers.ValidationError("El precio debe ser un valor positivo.")
        return value

    def validate_stock(self, value):
        """Asegura que el stock no sea negativo."""
        if value < 0:
            raise serializers.ValidationError("El stock no puede ser negativo.")
        return value


class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    alergias = serializers.PrimaryKeyRelatedField(queryset=Alergia.objects.all(), many=True)

    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'password', 'alergias']

    def create(self, validated_data):
        # Extraer la lista de alergias y la contraseña
        alergias = validated_data.pop('alergias', [])
        password = validated_data.pop('password')
        
        # Crear la instancia del usuario sin guardar aún
        usuario = Usuario(**validated_data)
        usuario.set_password(password)  # Hashear la contraseña
        usuario.save()

        # Asignar las alergias utilizando .set()
        usuario.alergias.set(alergias)
        return usuario



class CarritoItemSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(source='producto.nombre')
    precio = serializers.DecimalField(source='producto.precio', max_digits=10, decimal_places=2)
    subtotal = serializers.SerializerMethodField()
    id = serializers.IntegerField()  # Incluir ID en la respuesta del carrito

    class Meta:
        model = CarritoItem
        fields = ['id', 'producto_id', 'nombre', 'precio', 'cantidad', 'subtotal']

    def get_subtotal(self, obj):
        return obj.subtotal()


class CarritoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()  # Incluir ID en la respuesta del carrito
    items = CarritoItemSerializer(source='carritoitem_set', many=True)
    total = serializers.SerializerMethodField()
    impuestos = serializers.SerializerMethodField()
    envio = serializers.SerializerMethodField()
    total_final = serializers.SerializerMethodField()

    class Meta:
        model = Carrito
        fields = ['id', 'items', 'total', 'impuestos', 'envio', 'total_final']

    def get_total(self, obj):
        return obj.total()

    def get_impuestos(self, obj):
        return obj.impuestos()

    def get_envio(self, obj):
        return obj.envio()

    def get_total_final(self, obj):
        return obj.total_final()
    
class EnvioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Envio
        fields = ['id', 'direccion_calle_1', 'direccion_calle_2', 'estado', 'codigo_postal', 'ciudad', 'pais', 'pedido']


class PedidoSerializer(serializers.ModelSerializer):
    envios = EnvioSerializer(many=True, read_only=True)

    class Meta:
        model = Pedido
        fields = ['id', 'usuario', 'fecha_pedido', 'total', 'metodo_pago', 'envios']








