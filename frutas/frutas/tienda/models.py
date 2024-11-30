from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from decimal import Decimal

class Alergia(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Usuario(AbstractUser):
    alergias = models.ManyToManyField(Alergia, blank=True, related_name="usuarios")

    groups = models.ManyToManyField(
        Group,
        related_name="tienda_usuario_groups",
        blank=True,
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="tienda_usuario_permissions",
        blank=True,
        verbose_name="user permissions",
    )


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField()
    stock = models.IntegerField()
    tipo = models.CharField(max_length=50)
    alergias = models.ManyToManyField(Alergia, blank=True, related_name="productos")

    def __str__(self):
        return self.nombre


class Carrito(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    creado_en = models.DateTimeField(auto_now_add=True)

    def total(self):
        # Aquí haces la suma de los productos en el carrito
        total = Decimal('0.00')
        for item in self.carritoitem_set.all():
            total += item.producto.precio * item.cantidad
        return total
    
    def impuestos(self):
        iva = Decimal('0.16')  # 16% de IVA
        return self.total() * iva  # IVA

    def envio(self):
        return Decimal('50.00')  # Convertimos la tarifa de envío a Decimal

    def total_final(self):
        return self.total() + self.impuestos() + self.envio()


class CarritoItem(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.producto.precio * self.cantidad

    def __str__(self):
        return f"{self.producto.nombre} - {self.cantidad} unidades"
    
class Pedido(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)  # Usuario asociado al pedido
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=50)

    def __str__(self):
        return f"Pedido {self.id} - {self.usuario}"


class Envio(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='envios')  # Relación con Pedido
    estado = models.CharField(
        max_length=255,
        default='Pendiente',
        choices=[
            ('Pendiente', 'Pendiente'),
            ('Enviado', 'Enviado'),
            ('Entregado', 'Entregado'),
        ]
    )
    direccion_calle_1 = models.CharField(max_length=255)
    direccion_calle_2 = models.CharField(max_length=255, blank=True, null=True)
    codigo_postal = models.CharField(max_length=10)
    ciudad = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)

    def __str__(self):
        return f"Envio {self.id} - {self.estado} para Pedido {self.pedido.id}"









