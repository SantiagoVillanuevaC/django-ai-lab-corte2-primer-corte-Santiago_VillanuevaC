from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages  # Importante para las alertas
from .models import Producto, Pedido, Cliente
from .forms import ProductoForm, ClienteForm

# --- VISTA DE INICIO ---
def home(request):
    return render(request, "tienda/home.html")

# --- GESTIÓN DE PRODUCTOS ---

def lista_productos(request):
    # Obtenemos productos ordenados alfabéticamente
    query_productos = Producto.objects.all().order_by("nombre")
    return render(request, "tienda/lista_productos.html", {"productos": query_productos})

def detalle_producto(request, pk):
    producto_obj = get_object_or_404(Producto, pk=pk)
    return render(request, "tienda/detalle_producto.html", {"producto": producto_obj})

def crear_producto(request):
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto registrado con éxito.")
            return redirect("tienda:lista_productos")
    else:
        form = ProductoForm()
    return render(request, "tienda/crear_producto.html", {"form": form})

def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == "POST":
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.info(request, f"Se han actualizado los datos de {producto.nombre}.")
            return redirect("tienda:detalle_producto", pk=producto.pk)
    else:
        form = ProductoForm(instance=producto)
    return render(request, "tienda/editar_producto.html", {"form": form, "producto": producto})

def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == "POST":
        nombre_prod = producto.nombre
        producto.delete()
        messages.warning(request, f"El producto {nombre_prod} fue eliminado.")
        return redirect("tienda:lista_productos")
    return render(request, "tienda/eliminar_producto.html", {"producto": producto})


# --- GESTIÓN DE CLIENTES ---

def lista_clientes(request):
    # Lista general de clientes registrados
    todos_los_clientes = Cliente.objects.all().order_by("nombre")
    return render(request, "tienda/lista_clientes.html", {"clientes": todos_los_clientes})

def crear_cliente(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Nuevo cliente agregado al sistema.")
            return redirect("tienda:lista_clientes")
    else:
        form = ClienteForm()
    return render(request, "tienda/crear_cliente.html", {"form": form})

def detalle_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    # Obtenemos historial de pedidos del cliente
    historial = cliente.pedidos.select_related("cliente").prefetch_related("productos").order_by("-fecha")
    return render(request, "tienda/detalle_cliente.html", {"cliente": cliente, "pedidos": historial})


# --- GESTIÓN DE PEDIDOS ---

def lista_pedidos(request):
    # Optimizamos la consulta con select_related y prefetch_related
    pedidos_query = Pedido.objects.select_related("cliente").prefetch_related("productos").order_by("-fecha")
    contexto = {
        "pedidos": pedidos_query,
        "total_pedidos": pedidos_query.count() # Dato extra para el profesor
    }
    return render(request, "tienda/lista_pedidos.html", contexto)

def detalle_pedido(request, pk):
    pedido_det = get_object_or_404(
        Pedido.objects.select_related("cliente").prefetch_related("productos"),
        pk=pk
    )
    return render(request, "tienda/detalle_pedido.html", {"pedido": pedido_det})
