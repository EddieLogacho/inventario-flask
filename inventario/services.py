from Conexion.conexion import obtener_conexion

# 🔐 USUARIOS (LOGIN Y REGISTRO)
class UsuariosRepo:

    def crear(self, nombre, correo, password):
        conn = obtener_conexion()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO usuarios (nombre, correo, password) VALUES (%s, %s, %s)",
            (nombre, correo, password)
        )
        conn.commit()
        cur.close()
        conn.close()

    def autenticar(self, correo, password):
        conn = obtener_conexion()
        cur = conn.cursor()

        cur.execute(
            "SELECT id, nombre, correo FROM usuarios WHERE correo=%s AND password=%s",
            (correo, password)
        )

        user = cur.fetchone()

        cur.close()
        conn.close()

        if user:
            return {
                "id": user[0],
                "nombre": user[1],
                "correo": user[2]
            }

        return None


# 📦 PRODUCTOS
class ProductosRepo:

    def listar_productos(self):
        conn = obtener_conexion()
        cur = conn.cursor()
        cur.execute("SELECT id, nombre, descripcion, precio, stock FROM productos ORDER BY id DESC")
        rows = cur.fetchall()
        cur.close()
        conn.close()

        return [
            {"id": r[0], "nombre": r[1], "descripcion": r[2], "precio": r[3], "stock": r[4]}
            for r in rows
        ]

    def listar_destacados(self, limite=4):
        conn = obtener_conexion()
        cur = conn.cursor()

        query = f"""
        SELECT id, nombre, descripcion, precio, stock
        FROM productos
        ORDER BY id DESC
        LIMIT {limite}
        """

        cur.execute(query)
        rows = cur.fetchall()

        cur.close()
        conn.close()

        return [
            {"id": r[0], "nombre": r[1], "descripcion": r[2], "precio": r[3], "stock": r[4]}
            for r in rows
        ]

    def obtener(self, id):
        conn = obtener_conexion()
        cur = conn.cursor()
        cur.execute(
            "SELECT id, nombre, descripcion, precio, stock FROM productos WHERE id=%s",
            (id,)
        )
        row = cur.fetchone()
        cur.close()
        conn.close()

        if row:
            return {
                "id": row[0],
                "nombre": row[1],
                "descripcion": row[2],
                "precio": row[3],
                "stock": row[4]
            }
        return None

    def crear(self, nombre, descripcion, precio, stock):
        conn = obtener_conexion()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO productos (nombre, descripcion, precio, stock) VALUES (%s, %s, %s, %s)",
            (nombre, descripcion, precio, stock)
        )
        conn.commit()
        cur.close()
        conn.close()

    def actualizar(self, id, nombre, descripcion, precio, stock):
        conn = obtener_conexion()
        cur = conn.cursor()
        cur.execute(
            "UPDATE productos SET nombre=%s, descripcion=%s, precio=%s, stock=%s WHERE id=%s",
            (nombre, descripcion, precio, stock, id)
        )
        conn.commit()
        cur.close()
        conn.close()

    def eliminar(self, id):
        conn = obtener_conexion()
        cur = conn.cursor()
        cur.execute("DELETE FROM productos WHERE id=%s", (id,))
        conn.commit()
        cur.close()
        conn.close()