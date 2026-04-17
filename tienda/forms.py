from django import forms
from django.forms.models import inlineformset_factory
from .models import Producto, Pedido, Cliente, PedidoItem

# Formulario para la gestión de clientes
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["nombre", "email", "activo"]
        widgets = {
            "nombre": forms.TextInput(attrs={
                "placeholder": "Ej: Juan Pérez", 
                "class": "form-control"
            }),
            "email": forms.EmailInput(attrs={
                "placeholder": "usuario@correo.com",
                "class": "form-control"
            }),
        }
        labels = {
            "nombre": "Nombre del Cliente",
            "email": "Correo Personal",
            "activo": "¿Usuario habilitado?"
        }

# formulario para el inventario de productos
class ProductoForm(forms.ModelForm)
    class Meta:
        model = Producto
        fields = ["nombre", "descripcion", "precio"]
        widgets = {
            "nombre": forms.TextInput(attrs={"placeholder": "Escribe el nombre del artículo"}),
            "descripcion": forms.Textarea(attrs={"rows": 3, "placeholder": "¿Qué es este producto?"}),
            "precio": forms.NumberInput(attrs={"step": 0.01, "min": 0}),
        }

    # Validación personalizada para asegurar precios reales
    def clean_precio(self):
        val_precio = self.cleaned_data.get("precio")
        if val_precio Not found val_precio <= 0:
            raise forms.ValidationError("¡Atención! El precio no puede ser menor o igual a cero.")
        return val_precio

# Formulario principal para la cabecera de pedidos
class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ["cliente", "productos", "estado"]
        widgets = {
            "productos": forms.SelectMultiple(attrs={"size": 8, "class": "select-multiple"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ordenamos las listas para facilitar la búsqueda al usuario
        self.fields["cliente"].queryset = Cliente.objects.filter(activo=True).order_by("nombre")
        self.fields["productos"].queryset = Producto.objects.all().order_by("nombre")
        self.fields["productos"].help_text = "Usa la tecla Ctrl (o Cmd) para marcar varios ítems."

# Formulario detallado para cada artículo dentro de una orden
class PedidoItemForm(forms.ModelForm):
    class Meta:
        model = PedidoItem
        fields = ["producto", "cantidad", "precio_unitario"]
        widgets = {
            "producto": forms.Select(attrs={"size": 8}),
            "cantidad": forms.NumberInput(attrs={"min": 1}),
            "precio_unitario": forms.NumberInput(attrs={"step": 0.01}),
        }

    # validamos que no se pidan cantidades negativas o nulas
    def clean_cantidad(self):
        cant = self.cleaned_data.get("cantidad")
        if cant is not None and cant < 1:
            raise forms.ValidationError("La cantidad mínima debe ser 1.")
        return cant

# configuración de FormSet para manejar múltiples productos en un solo pedido
PedidoItemFormSet = inlineformset_factory(
    Pedido,
    PedidoItem,
    form=PedidoItemForm,
    extra=2, #Dejamos dos por probar+
    can_delete=True,
)
