import tkinter as tk
from tkinter import ttk, messagebox


class Justificaciones(tk.Frame):

    def __init__(
        self,
        master,
        database
    ):
        super().__init__(
            master,
            bg="#F3F3F3"
        )

        self.database = database

        self.datos_ausencias = []
        self.datos_pendientes = []
        self.ids_sesiones_permitidas = []

        self.pack(
            fill="both",
            expand=True
        )

        self.crear_interfaz()
        self.actualizar()


    def crear_interfaz(self):

        encabezado = tk.Frame(
            self,
            bg="#F3F3F3"
        )

        encabezado.pack(
            fill="x",
            padx=30,
            pady=(25, 15)
        )


        tk.Label(
            encabezado,
            text="Justificaciones",
            bg="#F3F3F3",
            fg="#202020",
            font=("Segoe UI", 24, "bold")
        ).pack(
            side="left"
        )


        tk.Button(
            encabezado,
            text="Actualizar",
            bg="#E5E5E5",
            fg="#202020",
            activebackground="#D5D5D5",
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 9),
            command=self.actualizar
        ).pack(
            side="right",
            ipadx=12,
            ipady=4
        )


        self.notebook = ttk.Notebook(
            self
        )

        self.notebook.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 20)
        )


        self.tab_registrar = tk.Frame(
            self.notebook,
            bg="#F3F3F3"
        )

        self.tab_pendientes = tk.Frame(
            self.notebook,
            bg="#F3F3F3"
        )


        self.notebook.add(
            self.tab_registrar,
            text="Registrar justificación"
        )

        self.notebook.add(
            self.tab_pendientes,
            text="Pendientes"
        )


        self.crear_tab_registrar()
        self.crear_tab_pendientes()


    def crear_tab_registrar(self):

        panel_busqueda = tk.Frame(
            self.tab_registrar,
            bg="#F3F3F3"
        )

        panel_busqueda.pack(
            fill="x",
            pady=(15, 10)
        )


        tk.Label(
            panel_busqueda,
            text="Buscar ausencia:",
            bg="#F3F3F3",
            fg="#202020",
            font=("Segoe UI", 10)
        ).pack(
            side="left"
        )


        self.txt_buscar_ausencia = ttk.Entry(
            panel_busqueda,
            width=35
        )

        self.txt_buscar_ausencia.pack(
            side="left",
            padx=8
        )

        self.txt_buscar_ausencia.bind(
            "<KeyRelease>",
            self.filtrar_ausencias
        )


        cuerpo = tk.Frame(
            self.tab_registrar,
            bg="#F3F3F3"
        )

        cuerpo.pack(
            fill="both",
            expand=True
        )


        cuerpo.grid_rowconfigure(
            0,
            weight=1
        )

        cuerpo.grid_columnconfigure(
            0,
            weight=1
        )

        cuerpo.grid_columnconfigure(
            1,
            weight=0
        )


        panel_tabla = tk.Frame(
            cuerpo,
            bg="#FFFFFF",
            highlightthickness=1,
            highlightbackground="#DDDDDD"
        )

        panel_tabla.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 10)
        )


        columnas = (
            "id",
            "codigo",
            "alumno",
            "curso",
            "seccion",
            "fecha"
        )


        self.tabla_ausencias = ttk.Treeview(
            panel_tabla,
            columns=columnas,
            show="headings",
            selectmode="browse"
        )


        self.tabla_ausencias.heading(
            "id",
            text="ID"
        )

        self.tabla_ausencias.heading(
            "codigo",
            text="Código"
        )

        self.tabla_ausencias.heading(
            "alumno",
            text="Alumno"
        )

        self.tabla_ausencias.heading(
            "curso",
            text="Curso"
        )

        self.tabla_ausencias.heading(
            "seccion",
            text="Sección"
        )

        self.tabla_ausencias.heading(
            "fecha",
            text="Fecha"
        )


        self.tabla_ausencias.column(
            "id",
            width=60,
            anchor="center"
        )

        self.tabla_ausencias.column(
            "codigo",
            width=120
        )

        self.tabla_ausencias.column(
            "alumno",
            width=220
        )

        self.tabla_ausencias.column(
            "curso",
            width=200
        )

        self.tabla_ausencias.column(
            "seccion",
            width=80,
            anchor="center"
        )

        self.tabla_ausencias.column(
            "fecha",
            width=110,
            anchor="center"
        )


        scroll = ttk.Scrollbar(
            panel_tabla,
            orient="vertical",
            command=self.tabla_ausencias.yview
        )

        self.tabla_ausencias.configure(
            yscrollcommand=scroll.set
        )


        self.tabla_ausencias.pack(
            side="left",
            fill="both",
            expand=True
        )

        scroll.pack(
            side="right",
            fill="y"
        )


        panel_formulario = tk.Frame(
            cuerpo,
            bg="#FFFFFF",
            width=360,
            highlightthickness=1,
            highlightbackground="#DDDDDD"
        )

        panel_formulario.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        panel_formulario.grid_propagate(
            False
        )


        tk.Label(
            panel_formulario,
            text="Registrar justificación",
            bg="#FFFFFF",
            fg="#202020",
            font=("Segoe UI", 15, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 15)
        )


        tk.Label(
            panel_formulario,
            text=(
                "Selecciona una ausencia y "
                "escribe el motivo."
            ),
            bg="#FFFFFF",
            fg="#666666",
            wraplength=310,
            justify="left",
            font=("Segoe UI", 9)
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )


        tk.Label(
            panel_formulario,
            text="Motivo",
            bg="#FFFFFF",
            fg="#202020",
            font=("Segoe UI", 9)
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 5)
        )


        self.txt_motivo = tk.Text(
            panel_formulario,
            height=7,
            font=("Segoe UI", 9)
        )

        self.txt_motivo.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )


        tk.Button(
            panel_formulario,
            text="Registrar justificación",
            bg="#0078D4",
            fg="#FFFFFF",
            activebackground="#106EBE",
            activeforeground="#FFFFFF",
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            command=self.registrar_justificacion
        ).pack(
            fill="x",
            padx=20,
            ipady=6
        )


    def crear_tab_pendientes(self):

        panel_busqueda = tk.Frame(
            self.tab_pendientes,
            bg="#F3F3F3"
        )

        panel_busqueda.pack(
            fill="x",
            pady=(15, 10)
        )


        tk.Label(
            panel_busqueda,
            text="Buscar:",
            bg="#F3F3F3",
            fg="#202020",
            font=("Segoe UI", 10)
        ).pack(
            side="left"
        )


        self.txt_buscar_pendiente = ttk.Entry(
            panel_busqueda,
            width=35
        )

        self.txt_buscar_pendiente.pack(
            side="left",
            padx=8
        )

        self.txt_buscar_pendiente.bind(
            "<KeyRelease>",
            self.filtrar_pendientes
        )


        panel_tabla = tk.Frame(
            self.tab_pendientes,
            bg="#FFFFFF",
            highlightthickness=1,
            highlightbackground="#DDDDDD"
        )

        panel_tabla.pack(
            fill="both",
            expand=True
        )


        columnas = (
            "id",
            "codigo",
            "alumno",
            "curso",
            "seccion",
            "fecha",
            "motivo",
            "solicitud"
        )


        self.tabla_pendientes = ttk.Treeview(
            panel_tabla,
            columns=columnas,
            show="headings",
            selectmode="browse"
        )


        self.tabla_pendientes.heading(
            "id",
            text="ID"
        )

        self.tabla_pendientes.heading(
            "codigo",
            text="Código"
        )

        self.tabla_pendientes.heading(
            "alumno",
            text="Alumno"
        )

        self.tabla_pendientes.heading(
            "curso",
            text="Curso"
        )

        self.tabla_pendientes.heading(
            "seccion",
            text="Sección"
        )

        self.tabla_pendientes.heading(
            "fecha",
            text="Fecha"
        )

        self.tabla_pendientes.heading(
            "motivo",
            text="Motivo"
        )

        self.tabla_pendientes.heading(
            "solicitud",
            text="Solicitud"
        )


        self.tabla_pendientes.column(
            "id",
            width=55,
            anchor="center"
        )

        self.tabla_pendientes.column(
            "codigo",
            width=110
        )

        self.tabla_pendientes.column(
            "alumno",
            width=190
        )

        self.tabla_pendientes.column(
            "curso",
            width=170
        )

        self.tabla_pendientes.column(
            "seccion",
            width=75,
            anchor="center"
        )

        self.tabla_pendientes.column(
            "fecha",
            width=100,
            anchor="center"
        )

        self.tabla_pendientes.column(
            "motivo",
            width=260
        )

        self.tabla_pendientes.column(
            "solicitud",
            width=160
        )


        scroll_vertical = ttk.Scrollbar(
            panel_tabla,
            orient="vertical",
            command=self.tabla_pendientes.yview
        )

        scroll_horizontal = ttk.Scrollbar(
            panel_tabla,
            orient="horizontal",
            command=self.tabla_pendientes.xview
        )


        self.tabla_pendientes.configure(
            yscrollcommand=scroll_vertical.set,
            xscrollcommand=scroll_horizontal.set
        )


        self.tabla_pendientes.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        scroll_vertical.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        scroll_horizontal.grid(
            row=1,
            column=0,
            sticky="ew"
        )


        panel_tabla.grid_rowconfigure(
            0,
            weight=1
        )

        panel_tabla.grid_columnconfigure(
            0,
            weight=1
        )


        panel_acciones = tk.Frame(
            self.tab_pendientes,
            bg="#F3F3F3"
        )

        panel_acciones.pack(
            fill="x",
            pady=(10, 0)
        )


        tk.Button(
            panel_acciones,
            text="Aprobar",
            bg="#0078D4",
            fg="#FFFFFF",
            activebackground="#106EBE",
            activeforeground="#FFFFFF",
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            command=lambda:
                self.resolver_justificacion(
                    "APROBADA"
                )
        ).pack(
            side="left",
            ipadx=20,
            ipady=5
        )


        tk.Button(
            panel_acciones,
            text="Rechazar",
            bg="#E5E5E5",
            fg="#202020",
            activebackground="#D5D5D5",
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 10),
            command=lambda:
                self.resolver_justificacion(
                    "RECHAZADA"
                )
        ).pack(
            side="left",
            padx=10,
            ipadx=20,
            ipady=5
        )


    def cargar_sesiones_permitidas(self):

        resultados = (
            self.database
            .llamar_procedimiento(
                "ListarSesionesDocente"
            )
        )


        if resultados is None:

            messagebox.showerror(
                "Justificaciones",
                (
                    "No se pudieron consultar "
                    "las sesiones.\n\n"
                    + str(
                        self.database
                        .obtener_ultimo_error()
                    )
                )
            )

            self.ids_sesiones_permitidas = []

            return False


        sesiones = []

        if resultados:

            sesiones = resultados[0]


        self.ids_sesiones_permitidas = [
            sesion["id"]
            for sesion in sesiones
        ]

        return True


    def cargar_ausencias(self):

        if not self.ids_sesiones_permitidas:

            self.datos_ausencias = []

            self.mostrar_ausencias(
                []
            )

            return


        placeholders = ", ".join(
            ["%s"] *
            len(
                self.ids_sesiones_permitidas
            )
        )


        consulta = f"""
            SELECT
                v.id_asistencia,
                v.id_sesion,
                v.codigo,
                v.alumno,
                v.curso,
                v.seccion,
                v.fecha,
                v.estado
            FROM vista_asistencia_alumnos v
            LEFT JOIN justificaciones j
                ON v.id_asistencia = j.id_asistencia
            WHERE v.estado = 'AUSENTE'
              AND j.id IS NULL
              AND v.id_sesion IN ({placeholders})
            ORDER BY
                v.fecha DESC,
                v.curso,
                v.alumno
        """


        resultados = (
            self.database
            .consultar(
                consulta,
                tuple(
                    self.ids_sesiones_permitidas
                )
            )
        )


        if (
            not resultados
            and self.database.obtener_ultimo_error()
        ):

            messagebox.showerror(
                "Justificaciones",
                (
                    "No se pudieron cargar "
                    "las ausencias.\n\n"
                    + str(
                        self.database
                        .obtener_ultimo_error()
                    )
                )
            )

            return


        self.datos_ausencias = resultados


        self.mostrar_ausencias(
            self.datos_ausencias
        )


    def mostrar_ausencias(
        self,
        datos
    ):

        for fila in (
            self.tabla_ausencias
            .get_children()
        ):

            self.tabla_ausencias.delete(
                fila
            )


        for ausencia in datos:

            self.tabla_ausencias.insert(
                "",
                tk.END,
                values=(
                    ausencia[
                        "id_asistencia"
                    ],
                    ausencia[
                        "codigo"
                    ],
                    ausencia[
                        "alumno"
                    ],
                    ausencia[
                        "curso"
                    ],
                    ausencia[
                        "seccion"
                    ],
                    self.formatear_fecha(
                        ausencia[
                            "fecha"
                        ]
                    )
                )
            )


    def filtrar_ausencias(
        self,
        event=None
    ):

        texto = (
            self.txt_buscar_ausencia
            .get()
            .strip()
            .lower()
        )


        filtradas = []


        for ausencia in self.datos_ausencias:

            codigo = str(
                ausencia["codigo"]
            ).lower()

            alumno = str(
                ausencia["alumno"]
            ).lower()

            curso = str(
                ausencia["curso"]
            ).lower()

            seccion = str(
                ausencia["seccion"]
            ).lower()

            fecha = (
                self.formatear_fecha(
                    ausencia["fecha"]
                )
                .lower()
            )


            if (
                texto == ""
                or texto in codigo
                or texto in alumno
                or texto in curso
                or texto in seccion
                or texto in fecha
            ):

                filtradas.append(
                    ausencia
                )


        self.mostrar_ausencias(
            filtradas
        )


    def obtener_ausencia_seleccionada(
        self
    ):

        seleccion = (
            self.tabla_ausencias
            .selection()
        )


        if not seleccion:

            messagebox.showwarning(
                "Justificaciones",
                (
                    "Selecciona una ausencia "
                    "para justificar."
                )
            )

            return None


        valores = (
            self.tabla_ausencias
            .item(
                seleccion[0],
                "values"
            )
        )


        return {
            "id_asistencia": int(
                valores[0]
            ),
            "codigo": valores[1],
            "alumno": valores[2],
            "curso": valores[3],
            "seccion": valores[4],
            "fecha": valores[5]
        }


    def registrar_justificacion(self):

        ausencia = (
            self.obtener_ausencia_seleccionada()
        )


        if ausencia is None:

            return


        motivo = (
            self.txt_motivo
            .get(
                "1.0",
                tk.END
            )
            .strip()
        )


        if motivo == "":

            messagebox.showwarning(
                "Justificaciones",
                (
                    "Ingresa el motivo "
                    "de la justificación."
                )
            )

            return


        if len(motivo) > 255:

            messagebox.showwarning(
                "Justificaciones",
                (
                    "El motivo no puede superar "
                    "255 caracteres."
                )
            )

            return


        confirmar = (
            messagebox.askyesno(
                "Registrar justificación",
                (
                    "¿Deseas registrar la "
                    "justificación?\n\n"
                    f"{ausencia['codigo']} - "
                    f"{ausencia['alumno']}\n"
                    f"{ausencia['curso']} - "
                    f"Sección "
                    f"{ausencia['seccion']}"
                )
            )
        )


        if not confirmar:

            return


        resultado = (
            self.database
            .llamar_procedimiento(
                "RegistrarJustificacion",
                (
                    ausencia[
                        "id_asistencia"
                    ],
                    motivo
                )
            )
        )


        if resultado is None:

            messagebox.showerror(
                "Justificaciones",
                (
                    "No se pudo registrar "
                    "la justificación.\n\n"
                    + str(
                        self.database
                        .obtener_ultimo_error()
                    )
                )
            )

            return


        messagebox.showinfo(
            "Justificaciones",
            (
                "Justificación registrada "
                "correctamente."
            )
        )


        self.txt_motivo.delete(
            "1.0",
            tk.END
        )

        self.actualizar()


    def cargar_pendientes(self):

        resultados = (
            self.database
            .llamar_procedimiento(
                "ListarJustificacionesPendientes"
            )
        )


        if resultados is None:

            messagebox.showerror(
                "Justificaciones",
                (
                    "No se pudieron cargar "
                    "las justificaciones "
                    "pendientes.\n\n"
                    + str(
                        self.database
                        .obtener_ultimo_error()
                    )
                )
            )

            return


        self.datos_pendientes = []


        if resultados:

            self.datos_pendientes = (
                resultados[0]
            )


        self.mostrar_pendientes(
            self.datos_pendientes
        )


    def mostrar_pendientes(
        self,
        datos
    ):

        for fila in (
            self.tabla_pendientes
            .get_children()
        ):

            self.tabla_pendientes.delete(
                fila
            )


        for justificacion in datos:

            self.tabla_pendientes.insert(
                "",
                tk.END,
                values=(
                    justificacion[
                        "id_justificacion"
                    ],
                    justificacion[
                        "codigo"
                    ],
                    justificacion[
                        "alumno"
                    ],
                    justificacion[
                        "curso"
                    ],
                    justificacion[
                        "seccion"
                    ],
                    self.formatear_fecha(
                        justificacion[
                            "fecha"
                        ]
                    ),
                    justificacion[
                        "motivo"
                    ],
                    self.formatear_fecha_hora(
                        justificacion[
                            "fecha_solicitud"
                        ]
                    )
                )
            )


    def filtrar_pendientes(
        self,
        event=None
    ):

        texto = (
            self.txt_buscar_pendiente
            .get()
            .strip()
            .lower()
        )


        filtradas = []


        for justificacion in (
            self.datos_pendientes
        ):

            codigo = str(
                justificacion["codigo"]
            ).lower()

            alumno = str(
                justificacion["alumno"]
            ).lower()

            curso = str(
                justificacion["curso"]
            ).lower()

            seccion = str(
                justificacion["seccion"]
            ).lower()

            motivo = str(
                justificacion["motivo"]
            ).lower()


            if (
                texto == ""
                or texto in codigo
                or texto in alumno
                or texto in curso
                or texto in seccion
                or texto in motivo
            ):

                filtradas.append(
                    justificacion
                )


        self.mostrar_pendientes(
            filtradas
        )


    def obtener_pendiente_seleccionado(
        self
    ):

        seleccion = (
            self.tabla_pendientes
            .selection()
        )


        if not seleccion:

            messagebox.showwarning(
                "Justificaciones",
                (
                    "Selecciona una "
                    "justificación pendiente."
                )
            )

            return None


        valores = (
            self.tabla_pendientes
            .item(
                seleccion[0],
                "values"
            )
        )


        return {
            "id_justificacion": int(
                valores[0]
            ),
            "codigo": valores[1],
            "alumno": valores[2],
            "curso": valores[3],
            "seccion": valores[4],
            "fecha": valores[5],
            "motivo": valores[6]
        }


    def resolver_justificacion(
        self,
        estado
    ):

        justificacion = (
            self.obtener_pendiente_seleccionado()
        )


        if justificacion is None:

            return


        accion = (
            "aprobar"
            if estado == "APROBADA"
            else "rechazar"
        )


        confirmar = (
            messagebox.askyesno(
                "Resolver justificación",
                (
                    f"¿Deseas {accion} esta "
                    "justificación?\n\n"
                    f"{justificacion['codigo']} - "
                    f"{justificacion['alumno']}\n"
                    f"{justificacion['curso']} - "
                    f"Sección "
                    f"{justificacion['seccion']}\n\n"
                    f"Motivo:\n"
                    f"{justificacion['motivo']}"
                )
            )
        )


        if not confirmar:

            return


        resultado = (
            self.database
            .llamar_procedimiento(
                "AprobarJustificacion",
                (
                    justificacion[
                        "id_justificacion"
                    ],
                    estado
                )
            )
        )


        if resultado is None:

            messagebox.showerror(
                "Justificaciones",
                (
                    "No se pudo resolver "
                    "la justificación.\n\n"
                    + str(
                        self.database
                        .obtener_ultimo_error()
                    )
                )
            )

            return


        if estado == "APROBADA":

            mensaje = (
                "Justificación aprobada "
                "correctamente."
            )

        else:

            mensaje = (
                "Justificación rechazada "
                "correctamente."
            )


        messagebox.showinfo(
            "Justificaciones",
            mensaje
        )


        self.actualizar()


    def formatear_fecha(
        self,
        fecha
    ):

        if fecha is None:

            return ""


        try:

            return fecha.strftime(
                "%Y-%m-%d"
            )

        except AttributeError:

            return str(
                fecha
            )


    def formatear_fecha_hora(
        self,
        fecha
    ):

        if fecha is None:

            return ""


        try:

            return fecha.strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        except AttributeError:

            return str(
                fecha
            )


    def actualizar(self):

        if not self.cargar_sesiones_permitidas():

            return


        self.cargar_ausencias()
        self.cargar_pendientes()