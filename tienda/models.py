from django.db import models

# Modelo para gestionar el inventario de la tienda
class Producto(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Producto")
    descripcion = models.TextField(verbose_name="Descripción")
    precio = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Precio Unitario")

    def __str__(self):
        return f"{self.nombre} (${self.precio})"

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"


# Registro de clientes que realizan compras
class Cliente(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre Completo")
    email = models.EmailField(unique=True, verbose_name="Correo Electrónico")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")
    activo = models.BooleanField(default=True, verbose_name="Cuenta Activa")

    def __str__(self):
        return f"{self.nombre} - {self.email}"

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"


# Estructura principal para las órdenes de compra
class Pedido(models.Model):
    # Opciones de estado para el flujo del pedido
    ESTADOS = [
        ("CREADO", "Creado"),
        ("PAGADO", "Pagado"),
        ("ENVIADO", "Enviado"),
        ("CERRADO", "Cerrado"),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="pedidos", verbose_name="Cliente Asociado")
    productos = models.ManyToManyField(Producto, related_name="pedidos", verbose_name="Artículos")
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=7, choices=ESTADOS, default="CREADO") 

    def __str__(self):
        return f"Orden #{self.pk} | Cliente: {self.cliente.nombre} | Estado: {self.estado}"

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"


# Detalle individual de cada producto dentro de un pedido
class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="items")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="items_pedido")
    cantidad = models.IntegerField(default=1, verbose_name="Cantidad Solicitada")
    precio_unitario = models.DecimalField(max_digits=8, decimal_places=2)
    precio_total = models.DecimalField(max_digits=8, decimal_places=2, editable=False)

    class Meta:
        unique_together = ["pedido", "producto"]
        verbose_name = "Detalle de Pedido"
        verbose_name_plural = "Detalles de Pedidos"

    # Lógica para calcular automáticamente el subtotal antes de guardar
    def save(self, *args, **kwargs):
        self.precio_total = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Item: {self.producto.nombre} (x{self.cantidad})"
