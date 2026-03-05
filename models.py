# models.py
from db import db  # <-- Importa la MISMA instancia
from datetime import datetime

class Producto(db.Model):
    __tablename__ = "productos"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), unique=True, nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    precio = db.Column(db.Float, nullable=False, default=0.0)
    stock = db.Column(db.Integer, nullable=False, default=0)

    # --- NUEVO: campos de auditoría ---
    # Se asigna automáticamente al crear (del lado de la BD).
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now()
    )
    # Se actualiza automáticamente en cada UPDATE (puede quedar NULL en creación).
    updated_at = db.Column(
        db.DateTime,
        nullable=True,
        onupdate=db.func.now()
    )

    def __repr__(self):
        return f"<Producto {self.id} - {self.nombre}>"