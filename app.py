from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from conexion.conexion import obtener_conexion
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io

app = Flask(__name__)
app.secret_key = "clave_secreta_inventario"

# ------------------------------
# INICIO
# ------------------------------
@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contactos")
def contactos():
    return render_template("contactos.html")

# ------------------------------
# CRUD PRODUCTOS
# ------------------------------
@app.route("/productos")
def productos():
    conn = obtener_conexion()
    cur = conn.cursor()
    cur.execute("SELECT * FROM productos")
    datos = cur.fetchall()
    conn.close()
    return render_template("productos.html", productos=datos)

@app.route("/form", methods=["GET", "POST"])
def formulario_producto():
    if request.method == "POST":
        nombre = request.form["nombre"]
        precio = request.form["precio"]
        stock = request.form["stock"]

        conn = obtener_conexion()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO productos (nombre, precio, stock) VALUES (%s,%s,%s)",
            (nombre, precio, stock)
        )
        conn.commit()
        conn.close()

        flash("Producto agregado correctamente", "success")
        return redirect(url_for("productos"))

    return render_template("producto_form.html")

@app.route("/eliminar/<int:id_producto>")
def eliminar_producto(id_producto):
    conn = obtener_conexion()
    cur = conn.cursor()
    cur.execute("DELETE FROM productos WHERE id_producto=%s", (id_producto,))
    conn.commit()
    conn.close()
    return redirect(url_for("productos"))

# ------------------------------
# REPORTE PDF
# ------------------------------
@app.route("/reporte_pdf")
def reporte_productos_pdf():
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    w, h = A4

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(200, h - 50, "Reporte de Productos")

    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(50, h - 100, "ID")
    pdf.drawString(100, h - 100, "Nombre")
    pdf.drawString(280, h - 100, "Precio")
    pdf.drawString(350, h - 100, "Stock")

    conn = obtener_conexion()
    cur = conn.cursor()
    cur.execute("SELECT * FROM productos")
    productos = cur.fetchall()
    conn.close()

    y = h - 120
    pdf.setFont("Helvetica", 10)

    for p in productos:
        pdf.drawString(50, y, str(p["id_producto"]))
        pdf.drawString(100, y, p["nombre"])
        pdf.drawString(280, y, str(p["precio"]))
        pdf.drawString(350, y, str(p["stock"]))
        y -= 15
        if y < 50:
            pdf.showPage()
            y = h - 50

    pdf.save()
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="reporte_productos.pdf",
        mimetype="application/pdf"
    )

if __name__ == "__main__":
    app.run(debug=True)
