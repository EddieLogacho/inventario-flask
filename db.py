# db.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    """Inicializa SQLAlchemy y crea tablas si no existen."""
    db.init_app(app)
    with app.app_context():
        db.create_all()