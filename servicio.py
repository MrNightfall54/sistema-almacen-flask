import bcrypt
import mysql.connector

from repositorio import (
    buscar_usuario_por_correo,
    listar_productos,
    registrar_producto,
    registrar_usuario,
)


def servicio_registrar_usuario(datos):
    nombre = datos.get("nombre")
    correo = datos.get("correo")
    password = datos.get("password")

    if not nombre or not correo or not password:
        return {"error": "Nombre, correo y password son obligatorios"}, 400

    nombre = nombre.strip()
    correo = correo.strip().lower()

    if len(password) < 6:
        return {"error": "La contraseña debe tener mínimo 6 caracteres"}, 400

    usuario_existente = buscar_usuario_por_correo(correo)

    if usuario_existente:
        return {"error": "El correo ya se encuentra registrado"}, 409

    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode(
        "utf-8"
    )

    try:
        usuario_id = registrar_usuario(nombre, correo, password_hash)

        return {
            "mensaje": "Usuario registrado correctamente",
            "usuario": {"id": usuario_id, "nombre": nombre, "correo": correo},
        }, 201

    except mysql.connector.Error as error:
        return {"error": "Error al registrar usuario", "detalle": str(error)}, 500


def servicio_login(datos):
    correo = datos.get("correo")
    password = datos.get("password")

    if not correo or not password:
        return {"error": "Correo y password son obligatorios"}, 400

    correo = correo.strip().lower()

    usuario = buscar_usuario_por_correo(correo)

    if usuario is None:
        return {"error": "Credenciales incorrectas"}, 401

    password_correcto = bcrypt.checkpw(
        password.encode("utf-8"), usuario["password_hash"].encode("utf-8")
    )

    if not password_correcto:
        return {"error": "Credenciales incorrectas"}, 401

    return {
        "mensaje": "Login exitoso",
        "usuario": {
            "id": usuario["id"],
            "nombre": usuario["nombre"],
            "correo": usuario["correo"],
        },
    }, 200


def servicio_registrar_producto(datos):
    campos_obligatorios = [
        "sku",
        "nombre",
        "descripcion",
        "stock",
        "precio_unitario",
        "categoria",
    ]

    for campo in campos_obligatorios:
        if campo not in datos:
            return {"error": f"El campo '{campo}' es obligatorio"}, 400

    sku = str(datos["sku"]).strip()
    nombre = str(datos["nombre"]).strip()
    descripcion = str(datos["descripcion"]).strip()
    categoria = str(datos["categoria"]).strip()

    if not sku or not nombre or not descripcion or not categoria:
        return {"error": "Los campos de texto no pueden estar vacíos"}, 400

    try:
        stock = int(datos["stock"])
    except (ValueError, TypeError):
        return {"error": "El stock debe ser un número entero"}, 400

    try:
        precio_unitario = float(datos["precio_unitario"])
    except (ValueError, TypeError):
        return {"error": "El precio unitario debe ser numérico"}, 400

    if stock < 0:
        return {"error": "El stock inicial no puede ser negativo"}, 400

    if precio_unitario <= 0:
        return {"error": "El precio unitario debe ser mayor a cero"}, 400

    try:
        producto_id = registrar_producto(
            sku, nombre, descripcion, stock, precio_unitario, categoria
        )

        return {
            "mensaje": "Producto registrado correctamente",
            "producto": {
                "id": producto_id,
                "sku": sku,
                "nombre": nombre,
                "descripcion": descripcion,
                "stock": stock,
                "precio_unitario": precio_unitario,
                "categoria": categoria,
            },
        }, 201

    except mysql.connector.IntegrityError:
        return {"error": "Ya existe un producto con ese SKU"}, 409

    except mysql.connector.Error as error:
        return {"error": "Error al registrar el producto", "detalle": str(error)}, 500


def servicio_listar_productos():
    try:
        productos = listar_productos()

        return {"cantidad": len(productos), "productos": productos}, 200

    except mysql.connector.Error as error:
        return {"error": "Error al obtener los productos", "detalle": str(error)}, 500
