import psycopg2

def obtener_conexion():
    return psycopg2.connect(
        host="db.efnjxoyjawfvawyscpdd.supabase.co",
        database="postgres",
        user="postgres",
        password="Salmo150fsu..",
        port=5432,
        sslmode="require"
    )