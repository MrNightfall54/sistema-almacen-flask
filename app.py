from flask import Flask, jsonify, request

from servicio import (
    servicio_listar_productos,
    servicio_login,
    servicio_registrar_producto,
    servicio_registrar_usuario,
)

app = Flask(__name__)


@app.route("/api/auth/registro", methods=["POST"])
def registro():
    datos = request.get_json(silent=True)

    if datos is None:
        return jsonify({"error": "Debe enviar datos en formato JSON"}), 400

    respuesta, codigo = servicio_registrar_usuario(datos)

    return jsonify(respuesta), codigo


@app.route("/api/auth/login", methods=["POST"])
def login():
    datos = request.get_json(silent=True)

    if datos is None:
        return jsonify({"error": "Debe enviar datos en formato JSON"}), 400

    respuesta, codigo = servicio_login(datos)

    return jsonify(respuesta), codigo


@app.route("/api/almacen/productos", methods=["POST"])
def crear_producto():
    datos = request.get_json(silent=True)

    if datos is None:
        return jsonify({"error": "Debe enviar datos en formato JSON"}), 400

    respuesta, codigo = servicio_registrar_producto(datos)

    return jsonify(respuesta), codigo


@app.route("/api/almacen/productos", methods=["GET"])
def obtener_productos():
    respuesta, codigo = servicio_listar_productos()

    return jsonify(respuesta), codigo


@app.route("/", methods=["GET"])
def inicio():
    return jsonify({"mensaje": "API Sistema de Almacen funcionando"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
