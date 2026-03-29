from inventario.bd import obtener_conexion
from inventario.producto import Producto

class Inventario:
    def __init__(self):
        self.productos = {}  # diccionario {id: Producto}

    def cargar_productos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos")
        filas = cursor.fetchall()
        conn.close()

        for fila in filas:
            producto = Producto(*fila)
            self.productos[producto.id] = producto

    def agregar_producto(self, producto):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO productos (nombre, cantidad, precio) VALUES (?, ?, ?)",
            producto.to_tuple()
        )
        conn.commit()
        conn.close()

    def eliminar_producto(self, id_producto):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM productos WHERE id=?", (id_producto,))
        conn.commit()
        conn.close()

    def actualizar_producto(self, id_producto, cantidad, precio):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE productos SET cantidad=?, precio=? WHERE id=?",
            (cantidad, precio, id_producto)
        )
        conn.commit()
        conn.close()

    def buscar_producto(self, nombre):
        return [p for p in self.productos.values() if nombre.lower() in p.nombre.lower()]