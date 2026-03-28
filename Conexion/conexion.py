# conexion.py
import psycopg2
from psycopg2.extras import RealDictCursor

# Configuración de conexión a Supabase
DB_CONFIG = {
    "host": "TU_HOST_SUPABASE",      # ejemplo: proyecto.supabase.co
    "port": 5432,
    "database": "postgres",          # por defecto Supabase
    "user": "postgres",              # por defecto Supabase
    "password": "Eddie!2026Flask$SecureDB"  # la contraseña que pusiste
}

def obtener_conexion():
    """
    Devuelve una conexión a la base de datos Supabase/PostgreSQL
    """
    return psycopg2.connect(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        database=DB_CONFIG["database"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        cursor_factory=RealDictCursor
    )