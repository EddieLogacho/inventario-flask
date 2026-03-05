# db.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    """
    Inicializa SQLAlchemy con la app y crea las tablas si no existen.
    """
    db.init_app(app)
    with app.app_context():
        # Importa los modelos aquí para que queden registrados antes de create_all
        from models import Producto
        db.create_all()