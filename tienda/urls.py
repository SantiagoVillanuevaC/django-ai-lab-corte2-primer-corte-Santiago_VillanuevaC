from django.urls import path
from . import views

# Espacio de nombres para las rutas de la aplicación
app_name = "tienda"

urlpatterns = [
    # --- Inicio ---
    path("", views.home, name="home"),

    # --- Gestión de Inventario (Productos) ---
    path("productos/", views.lista_productos, name="lista_productos"),
    path("productos/nuevo/", views.crear_producto, name="crear_producto"),
    path("productos/<int:pk>/", views.detalle_producto, name="detalle_producto"),
    path("productos/<int:pk>/editar/", views.editar_producto, name="editar_producto"),
    path("pedidos/<int:pk>/editar/", views.editar_pedido, name="editar_pedido"),
    path("productos/<int:pk>/eliminar/", views.eliminar_producto, name="eliminar_producto"),

    # --- Gestión de Clientes ---
    path("clientes/", views.lista_clientes, name="lista_clientes"),
    path("clientes/nuevo/", views.crear_cliente, name="crear_cliente"),
    path("clientes/<int:pk>/", views.detalle_cliente, name="detalle_cliente"), # Agregué la / al final
    path("clientes/<int:pk>/editar/", views.editar_cliente, name="editar_cliente"),
    path("clientes/<int:pk>/eliminar/", views.eliminar_cliente, name="eliminar_cliente"),

    # --- Gestión de Órdenes (Pedidos) ---
    path("pedidos/", views.lista_pedidos, name="lista_pedidos"),
    path("pedidos/<int:pk>/", views.detalle_pedido, name="detalle_pedido"), # Agregué la / al final
]
