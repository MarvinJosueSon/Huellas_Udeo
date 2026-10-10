class Sesion:

    def __init__(self):
        self.id_usuario = None
        self.usuario = None
        self.rol = None
        self.id_docente = None


    def iniciar(self, datos_usuario):

        self.id_usuario = datos_usuario["id"]
        self.usuario = datos_usuario["usuario"]
        self.rol = datos_usuario["rol"]
        self.id_docente = datos_usuario["id_docente"]


    def cerrar(self):

        self.id_usuario = None
        self.usuario = None
        self.rol = None
        self.id_docente = None


    def activa(self):

        return self.id_usuario is not None


    def es_superadmin(self):

        return self.rol == "SUPERADMIN"


    def es_docente(self):

        return self.rol == "DOCENTE"


    def obtener_datos(self):

        return {
            "id": self.id_usuario,
            "usuario": self.usuario,
            "rol": self.rol,
            "id_docente": self.id_docente
        }