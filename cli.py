# cli.py
import click
from db import db
from models import Producto


def register_cli(app):
    @app.cli.command("create-db")
    def create_db():
        """Crea las tablas en la base de datos."""
        db.create_all()
        click.echo("✔ Tablas creadas")

    @app.cli.command("drop-db")
    def drop_db():
        """Elimina todas las tablas."""
        db.drop_all()
        click.echo("✔ Tablas eliminadas")

    @app.cli.command("seed")
    def seed():
        """Inserta datos de ejemplo si la tabla está vacía."""
        if Producto.query.count() > 0:
            click.echo("ℹ Ya existen productos; no se insertó nada.")
            return

        ejemplos = [
            Producto(nombre="Teclado", descripcion="Mecánico", precio=45.9, stock=10),
            Producto(nombre="Mouse", descripcion="Inalámbrico", precio=25.0, stock=20),
            Producto(nombre="Monitor", descripcion="24 pulgadas", precio=150.0, stock=5),
        ]
        db.session.add_all(ejemplos)
        db.session.commit()
        click.echo("✔ Datos de ejemplo insertados")