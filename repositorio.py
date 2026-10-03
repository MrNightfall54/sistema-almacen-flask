from conexion import obtener_conexion


def registrar_usuario(nombre, correo, password_hash):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        sql = """
            INSERT INTO usuarios_almacen
            (nombre, correo, password_hash)
            VALUES (%s, %s, %s)
        """
        cursor.execute(sql, (nombre, correo, password_hash))
        conexion.commit()
        return cursor.lastrowid

    finally:
        cursor.close()
        conexion.close()


def buscar_usuario_por_correo(correo):
    conexion = obtener_conexion()

    cursor = conexion.cursor(dictionary=True)

    try:
        sql = """
            SELECT
                id,
                nombre,
                correo,
                password_hash,
                fecha_registro
            FROM usuarios_almacen
            WHERE correo = %s
        """

        cursor.execute(sql, (correo,))
        return cursor.fetchone()

    finally:
        cursor.close()
        conexion.close()


def registrar_producto(sku, nombre, descripcion, stock, precio_unitario, categoria):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        sql = """
            INSERT INTO productos_inventario
            (
                sku,
                nombre,
                descripcion,
                stock,
                precio_unitario,
                categoria
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.execute(
            sql, (sku, nombre, descripcion, stock, precio_unitario, categoria)
        )
        conexion.commit()
        return cursor.lastrowid

    finally:
        cursor.close()
        conexion.close()


def listar_productos():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    try:
        sql = """
            SELECT
                id,
                sku,
                nombre,
                descripcion,
                stock,
                precio_unitario,
                categoria,
                fecha_registro
            FROM productos_inventario
            ORDER BY id DESC
        """

        cursor.execute(sql)

        productos = cursor.fetchall()

        for producto in productos:
            producto["precio_unitario"] = float(producto["precio_unitario"])

        return productos

    finally:
        cursor.close()
        conexion.close()
