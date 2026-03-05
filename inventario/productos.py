# inventario/productos.py
import json
import csv
from pathlib import Path
from datetime import datetime

BASE_DATA = Path(__file__).resolve().parent / "data"
TXT_PATH = BASE_DATA / "datos.txt"
JSON_PATH = BASE_DATA / "datos.json"
CSV_PATH = BASE_DATA / "datos.csv"


def _ensure_dir():
    BASE_DATA.mkdir(parents=True, exist_ok=True)


# ---------------- TXT ----------------
def guardar_txt(nombre: str, precio: float, stock: int, descripcion: str = ""):
    _ensure_dir()
    linea = f"{datetime.now().isoformat()} | {nombre} | {precio} | {stock} | {descripcion}"
    with open(TXT_PATH, "a", encoding="utf-8") as f:
        f.write(linea + "\n")


def leer_txt():
    if not TXT_PATH.exists():
        return []
    with open(TXT_PATH, "r", encoding="utf-8") as f:
        return [l.strip() for l in f if l.strip()]


# ---------------- JSON ----------------
# Guardamos una LISTA de productos en JSON y vamos agregando
def guardar_json(nombre: str, precio: float, stock: int, descripcion: str = ""):
    _ensure_dir()
    data = []
    if JSON_PATH.exists():
        try:
            with open(JSON_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, list):
                data = []
        except Exception:
            data = []
    data.append({
        "nombre": nombre,
        "precio": precio,
        "stock": stock,
        "descripcion": descripcion,
        "fecha": datetime.now().isoformat()
    })
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def leer_json():
    if not JSON_PATH.exists():
        return []
    try:
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except Exception:
        return []


# ---------------- CSV ----------------
def guardar_csv(nombre: str, precio: float, stock: int, descripcion: str = ""):
    _ensure_dir()
    new_file = not CSV_PATH.exists()
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow(["fecha", "nombre", "precio", "stock", "descripcion"])
        writer.writerow([datetime.now().isoformat(), nombre, precio, stock, descripcion])


def leer_csv():
    if not CSV_PATH.exists():
        return []
    with open(CSV_PATH, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)
