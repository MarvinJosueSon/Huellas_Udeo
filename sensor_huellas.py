import time

try:
    import serial
    from serial.tools import list_ports

    SERIAL_DISPONIBLE = True

except ImportError:
    serial = None
    list_ports = None

    SERIAL_DISPONIBLE = False


class SensorHuellas:

    def __init__(
        self,
        puerto=None,
        baudios=115200
    ):
        self.puerto = puerto
        self.baudios = baudios
        self.serial = None


    def detectar_puerto(self):

        if not SERIAL_DISPONIBLE:
            raise Exception(
                "PySerial no está instalado."
            )

        puertos = list(
            list_ports.comports()
        )

        if not puertos:
            raise Exception(
                "No se encontraron puertos seriales."
            )

        palabras = (
            "arduino",
            "mega",
            "ch340",
            "ch341",
            "usb serial",
            "usb-serial"
        )

        for puerto in puertos:

            descripcion = (
                f"{puerto.device} "
                f"{puerto.description}"
            ).lower()

            if any(
                palabra in descripcion
                for palabra in palabras
            ):
                return puerto.device


        if len(puertos) == 1:
            return puertos[0].device


        raise Exception(
            "Hay varios puertos seriales y no "
            "se pudo identificar automáticamente "
            "el Arduino."
        )


    def conectar(self):

        if self.esta_conectado():
            return True


        if not SERIAL_DISPONIBLE:
            raise Exception(
                "PySerial no está instalado.\n"
                "Instálalo con: pip install pyserial"
            )


        if self.puerto is None:

            self.puerto = (
                self.detectar_puerto()
            )


        self.serial = serial.Serial(
            port=self.puerto,
            baudrate=self.baudios,
            timeout=1,
            write_timeout=2
        )


        time.sleep(2)


        self.serial.reset_input_buffer()
        self.serial.reset_output_buffer()


        self.enviar_linea(
            "PING"
        )


        respuesta = self.esperar_respuesta(
            timeout=5
        )


        if respuesta != "OK|READY":

            self.cerrar()

            raise Exception(
                "El Arduino respondió, pero "
                "el sensor de huella no está listo."
            )


        return True


    def esta_conectado(self):

        return (
            self.serial is not None
            and self.serial.is_open
        )


    def enviar_linea(
        self,
        texto
    ):

        if not self.esta_conectado():

            raise Exception(
                "El Arduino no está conectado."
            )


        mensaje = (
            texto.strip()
            + "\n"
        )

        self.serial.write(
            mensaje.encode(
                "utf-8"
            )
        )

        self.serial.flush()


    def esperar_respuesta(
        self,
        timeout=5
    ):

        inicio = time.time()


        while (
            time.time() - inicio
            < timeout
        ):

            linea = (
                self.serial
                .readline()
                .decode(
                    "utf-8",
                    errors="ignore"
                )
                .strip()
            )


            if linea != "":
                return linea


        raise Exception(
            "Tiempo de espera agotado."
        )


    def enrolar_automatico(
        self,
        callback_estado=None
    ):

        self.conectar()


        self.serial.reset_input_buffer()


        self.enviar_linea(
            "ENROLL_AUTO"
        )


        inicio = time.time()
        timeout = 90


        while (
            time.time() - inicio
            < timeout
        ):

            linea = (
                self.serial
                .readline()
                .decode(
                    "utf-8",
                    errors="ignore"
                )
                .strip()
            )


            if linea == "":
                continue


            partes = linea.split(
                "|"
            )


            if partes[0] == "INFO":

                mensaje = "|".join(
                    partes[1:]
                )

                if callback_estado:
                    callback_estado(
                        mensaje
                    )

                continue


            if (
                len(partes) >= 3
                and partes[0] == "OK"
                and partes[1] == "ENROLL"
            ):

                try:

                    return int(
                        partes[2]
                    )

                except ValueError:

                    raise Exception(
                        "El Arduino devolvió "
                        "un template inválido."
                    )


            if partes[0] == "ERROR":

                mensaje = "|".join(
                    partes[1:]
                )

                raise Exception(
                    mensaje
                )


        raise Exception(
            "Se agotó el tiempo para "
            "registrar la huella."
        )


    def eliminar_template(
        self,
        id_template
    ):

        self.conectar()


        self.serial.reset_input_buffer()


        self.enviar_linea(
            f"DELETE|{id_template}"
        )


        inicio = time.time()


        while (
            time.time() - inicio
            < 10
        ):

            linea = (
                self.serial
                .readline()
                .decode(
                    "utf-8",
                    errors="ignore"
                )
                .strip()
            )


            if linea == "":
                continue


            if linea == (
                f"OK|DELETE|"
                f"{id_template}"
            ):

                return True


            if linea.startswith(
                "ERROR|"
            ):

                raise Exception(
                    linea.split(
                        "|",
                        1
                    )[1]
                )


        raise Exception(
            "No se pudo eliminar "
            "el template del sensor."
        )


    def cerrar(self):

        if self.serial is not None:

            try:

                if self.serial.is_open:
                    self.serial.close()

            except Exception:
                pass


        self.serial = None