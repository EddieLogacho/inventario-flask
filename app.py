# app.py
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from db import init_db, db
from models import Producto

# Rutas absolutas a las carpetas del proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")


def create_app():
    # Forzamos a Flask a usar las carpetas correctas (evita problemas de rutas)
    app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

    # ---------- Configuración ----------
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")
    # Por defecto usa SQLite local en el archivo inventario.db
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///inventario.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ---------- Base de datos ----------
    init_db(app)

    # ---------- CLI ----------
    # Comandos: flask --app app create-db / drop-db / seed
    from cli import register_cli
    register_cli(app)

    # ---------- Filtros / Helpers Jinja ----------
    @app.template_filter("moneda")
    def moneda(value):
        """Formatea un número como dinero, e.g. 1234.5 -> $1,234.50"""
        try:
            return f"${float(value):,.2f}"
        except Exception:
            return value

    # ---------- Rutas ----------
    @app.route("/")
    def home():
        return redirect(url_for("lista_productos"))

    @app.route("/productos")
    def lista_productos():
        """
        Listado de productos con búsqueda opcional por nombre (?q=).
        Renderiza: templates/productos_list.html
        """
        q = (request.args.get("q") or "").strip()
        query = Producto.query.order_by(Producto.id.desc())
        if q:
            query = query.filter(Producto.nombre.ilike(f"%{q}%"))
        productos = query.all()
        return render_template("productos_list.html", productos=productos, q=q)

    @app.route("/productos/nuevo", methods=["GET", "POST"])
    def crear_producto():
        """
        Crea un producto nuevo.
        Renderiza: templates/producto_form.html
        """
        if request.method == "POST":
            nombre = (request.form.get("nombre") or "").strip()
            descripcion = (request.form.get("descripcion") or "").strip()
            precio_raw = (request.form.get("precio") or "0").strip().replace(",", ".")
            stock_raw = (request.form.get("stock") or "0").strip()

            errores = []
            # Validaciones
            if not nombre:
                errores.append("El nombre es obligatorio.")

            # Nombre único
            if Producto.query.filter_by(nombre=nombre).first():
                errores.append("Ya existe un producto con ese nombre.")

            # Precio
            try:
                precio = float(precio_raw)
                if precio < 0:
                    errores.append("El precio no puede ser negativo.")
            except ValueError:
                errores.append("El precio no es válido.")

            # Stock
            try:
                stock = int(stock_raw)
                if stock < 0:
                    errores.append("El stock no puede ser negativo.")
            except ValueError:
                errores.append("El stock no es válido.")

            if errores:
                for e in errores:
                    flash(e, "danger")
                # Volver a mostrar el formulario conservando lo ingresado
                return render_template("producto_form.html", producto=None, form=request.form)

            # Crear y guardar
            p = Producto(nombre=nombre, descripcion=descripcion, precio=precio, stock=stock)
            db.session.add(p)
            db.session.commit()
            flash("✅ Producto creado con éxito.", "success")
            return redirect(url_for("lista_productos"))

        # GET
        return render_template("producto_form.html", producto=None)

    @app.route("/productos/<int:producto_id>/editar", methods=["GET", "POST"])
    def editar_producto(producto_id):
        """
        Edita un producto existente.
        Renderiza: templates/producto_form.html
        """
        p = Producto.query.get_or_404(producto_id)

        if request.method == "POST":
            nombre = (request.form.get("nombre") or "").strip()
            descripcion = (request.form.get("descripcion") or "").strip()
            precio_raw = (request.form.get("precio") or "0").strip().replace(",", ".")
            stock_raw = (request.form.get("stock") or "0").strip()

            errores = []
            if not nombre:
                errores.append("El nombre es obligatorio.")

            # Unicidad excluyendo el actual
            existe = Producto.query.filter(Producto.nombre == nombre, Producto.id != p.id).first()
            if existe:
                errores.append("Ya existe un producto con ese nombre.")

            try:
                precio = float(precio_raw)
                if precio < 0:
                    errores.append("El precio no puede ser negativo.")
            except ValueError:
                errores.append("El precio no es válido.")

            try:
                stock = int(stock_raw)
                if stock < 0:
                    errores.append("El stock no puede ser negativo.")
            except ValueError:
                errores.append("El stock no es válido.")

            if errores:
                for e in errores:
                    flash(e, "danger")
                return render_template("producto_form.html", producto=p, form=request.form)

            # Guardar cambios
            p.nombre = nombre
            p.descripcion = descripcion
            p.precio = precio
            p.stock = stock
            db.session.commit()

            flash("✏️ Producto actualizado.", "success")
            return redirect(url_for("lista_productos"))

        # GET: precargar datos
        return render_template("producto_form.html", producto=p)

    @app.route("/productos/<int:producto_id>/eliminar", methods=["POST"])
    def eliminar_producto(producto_id):
        """
        Elimina un producto y retorna al listado.
        """
        p = Producto.query.get_or_404(producto_id)
        db.session.delete(p)
        db.session.commit()
        flash("🗑️ Producto eliminado.", "info")
        return redirect(url_for("lista_productos"))

    return app


# Instancia global para `flask run` o `gunicorn`
app = create_app()

if __name__ == "__main__":
    # Ejecutar con: python app.py
    app.run(debug=True)