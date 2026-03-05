# cli.py
import click
from flask import current_app
from flask.cli import with_appcontext
from db import db
from models import Producto

@click.command("create-db")
@with_appcontext
def create_db_command():
    db.create_all()
    click.echo("✅ Base de datos creada.")

@click.command("drop-db")
@with_appcontext
def drop_db_command():
    db.drop_all()
    click.echo("🗑️ Base de datos eliminada.")

@click.command("seed")
@with_appcontext
def seed_command():
    demo = [
        Producto(nombre="Laptop", descripcion="14 pulgadas", precio=650.0, stock=5),
        Producto(nombre="Mouse", descripcion="Óptico", precio=12.5, stock=30),
    ]
    db.session.add_all(demo)
    db.session.commit()
    click.echo("🌱 Datos de ejemplo insertados.")

def register_cli(app):
    app.cli.add_command(create_db_command)
    app.cli.add_command(drop_db_command)
    app.cli.add_command(seed_command)