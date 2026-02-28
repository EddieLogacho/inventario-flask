# models.py
from datetime import datetime
from db import db


class Producto(db.Model):
    __tablename__ = "productos"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False, unique=True)
    descripcion = db.Column(db.Text, default="")
    precio = db.Column(db.Float, nullable=False, default=0.0)
    stock = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # ==== Métodos de ayuda orientados a objetos ====
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def buscar_por_nombre(texto: str):
        """Devuelve un query filtrando por nombre (case-insensitive)."""
        return Producto.query.filter(Producto.nombre.ilike(f"%{texto}%"))

    def __repr__(self) -> str:
        return f"<Producto {self.id} - {self.nombre}>"