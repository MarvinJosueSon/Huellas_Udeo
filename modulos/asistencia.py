import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class Asistencia(tk.Frame):

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

        self.datos_sesiones = []
        self.mapa_sesiones = {}

        self.datos_asistencias = []

        self.pack(
            fill="both",
            expand=True
        )

        self.crear_interfaz()
        self.cargar_sesiones()


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
            text="Asistencia",
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


        panel_sesion = tk.Frame(
            self,
            bg="#FFFFFF",
            highlightthickness=1,
            highlightbackground="#DDDDDD"
        )

        panel_sesion.pack(
            fill="x",
            padx=30,
            pady=(0, 15)
        )


        tk.Label(
            panel_sesion,
            text="Sesión",
            bg="#FFFFFF",
            fg="#202020",
            font=("Segoe UI", 10, "bold")
        ).pack(
            side="left",
            padx=(20, 8),
            pady=15
        )


        self.cmb_sesion = ttk.Combobox(
            panel_sesion,
            state="readonly",
            width=75
        )

        self.cmb_sesion.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 20),
            pady=15
        )

        self.cmb_sesion.bind(
            "<<ComboboxSelected>>",
            self.cambiar_sesion
        )


        panel_registro = tk.Frame(
            self,
            bg="#F3F3F3"
        )

        panel_registro.pack(
            fill="x",
            padx=30,
            pady=(0, 15)
        )


        panel_codigo = tk.Frame(
            panel_registro,
            bg="#FFFFFF",
            highlightthickness=1,
            highlightbackground="#DDDDDD"
        )

        panel_codigo.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 7)
        )


        tk.Label(
            panel_codigo,
            text="Registrar por código",
            bg="#FFFFFF",
            fg="#202020",
            font=("Segoe UI", 12, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 10)
        )


        tk.Label(
            panel_codigo,
            text="Código del alumno",
            bg="#FFFFFF",
            fg="#202020",
            font=("Segoe UI", 9)
        ).pack(
            anchor="w",
            padx=20
        )


        self.txt_codigo = ttk.Entry(
            panel_codigo
        )

        self.txt_codigo.pack(
            fill="x",
            padx=20,
            pady=(5, 10)
        )

        self.txt_codigo.bind(
            "<Return>",
            lambda event:
                self.registrar_por_codigo()
        )


        tk.Button(
            panel_codigo,
            text="Registrar asistencia",
            bg="#0078D4",
            fg="#FFFFFF",
            activebackground="#106EBE",
            activeforeground="#FFFFFF",
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            command=self.registrar_por_codigo
        ).pack(
            fill="x",
            padx=20,
            pady=(0, 15),
            ipady=5
        )


        panel_huella = tk.Frame(
            panel_registro,
            bg="#FFFFFF",
            highlightthickness=1,
            highlightbackground="#DDDDDD"
        )

        panel_huella.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(7, 0)
        )


        tk.Label(
            panel_huella,
            text="Registrar por huella",
            bg="#FFFFFF",
            fg="#202020",
            font=("Segoe UI", 12, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 10)
        )


        tk.Label(
            panel_huella,
            text="ID del template",
            bg="#FFFFFF",
            fg="#202020",
            font=("Segoe UI", 9)
        ).pack(
            anchor="w",
            padx=20
        )


        self.txt_template = ttk.Entry(
            panel_huella
        )

        self.txt_template.pack(
            fill="x",
            padx=20,
            pady=(5, 10)
        )

        self.txt_template.bind(
            "<Return>",
            lambda event:
                self.registrar_por_huella()
        )


        tk.Button(
            panel_huella,
            text="Registrar huella",
            bg="#0078D4",
            fg="#FFFFFF",
            activebackground="#106EBE",
            activeforeground="#FFFFFF",
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            command=self.registrar_por_huella
        ).pack(
            fill="x",
            padx=20,
            pady=(0, 15),
            ipady=5
        )


        panel_filtros = tk.Frame(
            self,
            bg="#F3F3F3"
        )

        panel_filtros.pack(
            fill="x",
            padx=30,
            pady=(0, 10)
        )


        tk.Label(
            panel_filtros,
            text="Buscar:",
            bg="#F3F3F3",
            fg="#202020",
            font=("Segoe UI", 10)
        ).pack(
            side="left"
        )


        self.txt_buscar = ttk.Entry(
            panel_filtros,
            width=35
        )

        self.txt_buscar.pack(
            side="left",
            padx=(8, 20)
        )

        self.txt_buscar.bind(
            "<KeyRelease>",
            self.filtrar
        )


        tk.Label(
            panel_filtros,
            text="Estado:",
            bg="#F3F3F3",
            fg="#202020",
            font=("Segoe UI", 10)
        ).pack(
            side="left"
        )


        self.cmb_estado = ttk.Combobox(
            panel_filtros,
            state="readonly",
            values=(
                "TODOS",
                "PRESENTE",
                "TARDE",
                "AUSENTE",
                "FUERA_TIEMPO",
                "JUSTIFICADA"
            ),
            width=18
        )

        self.cmb_estado.set(
            "TODOS"
        )

        self.cmb_estado.pack(
            side="left",
            padx=8
        )

        self.cmb_estado.bind(
            "<<ComboboxSelected>>",
            self.filtrar
        )


        panel_tabla = tk.Frame(
            self,
            bg="#FFFFFF",
            highlightthickness=1,
            highlightbackground="#DDDDDD"
        )

        panel_tabla.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 15)
        )


        columnas = (
            "id",
            "codigo",
            "alumno",
            "hora",
            "estado"
        )


        self.tabla = ttk.Treeview(
            panel_tabla,
            columns=columnas,
            show="headings",
            selectmode="browse"
        )


        self.tabla.heading(
            "id",
            text="ID"
        )

        self.tabla.heading(
            "codigo",
            text="Código"
        )

        self.tabla.heading(
            "alumno",
            text="Alumno"
        )

        self.tabla.heading(
            "hora",
            text="Hora de registro"
        )

        self.tabla.heading(
            "estado",
            text="Estado"
        )


        self.tabla.column(
            "id",
            width=70,
            anchor="center"
        )

        self.tabla.column(
            "codigo",
            width=140
        )

        self.tabla.column(
            "alumno",
            width=300
        )

        self.tabla.column(
            "hora",
            width=180,
            anchor="center"
        )

        self.tabla.column(
            "estado",
            width=150,
            anchor="center"
        )


        scroll_vertical = ttk.Scrollbar(
            panel_tabla,
            orient="vertical",
            command=self.tabla.yview
        )


        self.tabla.configure(
            yscrollcommand=scroll_vertical.set
        )


        self.tabla.pack(
            side="left",
            fill="both",
            expand=True
        )

        scroll_vertical.pack(
            side="right",
            fill="y"
        )


        panel_acciones = tk.Frame(
            self,
            bg="#F3F3F3"
        )

        panel_acciones.pack(
            fill="x",
            padx=30,
            pady=(0, 20)
        )


        tk.Button(
            panel_acciones,
            text="Cambiar estado manualmente",
            bg="#E5E5E5",
            fg="#202020",
            activebackground="#D5D5D5",
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 10),
            command=self.cambiar_estado_manual
        ).pack(
            side="left",
            ipadx=15,
            ipady=5
        )


    def cargar_sesiones(self):

        id_anterior = (
            self.obtener_id_sesion()
        )


        resultados = (
            self.database
            .llamar_procedimiento(
                "ListarSesionesDocente"
            )
        )


        if resultados is None:

            messagebox.showerror(
                "Asistencia",
                (
                    "No se pudieron cargar "
                    "las sesiones.\n\n"
                    + str(
                        self.database
                        .obtener_ultimo_error()
                    )
                )
            )

            return


        self.datos_sesiones = []


        if resultados:

            self.datos_sesiones = (
                resultados[0]
            )


        valores = []

        self.mapa_sesiones = {}


        for sesion in self.datos_sesiones:

            texto = (
                f"{sesion['id']} - "
                f"{sesion['curso']} - "
                f"Sección {sesion['seccion']} - "
                f"{self.formatear_fecha(sesion['fecha'])} "
                f"{self.formatear_hora(sesion['hora_inicio'])} "
                f"({sesion['estado']})"
            )

            valores.append(
                texto
            )

            self.mapa_sesiones[
                texto
            ] = sesion["id"]


        self.cmb_sesion[
            "values"
        ] = valores


        if not valores:

            self.cmb_sesion.set(
                ""
            )

            self.datos_asistencias = []

            self.mostrar_datos(
                []
            )

            return


        seleccionado = False


        if id_anterior is not None:

            for texto, identificador in (
                self.mapa_sesiones.items()
            ):

                if identificador == id_anterior:

                    self.cmb_sesion.set(
                        texto
                    )

                    seleccionado = True

                    break


        if not seleccionado:

            abierta = None


            for texto in valores:

                if "(ABIERTA)" in texto:

                    abierta = texto

                    break


            if abierta is not None:

                self.cmb_sesion.set(
                    abierta
                )

            else:

                self.cmb_sesion.current(
                    0
                )


        self.cargar_asistencias()


    def obtener_id_sesion(self):

        if not hasattr(
            self,
            "cmb_sesion"
        ):

            return None


        return self.mapa_sesiones.get(
            self.cmb_sesion.get()
        )


    def cambiar_sesion(
        self,
        event=None
    ):

        self.txt_buscar.delete(
            0,
            tk.END
        )

        self.cmb_estado.set(
            "TODOS"
        )

        self.cargar_asistencias()


    def obtener_estado_sesion_actual(self):

        id_sesion = (
            self.obtener_id_sesion()
        )


        if id_sesion is None:

            return None


        for sesion in self.datos_sesiones:

            if sesion["id"] == id_sesion:

                return sesion["estado"]


        return None


    def cargar_asistencias(self):

        id_sesion = (
            self.obtener_id_sesion()
        )


        if id_sesion is None:

            self.datos_asistencias = []

            self.mostrar_datos(
                []
            )

            return


        resultados = (
            self.database
            .consultar(
                """
                SELECT
                    id_asistencia,
                    id_alumno,
                    codigo,
                    alumno,
                    hora_registro,
                    estado
                FROM vista_asistencia_alumnos
                WHERE id_sesion = %s
                ORDER BY alumno
                """,
                (
                    id_sesion,
                )
            )
        )


        if (
            not resultados
            and self.database.obtener_ultimo_error()
        ):

            messagebox.showerror(
                "Asistencia",
                (
                    "No se pudieron cargar "
                    "las asistencias.\n\n"
                    + str(
                        self.database
                        .obtener_ultimo_error()
                    )
                )
            )

            return


        self.datos_asistencias = resultados


        self.mostrar_datos(
            self.datos_asistencias
        )


    def mostrar_datos(
        self,
        datos
    ):

        for fila in (
            self.tabla.get_children()
        ):

            self.tabla.delete(
                fila
            )


        for asistencia in datos:

            self.tabla.insert(
                "",
                tk.END,
                values=(
                    asistencia[
                        "id_asistencia"
                    ],
                    asistencia[
                        "codigo"
                    ],
                    asistencia[
                        "alumno"
                    ],
                    self.formatear_fecha_hora(
                        asistencia[
                            "hora_registro"
                        ]
                    ),
                    asistencia[
                        "estado"
                    ]
                )
            )


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


    def formatear_hora(
        self,
        hora
    ):

        if hora is None:

            return ""


        if hasattr(
            hora,
            "total_seconds"
        ):

            segundos = int(
                hora.total_seconds()
            )

            horas = (
                segundos // 3600
            )

            minutos = (
                segundos % 3600
            ) // 60

            return (
                f"{horas:02d}:"
                f"{minutos:02d}"
            )


        texto = str(
            hora
        )


        if len(texto) >= 5:

            return texto[:5]


        return texto


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


    def filtrar(
        self,
        event=None
    ):

        texto = (
            self.txt_buscar
            .get()
            .strip()
            .lower()
        )

        estado = (
            self.cmb_estado
            .get()
        )


        filtradas = []


        for asistencia in self.datos_asistencias:

            codigo = str(
                asistencia["codigo"]
            ).lower()

            alumno = str(
                asistencia["alumno"]
            ).lower()


            coincide_texto = (
                texto == ""
                or texto in codigo
                or texto in alumno
            )


            coincide_estado = (
                estado == "TODOS"
                or asistencia["estado"]
                == estado
            )


            if (
                coincide_texto
                and coincide_estado
            ):

                filtradas.append(
                    asistencia
                )


        self.mostrar_datos(
            filtradas
        )


    def validar_sesion_abierta(self):

        id_sesion = (
            self.obtener_id_sesion()
        )


        if id_sesion is None:

            messagebox.showwarning(
                "Asistencia",
                "Selecciona una sesión."
            )

            return None


        estado = (
            self.obtener_estado_sesion_actual()
        )


        if estado != "ABIERTA":

            messagebox.showwarning(
                "Asistencia",
                (
                    "La sesión seleccionada "
                    "no está abierta."
                )
            )

            return None


        return id_sesion


    def registrar_por_codigo(self):

        id_sesion = (
            self.validar_sesion_abierta()
        )


        if id_sesion is None:

            return


        codigo = (
            self.txt_codigo
            .get()
            .strip()
        )


        if codigo == "":

            messagebox.showwarning(
                "Asistencia",
                (
                    "Ingresa el código "
                    "del alumno."
                )
            )

            self.txt_codigo.focus_set()

            return


        resultados = (
            self.database
            .llamar_procedimiento(
                "BuscarAlumnoPorCodigo",
                (
                    codigo,
                )
            )
        )


        if resultados is None:

            messagebox.showerror(
                "Asistencia",
                (
                    "No se pudo buscar "
                    "el alumno.\n\n"
                    + str(
                        self.database
                        .obtener_ultimo_error()
                    )
                )
            )

            return


        if (
            not resultados
            or not resultados[0]
        ):

            messagebox.showwarning(
                "Asistencia",
                (
                    "No se encontró un alumno "
                    "con ese código."
                )
            )

            return


        alumno = resultados[0][0]


        self.registrar_asistencia(
            alumno["id"],
            (
                f"{alumno['nombre']} "
                f"{alumno['apellido']}"
            )
        )


        self.txt_codigo.delete(
            0,
            tk.END
        )

        self.txt_codigo.focus_set()


    def registrar_por_huella(self):

        id_sesion = (
            self.validar_sesion_abierta()
        )


        if id_sesion is None:

            return


        template = (
            self.txt_template
            .get()
            .strip()
        )


        if template == "":

            messagebox.showwarning(
                "Asistencia",
                (
                    "Ingresa el ID "
                    "del template."
                )
            )

            self.txt_template.focus_set()

            return


        try:

            id_template = int(
                template
            )

        except ValueError:

            messagebox.showwarning(
                "Asistencia",
                (
                    "El ID del template "
                    "debe ser un número entero."
                )
            )

            return


        resultados = (
            self.database
            .llamar_procedimiento(
                "BuscarAlumnoPorHuella",
                (
                    id_template,
                )
            )
        )


        if resultados is None:

            messagebox.showerror(
                "Asistencia",
                (
                    "No se pudo consultar "
                    "la huella.\n\n"
                    + str(
                        self.database
                        .obtener_ultimo_error()
                    )
                )
            )

            return


        if (
            not resultados
            or not resultados[0]
        ):

            messagebox.showwarning(
                "Asistencia",
                (
                    "No existe una huella activa "
                    "con ese template."
                )
            )

            return


        alumno = resultados[0][0]


        self.registrar_asistencia(
            alumno["id"],
            (
                f"{alumno['nombre']} "
                f"{alumno['apellido']}"
            )
        )


        self.txt_template.delete(
            0,
            tk.END
        )

        self.txt_template.focus_set()


    def registrar_asistencia(
        self,
        id_alumno,
        nombre_alumno
    ):

        id_sesion = (
            self.obtener_id_sesion()
        )


        if id_sesion is None:

            return


        fecha_hora = (
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )


        resultado = (
            self.database
            .llamar_procedimiento(
                "RegistrarAsistencia",
                (
                    id_alumno,
                    id_sesion,
                    fecha_hora
                )
            )
        )


        if resultado is None:

            messagebox.showerror(
                "Asistencia",
                (
                    "No se pudo registrar "
                    "la asistencia.\n\n"
                    + str(
                        self.database
                        .obtener_ultimo_error()
                    )
                )
            )

            return


        estado = ""


        if resultado and resultado[0]:

            registro = resultado[0][0]

            estado = str(
                registro.get(
                    "estado",
                    ""
                )
            )


        mensaje = (
            "Asistencia registrada "
            "correctamente.\n\n"
            f"Alumno: {nombre_alumno}"
        )


        if estado != "":

            mensaje += (
                f"\nEstado: {estado}"
            )


        messagebox.showinfo(
            "Asistencia",
            mensaje
        )


        self.cargar_asistencias()


    def obtener_asistencia_seleccionada(
        self
    ):

        seleccion = (
            self.tabla.selection()
        )


        if not seleccion:

            messagebox.showwarning(
                "Asistencia",
                (
                    "Selecciona un registro "
                    "de asistencia."
                )
            )

            return None


        valores = self.tabla.item(
            seleccion[0],
            "values"
        )


        return {
            "id_asistencia": int(
                valores[0]
            ),
            "codigo": valores[1],
            "alumno": valores[2],
            "hora": valores[3],
            "estado": valores[4]
        }


    def cambiar_estado_manual(self):

        asistencia = (
            self.obtener_asistencia_seleccionada()
        )


        if asistencia is None:

            return


        ventana = tk.Toplevel(
            self
        )

        ventana.title(
            "Cambiar asistencia"
        )

        ventana.geometry(
            "440x330"
        )

        ventana.resizable(
            False,
            False
        )

        ventana.transient(
            self.winfo_toplevel()
        )

        ventana.grab_set()


        tk.Label(
            ventana,
            text="Cambiar asistencia",
            font=("Segoe UI", 15, "bold")
        ).pack(
            pady=(20, 5)
        )


        tk.Label(
            ventana,
            text=(
                f"{asistencia['codigo']} - "
                f"{asistencia['alumno']}"
            ),
            font=("Segoe UI", 10)
        ).pack(
            pady=(0, 15)
        )


        tk.Label(
            ventana,
            text="Nuevo estado",
            font=("Segoe UI", 9)
        ).pack()


        cmb_nuevo_estado = ttk.Combobox(
            ventana,
            state="readonly",
            values=(
                "PRESENTE",
                "TARDE",
                "AUSENTE",
                "FUERA_TIEMPO"
            ),
            width=25
        )

        cmb_nuevo_estado.set(
            asistencia["estado"]
            if asistencia["estado"]
            in (
                "PRESENTE",
                "TARDE",
                "AUSENTE",
                "FUERA_TIEMPO"
            )
            else ""
        )

        cmb_nuevo_estado.pack(
            pady=(5, 15)
        )


        tk.Label(
            ventana,
            text="Motivo del cambio",
            font=("Segoe UI", 9)
        ).pack()


        txt_motivo = tk.Text(
            ventana,
            height=4,
            width=45,
            font=("Segoe UI", 9)
        )

        txt_motivo.pack(
            pady=(5, 15)
        )


        def guardar_cambio():

            nuevo_estado = (
                cmb_nuevo_estado
                .get()
                .strip()
            )


            if nuevo_estado == "":

                messagebox.showwarning(
                    "Asistencia",
                    (
                        "Selecciona el "
                        "nuevo estado."
                    ),
                    parent=ventana
                )

                return


            motivo = (
                txt_motivo
                .get(
                    "1.0",
                    tk.END
                )
                .strip()
            )


            if motivo == "":

                messagebox.showwarning(
                    "Asistencia",
                    (
                        "Debes indicar el motivo "
                        "del cambio."
                    ),
                    parent=ventana
                )

                return


            resultado = (
                self.database
                .llamar_procedimiento(
                    "CambiarAsistenciaManual",
                    (
                        asistencia[
                            "id_asistencia"
                        ],
                        nuevo_estado,
                        motivo
                    )
                )
            )


            if resultado is None:

                messagebox.showerror(
                    "Asistencia",
                    (
                        "No se pudo modificar "
                        "la asistencia.\n\n"
                        + str(
                            self.database
                            .obtener_ultimo_error()
                        )
                    ),
                    parent=ventana
                )

                return


            messagebox.showinfo(
                "Asistencia",
                (
                    "Asistencia modificada "
                    "correctamente."
                ),
                parent=ventana
            )


            ventana.destroy()

            self.cargar_asistencias()


        tk.Button(
            ventana,
            text="Guardar cambio",
            bg="#0078D4",
            fg="#FFFFFF",
            activebackground="#106EBE",
            activeforeground="#FFFFFF",
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            command=guardar_cambio
        ).pack(
            ipadx=20,
            ipady=5
        )


    def actualizar(self):

        self.cargar_sesiones()