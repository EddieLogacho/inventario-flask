import pymysql

def obtener_conexion():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",  # coloca tu contraseña si tienes
        database="inventario",
        cursorclass=pymysql.cursors.DictCursor
    )