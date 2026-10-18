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

    def __init__(
        self,
        master,
        database,
        sesion,
        al_cerrar_sesion
    ):
        super().__init__(
            master,
            bg="#F3F3F3"
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

        self.sidebar = tk.Frame(
            self,
            bg="#202020",
            width=220
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.sidebar.pack_propagate(
            False
        )


        self.scroll_sidebar = ttk.Scrollbar(
            self.sidebar,
            orient="vertical"
        )

        self.scroll_sidebar.pack(
            side="right",
            fill="y"
        )


        self.canvas_sidebar = tk.Canvas(
            self.sidebar,
            bg="#202020",
            highlightthickness=0,
            bd=0,
            yscrollcommand=self.scroll_sidebar.set
        )

        self.canvas_sidebar.pack(
            side="left",
            fill="both",
            expand=True
        )


        self.scroll_sidebar.config(
            command=self.canvas_sidebar.yview
        )


        self.menu_contenido = tk.Frame(
            self.canvas_sidebar,
            bg="#202020"
        )


        self.ventana_menu = (
            self.canvas_sidebar.create_window(
                (0, 0),
                window=self.menu_contenido,
                anchor="nw"
            )
        )


        self.menu_contenido.bind(
            "<Configure>",
            self.actualizar_region_scroll
        )


        self.canvas_sidebar.bind(
            "<Configure>",
            self.ajustar_ancho_menu
        )


        self.canvas_sidebar.bind(
            "<MouseWheel>",
            self.desplazar_menu
        )

        self.menu_contenido.bind(
            "<MouseWheel>",
            self.desplazar_menu
        )


        self.contenido = tk.Frame(
            self,
            bg="#F3F3F3"
        )

        self.contenido.pack(
            side="right",
            fill="both",
            expand=True
        )


        tk.Label(
            self.menu_contenido,
            text="UDEO",
            bg="#202020",
            fg="#FFFFFF",
            font=("Segoe UI", 22, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(25, 0)
        )


        tk.Label(
            self.menu_contenido,
            text="Assistance Digital",
            bg="#202020",
            fg="#BFBFBF",
            font=("Segoe UI", 10)
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 20)
        )


        tk.Label(
            self.menu_contenido,
            text=self.sesion.usuario,
            bg="#202020",
            fg="#FFFFFF",
            font=("Segoe UI", 10, "bold")
        ).pack(
            anchor="w",
            padx=20
        )


        tk.Label(
            self.menu_contenido,
            text=self.sesion.rol,
            bg="#202020",
            fg="#AFAFAF",
            font=("Segoe UI", 9)
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 20)
        )


        self.crear_boton_menu(
            "Inicio",
            self.mostrar_inicio
        )


        if self.sesion.es_superadmin():

            self.crear_menu_superadmin()

        elif self.sesion.es_docente():

            self.crear_menu_docente()


        tk.Frame(
            self.menu_contenido,
            bg="#202020",
            height=20
        ).pack(
            fill="x"
        )


        tk.Button(
            self.menu_contenido,
            text="Cerrar sesión",
            bg="#202020",
            fg="#FFFFFF",
            activebackground="#343434",
            activeforeground="#FFFFFF",
            relief="flat",
            bd=0,
            anchor="w",
            font=("Segoe UI", 10),
            cursor="hand2",
            command=self.al_cerrar_sesion
        ).pack(
            fill="x",
            padx=10,
            pady=(10, 20),
            ipady=8
        )


        self.after(
            100,
            self.actualizar_scroll
        )


    def actualizar_region_scroll(
        self,
        event=None
    ):

        self.canvas_sidebar.configure(
            scrollregion=self.canvas_sidebar.bbox(
                "all"
            )
        )


    def ajustar_ancho_menu(
        self,
        event
    ):

        self.canvas_sidebar.itemconfigure(
            self.ventana_menu,
            width=event.width
        )


    def actualizar_scroll(self):

        self.update_idletasks()

        self.canvas_sidebar.configure(
            scrollregion=self.canvas_sidebar.bbox(
                "all"
            )
        )


    def desplazar_menu(
        self,
        event
    ):

        if event.delta == 0:
            return

        pasos = int(
            -1 * (
                event.delta / 120
            )
        )

        self.canvas_sidebar.yview_scroll(
            pasos,
            "units"
        )


    def crear_menu_superadmin(self):

        self.crear_boton_menu(
            "Alumnos",
            self.mostrar_alumnos
        )

        self.crear_boton_menu(
            "Docentes",
            self.mostrar_docentes
        )

        self.crear_boton_menu(
            "Carreras",
            self.mostrar_carreras
        )

        self.crear_boton_menu(
            "Jornadas",
            self.mostrar_jornadas
        )

        self.crear_boton_menu(
            "Periodos",
            self.mostrar_periodos
        )

        self.crear_boton_menu(
            "Cursos",
            self.mostrar_cursos
        )

        self.crear_boton_menu(
            "Secciones",
            self.mostrar_secciones
        )

        self.crear_boton_menu(
            "Horarios",
            self.mostrar_horarios
        )

        self.crear_boton_menu(
            "Inscripciones",
            self.mostrar_inscripciones
        )

        self.crear_boton_menu(
            "Huellas",
            self.mostrar_huellas
        )

        self.crear_boton_menu(
            "Sesiones",
            self.mostrar_sesiones
        )

        self.crear_boton_menu(
            "Asistencia",
            self.mostrar_asistencia
        )

        self.crear_boton_menu(
            "Justificaciones",
            self.mostrar_justificaciones
        )

        self.crear_boton_menu(
            "Configuración",
            self.mostrar_configuracion
        )

        self.crear_boton_menu(
            "Puntuación",
            self.mostrar_puntuacion
        )

        self.crear_boton_menu(
            "Reportes",
            self.mostrar_reportes
        )

        self.crear_boton_menu(
            "Auditoría",
            self.mostrar_auditoria
        )


    def crear_menu_docente(self):

        self.crear_boton_menu(
            "Mis secciones",
            lambda:
                self.mostrar_pendiente(
                    "Mis secciones"
                )
        )

        self.crear_boton_menu(
            "Mis alumnos",
            self.mostrar_inscripciones
        )

        self.crear_boton_menu(
            "Horarios",
            self.mostrar_horarios
        )

        self.crear_boton_menu(
            "Sesiones",
            self.mostrar_sesiones
        )

        self.crear_boton_menu(
            "Asistencia",
            self.mostrar_asistencia
        )

        self.crear_boton_menu(
            "Justificaciones",
            self.mostrar_justificaciones
        )

        self.crear_boton_menu(
            "Puntuación",
            self.mostrar_puntuacion
        )

        self.crear_boton_menu(
            "Reportes",
            self.mostrar_reportes
        )


    def crear_boton_menu(
        self,
        texto,
        comando
    ):

        boton = tk.Button(
            self.menu_contenido,
            text=texto,
            bg="#202020",
            fg="#FFFFFF",
            activebackground="#343434",
            activeforeground="#FFFFFF",
            relief="flat",
            bd=0,
            anchor="w",
            font=("Segoe UI", 10),
            cursor="hand2",
            command=comando
        )

        boton.pack(
            fill="x",
            padx=10,
            pady=1,
            ipady=7
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
            bg="#F3F3F3"
        )

        contenedor.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=35
        )


        tk.Label(
            contenedor,
            text="Inicio",
            bg="#F3F3F3",
            fg="#202020",
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
            bg="#F3F3F3",
            fg="#404040",
            font=("Segoe UI", 14)
        ).pack(
            anchor="w",
            pady=(20, 5)
        )


        tk.Label(
            contenedor,
            text=(
                f"Rol: "
                f"{self.sesion.rol}"
            ),
            bg="#F3F3F3",
            fg="#666666",
            font=("Segoe UI", 11)
        ).pack(
            anchor="w"
        )


        if self.sesion.es_docente():

            tk.Label(
                contenedor,
                text=(
                    f"ID docente: "
                    f"{self.sesion.id_docente}"
                ),
                bg="#F3F3F3",
                fg="#666666",
                font=("Segoe UI", 11)
            ).pack(
                anchor="w",
                pady=(5, 0)
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
            bg="#F3F3F3"
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
            bg="#F3F3F3",
            fg="#202020",
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
            bg="#F3F3F3",
            fg="#666666",
            font=("Segoe UI", 11)
        ).pack(
            anchor="w",
            pady=(20, 0)
        )