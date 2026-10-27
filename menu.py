import tkinter as tk
from tkinter import ttk

from modulos.alumnos import Alumnos
from modulos.docentes import Docentes
from modulos.carreras import Carreras
from modulos.jornadas import Jornadas
from modulos.periodos import Periodos
from modulos.cursos import Cursos
from modulos.secciones import Secciones
from modulos.horarios import Horarios
from modulos.inscripciones import Inscripciones
from modulos.huellas import Huellas
from modulos.sesiones import Sesiones
from modulos.asistencia import Asistencia
from modulos.justificaciones import Justificaciones
from modulos.configuracion import ConfiguracionAsistencia
from modulos.puntuacion import Puntuacion
from modulos.reportes import Reportes
from modulos.auditoria import Auditoria


class MenuPrincipal(tk.Frame):

    MORADO = "#46384E"
    MORADO_HOVER = "#5A4964"

    DORADO = "#DDA62F"
    DORADO_HOVER = "#C99326"

    VERDE = "#3F7C49"

    ROJO = "#8F2533"
    ROJO_HOVER = "#77202B"

    FONDO = "#F4F2F0"
    PANEL = "#FFFFFF"

    TEXTO = "#202020"
    TEXTO_SECUNDARIO = "#666666"

    BORDE = "#D8D5D2"


    def __init__(
        self,
        master,
        database,
        sesion,
        al_cerrar_sesion
    ):
        super().__init__(
            master,
            bg=self.FONDO
        )

        self.database = database
        self.sesion = sesion
        self.al_cerrar_sesion = al_cerrar_sesion

        self.pack(
            fill="both",
            expand=True
        )

        self.crear_interfaz()
        self.mostrar_inicio()


    def crear_interfaz(self):

        self.barra_superior = tk.Frame(
            self,
            bg=self.MORADO,
            height=72
        )

        self.barra_superior.pack(
            side="top",
            fill="x"
        )

        self.barra_superior.pack_propagate(
            False
        )


        bloque_marca = tk.Frame(
            self.barra_superior,
            bg=self.MORADO
        )

        bloque_marca.pack(
            side="left",
            padx=(24, 20),
            fill="y"
        )


        tk.Label(
            bloque_marca,
            text="UDEO",
            bg=self.MORADO,
            fg="#FFFFFF",
            font=("Segoe UI", 18, "bold")
        ).pack(
            anchor="w",
            pady=(12, 0)
        )


        tk.Label(
            bloque_marca,
            text="Assistance Digital",
            bg=self.MORADO,
            fg="#D7CFDC",
            font=("Segoe UI", 9)
        ).pack(
            anchor="w"
        )


        bloque_usuario = tk.Frame(
            self.barra_superior,
            bg=self.MORADO
        )

        bloque_usuario.pack(
            side="right",
            padx=(20, 24),
            fill="y"
        )


        tk.Button(
            bloque_usuario,
            text="Cerrar sesión",
            bg=self.ROJO,
            fg="#FFFFFF",
            activebackground=self.ROJO_HOVER,
            activeforeground="#FFFFFF",
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 9, "bold"),
            command=self.al_cerrar_sesion
        ).pack(
            side="right",
            padx=(18, 0),
            pady=20,
            ipadx=12,
            ipady=5
        )


        datos_usuario = tk.Frame(
            bloque_usuario,
            bg=self.MORADO
        )

        datos_usuario.pack(
            side="right",
            pady=13
        )


        tk.Label(
            datos_usuario,
            text=self.sesion.usuario,
            bg=self.MORADO,
            fg="#FFFFFF",
            font=("Segoe UI", 10, "bold")
        ).pack(
            anchor="e"
        )


        tk.Label(
            datos_usuario,
            text=self.sesion.rol,
            bg=self.MORADO,
            fg="#D7CFDC",
            font=("Segoe UI", 8)
        ).pack(
            anchor="e"
        )


        self.barra_navegacion = tk.Frame(
            self,
            bg=self.PANEL,
            height=48,
            highlightthickness=1,
            highlightbackground=self.BORDE
        )

        self.barra_navegacion.pack(
            side="top",
            fill="x"
        )

        self.barra_navegacion.pack_propagate(
            False
        )


        tk.Button(
            self.barra_navegacion,
            text="Inicio",
            bg=self.PANEL,
            fg=self.MORADO,
            activebackground="#EFE8F2",
            activeforeground=self.MORADO,
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            command=self.mostrar_inicio
        ).pack(
            side="left",
            padx=(20, 4),
            pady=7,
            ipadx=14,
            ipady=5
        )


        if self.sesion.es_superadmin():

            self.crear_menu_superadmin()

        elif self.sesion.es_docente():

            self.crear_menu_docente()


        self.contenido = tk.Frame(
            self,
            bg=self.FONDO
        )

        self.contenido.pack(
            side="top",
            fill="both",
            expand=True
        )


    def crear_menu_desplegable(
        self,
        texto,
        opciones
    ):

        boton = tk.Menubutton(
            self.barra_navegacion,
            text=texto,
            bg=self.PANEL,
            fg=self.TEXTO,
            activebackground="#EFE8F2",
            activeforeground=self.MORADO,
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 10),
            padx=14,
            pady=5
        )

        boton.pack(
            side="left",
            padx=2,
            pady=7
        )


        menu = tk.Menu(
            boton,
            tearoff=0,
            bg=self.PANEL,
            fg=self.TEXTO,
            activebackground=self.DORADO,
            activeforeground=self.TEXTO,
            bd=1,
            relief="solid",
            font=("Segoe UI", 9)
        )


        for nombre, comando in opciones:

            menu.add_command(
                label=nombre,
                command=comando
            )


        boton.config(
            menu=menu
        )


    def crear_menu_superadmin(self):

        self.crear_menu_desplegable(
            "Académico",
            (
                (
                    "Alumnos",
                    self.mostrar_alumnos
                ),
                (
                    "Docentes",
                    self.mostrar_docentes
                ),
                (
                    "Carreras",
                    self.mostrar_carreras
                ),
                (
                    "Jornadas",
                    self.mostrar_jornadas
                ),
                (
                    "Periodos",
                    self.mostrar_periodos
                ),
                (
                    "Cursos",
                    self.mostrar_cursos
                ),
                (
                    "Secciones",
                    self.mostrar_secciones
                ),
                (
                    "Horarios",
                    self.mostrar_horarios
                ),
                (
                    "Inscripciones",
                    self.mostrar_inscripciones
                )
            )
        )


        self.crear_menu_desplegable(
            "Asistencia",
            (
                (
                    "Huellas",
                    self.mostrar_huellas
                ),
                (
                    "Sesiones",
                    self.mostrar_sesiones
                ),
                (
                    "Asistencia",
                    self.mostrar_asistencia
                ),
                (
                    "Justificaciones",
                    self.mostrar_justificaciones
                )
            )
        )


        self.crear_menu_desplegable(
            "Administración",
            (
                (
                    "Configuración",
                    self.mostrar_configuracion
                ),
                (
                    "Puntuación",
                    self.mostrar_puntuacion
                ),
                (
                    "Auditoría",
                    self.mostrar_auditoria
                )
            )
        )


        self.crear_menu_desplegable(
            "Reportes",
            (
                (
                    "Consultar reportes",
                    self.mostrar_reportes
                ),
            )
        )


    def crear_menu_docente(self):

        self.crear_menu_desplegable(
            "Académico",
            (
                (
                    "Mis secciones",
                    lambda:
                        self.mostrar_pendiente(
                            "Mis secciones"
                        )
                ),
                (
                    "Mis alumnos",
                    self.mostrar_inscripciones
                ),
                (
                    "Horarios",
                    self.mostrar_horarios
                )
            )
        )


        self.crear_menu_desplegable(
            "Asistencia",
            (
                (
                    "Sesiones",
                    self.mostrar_sesiones
                ),
                (
                    "Asistencia",
                    self.mostrar_asistencia
                ),
                (
                    "Justificaciones",
                    self.mostrar_justificaciones
                )
            )
        )


        self.crear_menu_desplegable(
            "Puntuación",
            (
                (
                    "Puntuación",
                    self.mostrar_puntuacion
                ),
            )
        )


        self.crear_menu_desplegable(
            "Reportes",
            (
                (
                    "Consultar reportes",
                    self.mostrar_reportes
                ),
            )
        )


    def limpiar_contenido(self):

        for widget in (
            self.contenido.winfo_children()
        ):

            widget.destroy()


    def mostrar_inicio(self):

        self.limpiar_contenido()


        contenedor = tk.Frame(
            self.contenido,
            bg=self.FONDO
        )

        contenedor.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=30
        )


        tk.Label(
            contenedor,
            text="Inicio",
            bg=self.FONDO,
            fg=self.MORADO,
            font=("Segoe UI", 26, "bold")
        ).pack(
            anchor="w"
        )


        tk.Label(
            contenedor,
            text=(
                f"Bienvenido, "
                f"{self.sesion.usuario}"
            ),
            bg=self.FONDO,
            fg=self.TEXTO,
            font=("Segoe UI", 14)
        ).pack(
            anchor="w",
            pady=(8, 2)
        )


        tk.Label(
            contenedor,
            text=(
                f"Rol: "
                f"{self.sesion.rol}"
            ),
            bg=self.FONDO,
            fg=self.TEXTO_SECUNDARIO,
            font=("Segoe UI", 10)
        ).pack(
            anchor="w"
        )


        tk.Label(
            contenedor,
            text="Accesos rápidos",
            bg=self.FONDO,
            fg=self.MORADO,
            font=("Segoe UI", 15, "bold")
        ).pack(
            anchor="w",
            pady=(30, 15)
        )


        panel_tarjetas = tk.Frame(
            contenedor,
            bg=self.FONDO
        )

        panel_tarjetas.pack(
            fill="x"
        )


        panel_tarjetas.grid_columnconfigure(
            0,
            weight=1
        )

        panel_tarjetas.grid_columnconfigure(
            1,
            weight=1
        )

        panel_tarjetas.grid_columnconfigure(
            2,
            weight=1
        )

        panel_tarjetas.grid_columnconfigure(
            3,
            weight=1
        )


        if self.sesion.es_superadmin():

            tarjetas = (
                (
                    "Alumnos",
                    "Administrar estudiantes.",
                    self.mostrar_alumnos
                ),
                (
                    "Huellas",
                    "Registrar huellas digitales.",
                    self.mostrar_huellas
                ),
                (
                    "Sesiones",
                    "Abrir y controlar clases.",
                    self.mostrar_sesiones
                ),
                (
                    "Asistencia",
                    "Registrar asistencia por huella.",
                    self.mostrar_asistencia
                )
            )

        else:

            tarjetas = (
                (
                    "Mis alumnos",
                    "Consultar alumnos inscritos.",
                    self.mostrar_inscripciones
                ),
                (
                    "Horarios",
                    "Consultar horarios.",
                    self.mostrar_horarios
                ),
                (
                    "Sesiones",
                    "Abrir y controlar clases.",
                    self.mostrar_sesiones
                ),
                (
                    "Asistencia",
                    "Registrar asistencia por huella.",
                    self.mostrar_asistencia
                )
            )


        for columna, tarjeta in enumerate(
            tarjetas
        ):

            self.crear_tarjeta(
                panel_tarjetas,
                columna,
                tarjeta[0],
                tarjeta[1],
                tarjeta[2]
            )


    def crear_tarjeta(
        self,
        padre,
        columna,
        titulo,
        descripcion,
        comando
    ):

        tarjeta = tk.Frame(
            padre,
            bg=self.PANEL,
            highlightthickness=1,
            highlightbackground=self.BORDE
        )

        tarjeta.grid(
            row=0,
            column=columna,
            sticky="nsew",
            padx=(
                0 if columna == 0 else 6,
                0 if columna == 3 else 6
            )
        )


        tk.Frame(
            tarjeta,
            bg=self.DORADO,
            height=4
        ).pack(
            fill="x"
        )


        tk.Label(
            tarjeta,
            text=titulo,
            bg=self.PANEL,
            fg=self.MORADO,
            font=("Segoe UI", 13, "bold")
        ).pack(
            anchor="w",
            padx=18,
            pady=(18, 5)
        )


        tk.Label(
            tarjeta,
            text=descripcion,
            bg=self.PANEL,
            fg=self.TEXTO_SECUNDARIO,
            font=("Segoe UI", 9),
            justify="left",
            wraplength=180
        ).pack(
            anchor="w",
            padx=18
        )


        tk.Button(
            tarjeta,
            text="Abrir",
            bg=self.DORADO,
            fg=self.TEXTO,
            activebackground=self.DORADO_HOVER,
            activeforeground=self.TEXTO,
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 9, "bold"),
            command=comando
        ).pack(
            anchor="w",
            padx=18,
            pady=(18, 18),
            ipadx=14,
            ipady=4
        )


    def mostrar_alumnos(self):

        self.limpiar_contenido()

        Alumnos(
            self.contenido,
            self.database
        )


    def mostrar_docentes(self):

        self.limpiar_contenido()

        Docentes(
            self.contenido,
            self.database
        )


    def mostrar_carreras(self):

        self.limpiar_contenido()

        Carreras(
            self.contenido,
            self.database
        )


    def mostrar_jornadas(self):

        self.limpiar_contenido()

        Jornadas(
            self.contenido,
            self.database
        )


    def mostrar_periodos(self):

        self.limpiar_contenido()

        Periodos(
            self.contenido,
            self.database
        )


    def mostrar_cursos(self):

        self.limpiar_contenido()

        Cursos(
            self.contenido,
            self.database
        )


    def mostrar_secciones(self):

        self.limpiar_contenido()

        Secciones(
            self.contenido,
            self.database
        )


    def mostrar_horarios(self):

        self.limpiar_contenido()

        Horarios(
            self.contenido,
            self.database
        )


    def mostrar_inscripciones(self):

        self.limpiar_contenido()

        Inscripciones(
            self.contenido,
            self.database
        )


    def mostrar_huellas(self):

        self.limpiar_contenido()

        Huellas(
            self.contenido,
            self.database
        )


    def mostrar_sesiones(self):

        self.limpiar_contenido()

        Sesiones(
            self.contenido,
            self.database,
            self.sesion
        )


    def mostrar_asistencia(self):

        self.limpiar_contenido()

        Asistencia(
            self.contenido,
            self.database
        )


    def mostrar_justificaciones(self):

        self.limpiar_contenido()

        Justificaciones(
            self.contenido,
            self.database
        )


    def mostrar_configuracion(self):

        self.limpiar_contenido()

        ConfiguracionAsistencia(
            self.contenido,
            self.database
        )


    def mostrar_puntuacion(self):

        self.limpiar_contenido()

        Puntuacion(
            self.contenido,
            self.database
        )


    def mostrar_reportes(self):

        self.limpiar_contenido()

        Reportes(
            self.contenido,
            self.database
        )


    def mostrar_auditoria(self):

        self.limpiar_contenido()

        Auditoria(
            self.contenido,
            self.database
        )


    def mostrar_pendiente(
        self,
        nombre
    ):

        self.limpiar_contenido()


        contenedor = tk.Frame(
            self.contenido,
            bg=self.FONDO
        )

        contenedor.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=35
        )


        tk.Label(
            contenedor,
            text=nombre,
            bg=self.FONDO,
            fg=self.MORADO,
            font=("Segoe UI", 26, "bold")
        ).pack(
            anchor="w"
        )


        tk.Label(
            contenedor,
            text=(
                "Este módulo se agregará "
                "cuando corresponda."
            ),
            bg=self.FONDO,
            fg=self.TEXTO_SECUNDARIO,
            font=("Segoe UI", 11)
        ).pack(
            anchor="w",
            pady=(20, 0)
        )