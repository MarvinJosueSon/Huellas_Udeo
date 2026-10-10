import mysql.connector
from mysql.connector import Error


class BaseDatos:

    def __init__(
        self,
        host="localhost",
        puerto=3306,
        usuario="root",
        contrasena="110201",
        base_datos="Huellas_Udeo"
    ):
        self.host = host
        self.puerto = puerto
        self.usuario = usuario
        self.contrasena = contrasena
        self.base_datos = base_datos

        self.conexion = None
        self.ultimo_error = None


    def conectar(self):
        try:
            self.conexion = mysql.connector.connect(
                host=self.host,
                port=self.puerto,
                user=self.usuario,
                password=self.contrasena,
                database=self.base_datos,
                charset="utf8mb4"
            )

            self.ultimo_error = None

            return True

        except Error as error:
            self.ultimo_error = str(error)
            self.conexion = None

            return False


    def esta_conectado(self):
        return (
            self.conexion is not None
            and self.conexion.is_connected()
        )


    def obtener_ultimo_error(self):
        return self.ultimo_error


    def consultar(
        self,
        sql,
        parametros=None
    ):
        if not self.esta_conectado():
            self.ultimo_error = (
                "No existe una conexión activa "
                "con la base de datos."
            )
            return []

        cursor = None

        try:
            cursor = self.conexion.cursor(
                dictionary=True
            )

            cursor.execute(
                sql,
                parametros or ()
            )

            datos = cursor.fetchall()

            self.ultimo_error = None

            return datos

        except Error as error:
            self.ultimo_error = str(error)

            return []

        finally:
            if cursor is not None:
                cursor.close()


    def consultar_uno(
        self,
        sql,
        parametros=None
    ):
        datos = self.consultar(
            sql,
            parametros
        )

        if not datos:
            return None

        return datos[0]


    def ejecutar(
        self,
        sql,
        parametros=None
    ):
        if not self.esta_conectado():
            self.ultimo_error = (
                "No existe una conexión activa "
                "con la base de datos."
            )
            return False

        cursor = None

        try:
            cursor = self.conexion.cursor()

            cursor.execute(
                sql,
                parametros or ()
            )

            self.conexion.commit()

            self.ultimo_error = None

            return True

        except Error as error:
            self.conexion.rollback()

            self.ultimo_error = str(error)

            return False

        finally:
            if cursor is not None:
                cursor.close()


    def ejecutar_insert(
        self,
        sql,
        parametros=None
    ):
        if not self.esta_conectado():
            self.ultimo_error = (
                "No existe una conexión activa "
                "con la base de datos."
            )
            return None

        cursor = None

        try:
            cursor = self.conexion.cursor()

            cursor.execute(
                sql,
                parametros or ()
            )

            id_insertado = cursor.lastrowid

            self.conexion.commit()

            self.ultimo_error = None

            return id_insertado

        except Error as error:
            self.conexion.rollback()

            self.ultimo_error = str(error)

            return None

        finally:
            if cursor is not None:
                cursor.close()


    def llamar_procedimiento(
        self,
        nombre,
        parametros=None
    ):
        if not self.esta_conectado():
            self.ultimo_error = (
                "No existe una conexión activa "
                "con la base de datos."
            )
            return None

        cursor = None

        try:
            cursor = self.conexion.cursor(
                dictionary=True
            )

            cursor.callproc(
                nombre,
                parametros or ()
            )

            resultados = []

            for resultado in cursor.stored_results():
                resultados.append(
                    resultado.fetchall()
                )

            self.conexion.commit()

            self.ultimo_error = None

            return resultados

        except Error as error:
            self.conexion.rollback()

            self.ultimo_error = str(error)

            return None

        finally:
            if cursor is not None:
                cursor.close()


    def llamar_procedimiento_uno(
        self,
        nombre,
        parametros=None
    ):
        resultados = self.llamar_procedimiento(
            nombre,
            parametros
        )

        if resultados is None:
            return None

        for conjunto in resultados:
            if conjunto:
                return conjunto[0]

        return None


    def cerrar(self):
        if self.conexion is not None:
            try:
                if self.conexion.is_connected():
                    self.conexion.close()
            except Error:
                pass

        self.conexion = None