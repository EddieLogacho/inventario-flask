from flask import Flask, render_template, request, redirect, url_for, session, flash
from services import UsuariosRepo, ProductosRepo

app = Flask(__name__)
app.secret_key = "clave_secreta"

usuarios_repo = UsuariosRepo()
productos_repo = ProductosRepo()

# -------------------------
# 🔐 DECORADOR LOGIN MEJORADO
# -------------------------
def requiere_login(view):
    from functools import wraps
    @wraps(view)
    def wrapper(*args, **kwargs):
        if not session.get('user'):
            flash("Debes iniciar sesión primero", "warning")
            return redirect(url_for('login'))
        return view(*args, **kwargs)
    return wrapper


# -------------------------
# RUTAS PÚBLICAS
# -------------------------
@app.route("/")
def index():
    productos_destacados = productos_repo.listar_destacados()
    return render_template("index.html", productos_destacados=productos_destacados)


@app.route("/catalogo")
def catalogo():
    productos = productos_repo.listar_productos()
    return render_template("catalogo.html", productos=productos)


@app.route("/about")
def about():
    return render_template("about.html")


# -------------------------
# 🔐 LOGIN (MEJORADO)
# -------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        correo = request.form["correo"]
        password = request.form["password"]

        user = usuarios_repo.autenticar(correo, password)

        if user:
            session["user"] = user
            flash("Bienvenido", "success")

            # 🔥 CAMBIO IMPORTANTE AQUÍ
            return redirect(url_for("stock"))

        flash("Credenciales incorrectas", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada", "success")
    return redirect(url_for("index"))


# -------------------------
# REGISTRO
# -------------------------
@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form["nombre"]
        correo = request.form["correo"]
        password = request.form["password"]

        usuarios_repo.crear(nombre, correo, password)

        flash("Usuario creado", "success")
        return redirect(url_for("login"))

    return render_template("registro.html")


# -------------------------
# 🔒 STOCK (PROTEGIDO)
# -------------------------
@app.route("/stock")
@requiere_login
def stock():
    productos = productos_repo.listar_productos()
    return render_template("stock.html", productos=productos)


# -------------------------
# 🛒 CARRITO (SIN ERROR)
# -------------------------
@app.route("/carrito/agregar/<int:producto_id>", methods=["POST"])
def agregar_al_carrito(producto_id):
    if "carrito" not in session:
        session["carrito"] = []

    session["carrito"].append(producto_id)
    session.modified = True

    flash("Producto agregado al carrito", "success")
    return redirect(url_for("catalogo"))


# -------------------------
# INICIO
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)