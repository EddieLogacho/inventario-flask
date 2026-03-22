from flask import Flask, render_template, request, redirect, url_for, session, flash
from services import UsuariosRepo, ProductosRepo

app = Flask(__name__)
app.secret_key = "clave_secreta"

usuarios_repo = UsuariosRepo()
productos_repo = ProductosRepo()

# -------------------------
# 🔐 DECORADOR LOGIN
# -------------------------
def requiere_login(view):
    from functools import wraps
    @wraps(view)
    def wrapper(*args, **kwargs):
        if not session.get('user'):
            return redirect(url_for('login'))
        return view(*args, **kwargs)
    return wrapper


# -------------------------
# 🔒 PROTEGER TODA LA APP
# -------------------------
@app.route("/")
def home():
    if not session.get('user'):
        return redirect(url_for('login'))
    return redirect(url_for('index'))


@app.route("/index")
@requiere_login
def index():
    productos_destacados = productos_repo.listar_destacados()
    return render_template("index.html", productos_destacados=productos_destacados)


@app.route("/catalogo")
@requiere_login
def catalogo():
    productos = productos_repo.listar_productos()
    return render_template("catalogo.html", productos=productos)


@app.route("/stock")
@requiere_login
def stock():
    productos = productos_repo.listar_productos()
    return render_template("stock.html", productos=productos)


@app.route("/about")
@requiere_login
def about():
    return render_template("about.html")


# -------------------------
# 🔐 LOGIN
# -------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        correo = request.form["correo"]
        password = request.form["password"]

        user = usuarios_repo.autenticar(correo, password)

        if user:
            session["user"] = user
            return redirect(url_for("index"))

        flash("Credenciales incorrectas", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# -------------------------
# REGISTRO
# -------------------------
@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form["nombre"]
        correo = request.form["correo"]
        password = request.form["password"]

        if usuarios_repo.existe_correo(correo):
            flash("El correo ya existe", "warning")
            return render_template("registro.html")

        usuarios_repo.crear(nombre, correo, password)
        flash("Cuenta creada, inicia sesión", "success")
        return redirect(url_for("login"))

    return render_template("registro.html")


# -------------------------
# 🛒 CARRITO
# -------------------------
@app.route("/carrito/agregar/<int:producto_id>", methods=["POST"])
@requiere_login
def agregar_al_carrito(producto_id):
    if "carrito" not in session:
        session["carrito"] = []

    session["carrito"].append(producto_id)
    session.modified = True

    flash("Producto agregado", "success")
    return redirect(url_for("catalogo"))


# -------------------------
# RUN
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)