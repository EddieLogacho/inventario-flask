from inventario.inventario import Inventario
from inventario.producto import Producto

inv = Inventario()
inv.cargar_productos()

while True:
    print("""
1. Agregar producto
2. Eliminar producto
3. Actualizar producto
4. Buscar producto
5. Mostrar productos
6. Salir
""")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        nombre = input("Nombre: ")
        cantidad = int(input("Cantidad: "))
        precio = float(input("Precio: "))
        inv.agregar_producto(Producto(None, nombre, cantidad, precio))

    elif opcion == "5":
        inv.cargar_productos()
        for p in inv.productos.values():
            print(p.id, p.nombre, p.cantidad, p.precio)

    elif opcion == "6":
        break