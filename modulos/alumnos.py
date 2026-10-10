import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class Alumnos(tk.Frame):

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

        self.id_seleccionado = None
        self.datos_alumnos = []

        self.carreras = []
        self.mapa_carreras = {}

        self.pack(
            fill="both",
            expand=True
        )

        self.crear_interfaz()
        self.cargar_carreras()
        self.cargar_alumnos()
        self.nuevo()


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
            text="Alumnos",
            bg="#F3F3F3",
            fg="#202020",
            font=("Segoe UI", 24, "bold")
        ).pack(
            side="left"
        )


        tk.Button(
            encabezado,
            text="+ Nuevo alumno",
            bg="#0078D4",
            fg="#FFFFFF",
            activebackground="#106EBE",
            activeforeground="#FFFFFF",
            relief="flat",
            bd=0,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            command=self.nuevo
        ).pack(
            side="right",
            ipadx=15,
            ipady=6
        )


        panel_busqueda = tk.Frame(
            self,
            bg="#F3F3F3"
        )

        panel_busqueda.pack(
            fill="x",
            padx=30,
            pady=(0, 10)
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


        self.txt_buscar = ttk.Entry(
            panel_busqueda,
            width=35
        )

        self.txt_buscar.pack(
            side="left",
            padx=(8, 20)
        )

        self.txt_buscar.bind(
            "<Return>",
            self.buscar
        )


        tk.Button(
            panel_busqueda,
            text="Buscar",
            bg="#E5E5E5",
            fg="#202020",
            activebackground="#D5D5D5",
            relief="flat",
            bd=0,
            font=("Segoe UI", 9),
            cursor="hand2",
            command=self.buscar
        ).pack(
            side="left",
            ipadx=12,
            ipady=4
        )


        tk.Button(
            panel_busqueda,
            text="Mostrar todos",
            bg="#E5E5E5",
            fg="#202020",
            activebackground="#D5D5D5",
            relief="flat",
            bd=0,
            font=("Segoe UI", 9),
            cursor="hand2",
            command=self.mostrar_todos
        ).pack(
            side="left",
            padx=8,
            ipadx=12,
            ipady=4
        )


        cuerpo = tk.Frame(
            self,
            bg="#F3F3F3"
        )

        cuerpo.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 15)
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
            "nombre",
            "apellido",
            "edad",
            "correo",
            "carrera",
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
            "nombre",
            text="Nombre"
        )

        self.tabla.heading(
            "apellido",
            text="Apellido"
        )

        self.tabla.heading(
            "edad",
            text="Edad"
        )

        self.tabla.heading(
            "correo",
            text="Correo"
        )

        self.tabla.heading(
            "carrera",
            text="Carrera"
        )

        self.tabla.heading(
            "estado",
            text="Estado"
        )


        self.tabla.column(
            "id",
            width=50,
            anchor="center"
        )

        self.tabla.column(
            "codigo",
            width=110
        )

        self.tabla.column(
            "nombre",
            width=130
        )

        self.tabla.column(
            "apellido",
            width=130
        )

        self.tabla.column(
            "edad",
            width=60,
            anchor="center"
        )

        self.tabla.column(
            "correo",
            width=220
        )

        self.tabla.column(
            "carrera",
            width=180
        )

        self.tabla.column(
            "estado",
            width=90,
            anchor="center"
        )


        scroll_vertical = ttk.Scrollbar(
            panel_tabla,
            orient="vertical",
            command=self.tabla.yview
        )


        scroll_horizontal = ttk.Scrollbar(
            panel_tabla,
            orient="horizontal",
            command=self.tabla.xview
        )


        self.tabla.configure(
            yscrollcommand=scroll_vertical.set,
            xscrollcommand=scroll_horizontal.set
        )


        self.tabla.grid(
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


        self.tabla.bind(
            "<Double-1>",
            self.editar
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


        self.lbl_titulo = tk.Label(
            panel_formulario,
            text="Nuevo alumno",
            bg="#FFFFFF",
            fg="#202020",
            font=("Segoe UI", 15, "bold")
        )

        self.lbl_titulo.pack(
            anchor="w",
            padx=20,
            pady=(20, 18)
        )


        self.crear_etiqueta(
            panel_formulario,
            "Código"
        )

        self.txt_codigo = ttk.Entry(
            panel_formulario
        )

        self.txt_codigo.pack(
            fill="x",
            padx=20,
            pady=(0, 12)
        )


        self.crear_etiqueta(
            panel_formulario,
            "Nombre"
        )

        self.txt_nombre = ttk.Entry(
            panel_formulario
        )

        self.txt_nombre.pack(
            fill="x",
            padx=20,
            pady=(0, 12)
        )


        self.crear_etiqueta(
            panel_formulario,
            "Apellido"
        )

        self.txt_apellido = ttk.Entry(
            panel_formulario
        )

        self.txt_apellido.pack(
            fill="x",
            padx=20,
            pady=(0, 12)
        )


        self.crear_etiqueta(
            panel_formulario,
            "Fecha de nacimiento (AAAA-MM-DD)"
        )

        self.txt_fecha_nacimiento = ttk.Entry(
            panel_formulario
        )

        self.txt_fecha_nacimiento.pack(
            fill="x",
            padx=20,
            pady=(0, 12)
        )


        self.crear_etiqueta(
            panel_formulario,
            "Carrera"
        )

        self.cmb_carrera = ttk.Combobox(
            panel_formulario,
            state="readonly"
        )

        self.cmb_carrera.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )


        self.btn_guardar = tk.Button(
            panel_formulario,
            text="Guardar alumno",
            bg="#0078D4",
            fg="#FFFFFF",
            activebackground="#106EBE",
            activeforeground="#FFFFFF",
            relief="flat",
            bd=0,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            command=self.guardar
        )

        self.btn_guardar.pack(
            fill="x",
            padx=20,
            pady=(0, 8),
            ipady=6
        )


        tk.Button(
            panel_formulario,
            text="Cancelar",
            bg="#E5E5E5",
            fg="#202020",
            activebackground="#D5D5D5",
            relief="flat",
            bd=0,
            font=("Segoe UI", 10),
            cursor="hand2",
            command=self.nuevo
        ).pack(
            fill="x",
            padx=20,
            ipady=5
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
            text="Editar",
            bg="#E5E5E5",
            fg="#202020",
            activebackground="#D5D5D5",
            relief="flat",
            bd=0,
            font=("Segoe UI", 10),
            cursor="hand2",
            command=self.editar
        ).pack(
            side="left",
            ipadx=15,
            ipady=5
        )


        tk.Button(
            panel_acciones,
            text="Inactivar",
            bg="#E5E5E5",
            fg="#202020",
            activebackground="#D5D5D5",
            relief="flat",
            bd=0,
            font=("Segoe UI", 10),
            cursor="hand2",
            command=self.inactivar
        ).pack(
            side="left",
            padx=10,
            ipadx=15,
            ipady=5
        )


        tk.Button(
            panel_acciones,
            text="Actualizar",
            bg="#E5E5E5",
            fg="#202020",
            activebackground="#D5D5D5",
            relief="flat",
            bd=0,
            font=("Segoe UI", 10),
            cursor="hand2",
            command=self.actualizar
        ).pack(
            side="left",
            ipadx=15,
            ipady=5
        )


    def crear_etiqueta(
        self,
        padre,
        texto
    ):

        tk.Label(
            padre,
            text=texto,
            bg="#FFFFFF",
            fg="#202020",
            font=("Segoe UI", 9)
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 5)
        )


    def cargar_carreras(self):

        resultados = (
            self.database
            .llamar_procedimiento(
                "ListarCarreras"
            )
        )


        if resultados is None:

            messagebox.showerror(
                "Alumnos",
                (
                    "No se pudieron cargar "
                    "las carreras.\n\n"
                    + str(
                        self.database
                        .obtener_ultimo_error()
                    )
                )
            )

            return


        self.carreras = []

        if resultados:

            self.carreras = resultados[0]


        nombres = []
        self.mapa_carreras = {}


        for carrera in self.carreras:

            texto = (
                f"{carrera['id']} - "
                f"{carrera['nombre']} "
                f"({carrera['estado']})"
            )

            nombres.append(
                texto
            )

            self.mapa_carreras[
                texto
            ] = carrera["id"]


        self.cmb_carrera[
            "values"
        ] = nombres


    def cargar_alumnos(self):

        self.buscar_alumnos(
            ""
        )


    def buscar_alumnos(
        self,
        texto
    ):

        resultados = (
            self.database
            .llamar_procedimiento(
                "BuscarAlumno",
                (
                    texto,
                )
            )
        )


        if resultados is None:

            messagebox.showerror(
                "Alumnos",
                (
                    "No se pudieron cargar "
                    "los alumnos.\n\n"
                    + str(
                        self.database
                        .obtener_ultimo_error()
                    )
                )
            )

            return


        self.datos_alumnos = []


        if resultados:

            self.datos_alumnos = (
                resultados[0]
            )


        self.mostrar_datos(
            self.datos_alumnos
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


        for alumno in datos:

            self.tabla.insert(
                "",
                tk.END,
                values=(
                    alumno["id"],
                    alumno["codigo"],
                    alumno["nombre"],
                    alumno["apellido"],
                    alumno["edad"],
                    alumno["correo"],
                    alumno["carrera"],
                    alumno["estado"]
                )
            )


    def buscar(
        self,
        event=None
    ):

        texto = (
            self.txt_buscar
            .get()
            .strip()
        )


        self.buscar_alumnos(
            texto
        )


    def mostrar_todos(self):

        self.txt_buscar.delete(
            0,
            tk.END
        )

        self.buscar_alumnos(
            ""
        )


    def obtener_seleccion(self):

        seleccion = (
            self.tabla.selection()
        )


        if not seleccion:

            messagebox.showwarning(
                "Alumnos",
                "Selecciona un alumno."
            )

            return None


        valores = self.tabla.item(
            seleccion[0],
            "values"
        )


        return {
            "id": int(valores[0]),
            "codigo": valores[1],
            "nombre": valores[2],
            "apellido": valores[3],
            "edad": valores[4],
            "correo": valores[5],
            "carrera": valores[6],
            "estado": valores[7]
        }


    def obtener_detalle_alumno(
        self,
        id_alumno
    ):

        resultado = (
            self.database
            .consultar_uno(
                """
                SELECT
                    id,
                    id_carrera,
                    codigo,
                    nombre,
                    apellido,
                    fecha_nacimiento,
                    correo,
                    estado
                FROM alumnos
                WHERE id = %s
                """,
                (
                    id_alumno,
                )
            )
        )


        if resultado is None:

            messagebox.showerror(
                "Alumnos",
                (
                    "No se pudo obtener "
                    "la información del alumno.\n\n"
                    + str(
                        self.database
                        .obtener_ultimo_error()
                        or ""
                    )
                )
            )

            return None


        return resultado


    def nuevo(self):

        self.id_seleccionado = None


        self.lbl_titulo.config(
            text="Nuevo alumno"
        )


        self.btn_guardar.config(
            text="Guardar alumno"
        )


        self.txt_codigo.delete(
            0,
            tk.END
        )

        self.txt_nombre.delete(
            0,
            tk.END
        )

        self.txt_apellido.delete(
            0,
            tk.END
        )

        self.txt_fecha_nacimiento.delete(
            0,
            tk.END
        )

        self.cmb_carrera.set(
            ""
        )


        for fila in (
            self.tabla.selection()
        ):

            self.tabla.selection_remove(
                fila
            )


        self.txt_codigo.focus_set()


    def editar(
        self,
        event=None
    ):

        alumno = (
            self.obtener_seleccion()
        )


        if alumno is None:

            return


        detalle = (
            self.obtener_detalle_alumno(
                alumno["id"]
            )
        )


        if detalle is None:

            return


        self.id_seleccionado = (
            detalle["id"]
        )


        self.txt_codigo.delete(
            0,
            tk.END
        )

        self.txt_codigo.insert(
            0,
            detalle["codigo"]
        )


        self.txt_nombre.delete(
            0,
            tk.END
        )

        self.txt_nombre.insert(
            0,
            detalle["nombre"]
        )


        self.txt_apellido.delete(
            0,
            tk.END
        )

        self.txt_apellido.insert(
            0,
            detalle["apellido"]
        )


        self.txt_fecha_nacimiento.delete(
            0,
            tk.END
        )


        fecha = detalle[
            "fecha_nacimiento"
        ]

        try:

            fecha = fecha.strftime(
                "%Y-%m-%d"
            )

        except AttributeError:

            fecha = str(fecha)


        self.txt_fecha_nacimiento.insert(
            0,
            fecha
        )


        self.seleccionar_carrera(
            detalle["id_carrera"]
        )


        self.lbl_titulo.config(
            text="Editar alumno"
        )


        self.btn_guardar.config(
            text="Guardar cambios"
        )


        self.txt_codigo.focus_set()


    def seleccionar_carrera(
        self,
        id_carrera
    ):

        for texto, identificador in (
            self.mapa_carreras.items()
        ):

            if identificador == id_carrera:

                self.cmb_carrera.set(
                    texto
                )

                return


        self.cmb_carrera.set(
            ""
        )


    def validar_formulario(self):

        codigo = (
            self.txt_codigo
            .get()
            .strip()
        )

        nombre = (
            self.txt_nombre
            .get()
            .strip()
        )

        apellido = (
            self.txt_apellido
            .get()
            .strip()
        )

        fecha_nacimiento = (
            self.txt_fecha_nacimiento
            .get()
            .strip()
        )

        carrera_texto = (
            self.cmb_carrera
            .get()
            .strip()
        )


        if codigo == "":

            messagebox.showwarning(
                "Alumnos",
                "Ingresa el código del alumno."
            )

            return None


        if nombre == "":

            messagebox.showwarning(
                "Alumnos",
                "Ingresa el nombre del alumno."
            )

            return None


        if apellido == "":

            messagebox.showwarning(
                "Alumnos",
                "Ingresa el apellido del alumno."
            )

            return None


        if carrera_texto == "":

            messagebox.showwarning(
                "Alumnos",
                "Selecciona una carrera."
            )

            return None


        if carrera_texto not in self.mapa_carreras:

            messagebox.showwarning(
                "Alumnos",
                "La carrera seleccionada no es válida."
            )

            return None


        try:

            datetime.strptime(
                fecha_nacimiento,
                "%Y-%m-%d"
            )

        except ValueError:

            messagebox.showwarning(
                "Alumnos",
                (
                    "La fecha de nacimiento debe "
                    "usar el formato AAAA-MM-DD."
                )
            )

            return None


        return {
            "id_carrera": self.mapa_carreras[
                carrera_texto
            ],
            "codigo": codigo,
            "nombre": nombre,
            "apellido": apellido,
            "fecha_nacimiento": fecha_nacimiento
        }


    def guardar(self):

        datos = (
            self.validar_formulario()
        )


        if datos is None:

            return


        if self.id_seleccionado is None:

            resultado = (
                self.database
                .llamar_procedimiento(
                    "CrearAlumno",
                    (
                        datos["id_carrera"],
                        datos["codigo"],
                        datos["nombre"],
                        datos["apellido"],
                        datos["fecha_nacimiento"]
                    )
                )
            )


            if resultado is None:

                messagebox.showerror(
                    "Alumnos",
                    (
                        "No se pudo crear "
                        "el alumno.\n\n"
                        + str(
                            self.database
                            .obtener_ultimo_error()
                        )
                    )
                )

                return


            mensaje = (
                "Alumno creado correctamente."
            )


            if resultado:

                if resultado[0]:

                    alumno = resultado[0][0]

                    if "correo" in alumno:

                        mensaje += (
                            "\n\nCorreo generado:\n"
                            + str(
                                alumno["correo"]
                            )
                        )


            messagebox.showinfo(
                "Alumnos",
                mensaje
            )


        else:

            resultado = (
                self.database
                .llamar_procedimiento(
                    "ModificarAlumno",
                    (
                        self.id_seleccionado,
                        datos["id_carrera"],
                        datos["codigo"],
                        datos["nombre"],
                        datos["apellido"],
                        datos["fecha_nacimiento"]
                    )
                )
            )


            if resultado is None:

                messagebox.showerror(
                    "Alumnos",
                    (
                        "No se pudo modificar "
                        "el alumno.\n\n"
                        + str(
                            self.database
                            .obtener_ultimo_error()
                        )
                    )
                )

                return


            messagebox.showinfo(
                "Alumnos",
                (
                    "Alumno modificado "
                    "correctamente."
                )
            )


        self.cargar_alumnos()

        self.nuevo()


    def inactivar(self):

        alumno = (
            self.obtener_seleccion()
        )


        if alumno is None:

            return


        if alumno["estado"] == "INACTIVO":

            messagebox.showinfo(
                "Alumnos",
                (
                    "El alumno ya se encuentra "
                    "inactivo."
                )
            )

            return


        confirmar = (
            messagebox.askyesno(
                "Inactivar alumno",
                (
                    "¿Deseas inactivar al alumno?\n\n"
                    f"{alumno['codigo']} - "
                    f"{alumno['nombre']} "
                    f"{alumno['apellido']}"
                )
            )
        )


        if not confirmar:

            return


        resultado = (
            self.database
            .llamar_procedimiento(
                "InactivarAlumno",
                (
                    alumno["id"],
                )
            )
        )


        if resultado is None:

            messagebox.showerror(
                "Alumnos",
                (
                    "No se pudo inactivar "
                    "el alumno.\n\n"
                    + str(
                        self.database
                        .obtener_ultimo_error()
                    )
                )
            )

            return


        messagebox.showinfo(
            "Alumnos",
            "Alumno inactivado correctamente."
        )


        self.cargar_alumnos()

        self.nuevo()


    def actualizar(self):

        self.cargar_carreras()
        self.cargar_alumnos()
        self.nuevo()