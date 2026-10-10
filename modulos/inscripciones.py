import tkinter as tk
from tkinter import ttk, messagebox


class Inscripciones(tk.Frame):

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

        self.mapa_secciones = {}
        self.mapa_alumnos = {}

        self.datos_inscripciones = []
        self.datos_alumnos = []

        self.pack(
            fill="both",
            expand=True
        )

        self.crear_interfaz()

        self.cargar_alumnos()
        self.cargar_secciones()


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
            text="Inscripciones",
            bg="#F3F3F3",
            fg="#202020",
            font=("Segoe UI", 24, "bold")
        ).pack(
            side="left"
        )


        panel_seccion = tk.Frame(
            self,
            bg="#F3F3F3"
        )

        panel_seccion.pack(
            fill="x",
            padx=30,
            pady=(0, 12)
        )


        tk.Label(
            panel_seccion,
            text="Sección:",
            bg="#F3F3F3",
            fg="#202020",
            font=("Segoe UI", 10)
        ).pack(
            side="left"
        )


        self.cmb_seccion = ttk.Combobox(
            panel_seccion,
            state="readonly",
            width=65
        )

        self.cmb_seccion.pack(
            side="left",
            padx=(8, 15)
        )

        self.cmb_seccion.bind(
            "<<ComboboxSelected>>",
            self.cambiar_seccion
        )


        tk.Button(
            panel_seccion,
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
            side="left",
            ipadx=12,
            ipady=4
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
            "<KeyRelease>",
            self.filtrar
        )


        tk.Label(
            panel_busqueda,
            text="Estado:",
            bg="#F3F3F3",
            fg="#202020",
            font=("Segoe UI", 10)
        ).pack(
            side="left"
        )


        self.cmb_estado = ttk.Combobox(
            panel_busqueda,
            state="readonly",
            values=(
                "TODOS",
                "ACTIVO",
                "RETIRADO"
            ),
            width=15
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
            "id_alumno",
            "codigo",
            "nombre",
            "apellido",
            "fecha_inscripcion",
            "fecha_retiro",
            "estado"
        )


        self.tabla = ttk.Treeview(
            panel_tabla,
            columns=columnas,
            show="headings",
            selectmode="browse"
        )


        self.tabla.heading(
            "id_alumno",
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
            "fecha_inscripcion",
            text="Inscripción"
        )

        self.tabla.heading(
            "fecha_retiro",
            text="Retiro"
        )

        self.tabla.heading(
            "estado",
            text="Estado"
        )


        self.tabla.column(
            "id_alumno",
            width=55,
            anchor="center"
        )

        self.tabla.column(
            "codigo",
            width=120
        )

        self.tabla.column(
            "nombre",
            width=150
        )

        self.tabla.column(
            "apellido",
            width=150
        )

        self.tabla.column(
            "fecha_inscripcion",
            width=110,
            anchor="center"
        )

        self.tabla.column(
            "fecha_retiro",
            width=110,
            anchor="center"
        )

        self.tabla.column(
            "estado",
            width=100,
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


        panel_formulario = tk.Frame(
            cuerpo,
            bg="#FFFFFF",
            width=370,
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
            text="Inscribir alumno",
            bg="#FFFFFF",
            fg="#202020",
            font=("Segoe UI", 15, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 20)
        )


        tk.Label(
            panel_formulario,
            text="Alumno",
            bg="#FFFFFF",
            fg="#202020",
            font=("Segoe UI", 9)
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 5)
        )


        self.cmb_alumno = ttk.Combobox(
            panel_formulario,
            state="readonly"
        )

        self.cmb_alumno.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )


        tk.Label(
            panel_formulario,
            text=(
                "Solo aparecen alumnos activos que "
                "todavía no pertenecen a esta sección."
            ),
            bg="#FFFFFF",
            fg="#666666",
            justify="left",
            wraplength=320,
            font=("Segoe UI", 9)
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 20)
        )


        tk.Button(
            panel_formulario,
            text="Inscribir alumno",
            bg="#0078D4",
            fg="#FFFFFF",
            activebackground="#106EBE",
            activeforeground="#FFFFFF",
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            command=self.inscribir
        ).pack(
            fill="x",
            padx=20,
            ipady=6
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
            text="Retirar alumno",
            bg="#E5E5E5",
            fg="#202020",
            activebackground="#D5D5D5",
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 10),
            command=self.retirar
        ).pack(
            side="left",
            ipadx=15,
            ipady=5
        )


    def cargar_secciones(self):

        id_actual = (
            self.obtener_id_seccion()
        )


        resultados = (
            self.database
            .llamar_procedimiento(
                "ListarSeccionesDocente"
            )
        )


        if resultados is None:

            messagebox.showerror(
                "Inscripciones",
                (
                    "No se pudieron cargar "
                    "las secciones.\n\n"
                    + str(
                        self.database
                        .obtener_ultimo_error()
                    )
                )
            )

            return


        secciones = []

        if resultados:

            secciones = resultados[0]


        valores = []

        self.mapa_secciones = {}


        for seccion in secciones:

            texto = (
                f"{seccion['id']} - "
                f"{seccion['curso']} - "
                f"Sección {seccion['seccion']} - "
                f"{seccion['periodo']} - "
                f"{seccion['jornada']} "
                f"({seccion['estado']})"
            )

            valores.append(
                texto
            )

            self.mapa_secciones[
                texto
            ] = seccion["id"]


        self.cmb_seccion[
            "values"
        ] = valores


        if not valores:

            self.cmb_seccion.set(
                ""
            )

            self.datos_inscripciones = []

            self.mostrar_datos(
                []
            )

            self.actualizar_alumnos_disponibles()

            return


        seleccionado = False


        if id_actual is not None:

            for texto, identificador in (
                self.mapa_secciones.items()
            ):

                if identificador == id_actual:

                    self.cmb_seccion.set(
                        texto
                    )

                    seleccionado = True

                    break


        if not seleccionado:

            self.cmb_seccion.current(
                0
            )


        self.cargar_inscripciones()


    def cargar_alumnos(self):

        resultados = (
            self.database
            .consultar(
                """
                SELECT
                    id,
                    codigo,
                    nombre,
                    apellido,
                    estado
                FROM alumnos
                WHERE estado = 'ACTIVO'
                ORDER BY nombre, apellido
                """
            )
        )


        if (
            not resultados
            and self.database.obtener_ultimo_error()
        ):

            messagebox.showerror(
                "Inscripciones",
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


        self.datos_alumnos = resultados


    def obtener_id_seccion(self):

        if not hasattr(
            self,
            "cmb_seccion"
        ):

            return None


        texto = (
            self.cmb_seccion
            .get()
        )


        return self.mapa_secciones.get(
            texto
        )


    def cambiar_seccion(
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

        self.cargar_inscripciones()


    def cargar_inscripciones(self):

        id_seccion = (
            self.obtener_id_seccion()
        )


        if id_seccion is None:

            self.datos_inscripciones = []

            self.mostrar_datos(
                []
            )

            self.actualizar_alumnos_disponibles()

            return


        resultados = (
            self.database
            .llamar_procedimiento(
                "ListarAlumnosSeccion",
                (
                    id_seccion,
                )
            )
        )


        if resultados is None:

            messagebox.showerror(
                "Inscripciones",
                (
                    "No se pudieron cargar "
                    "los alumnos de la sección.\n\n"
                    + str(
                        self.database
                        .obtener_ultimo_error()
                    )
                )
            )

            return


        self.datos_inscripciones = []


        if resultados:

            self.datos_inscripciones = (
                resultados[0]
            )


        self.mostrar_datos(
            self.datos_inscripciones
        )

        self.actualizar_alumnos_disponibles()


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
                    self.formatear_fecha(
                        alumno["fecha_inscripcion"]
                    ),
                    self.formatear_fecha(
                        alumno["fecha_retiro"]
                    ),
                    alumno["estado"]
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


        filtrados = []


        for alumno in self.datos_inscripciones:

            codigo = str(
                alumno["codigo"]
            ).lower()

            nombre = str(
                alumno["nombre"]
            ).lower()

            apellido = str(
                alumno["apellido"]
            ).lower()


            coincide_texto = (
                texto == ""
                or texto in codigo
                or texto in nombre
                or texto in apellido
            )


            coincide_estado = (
                estado == "TODOS"
                or alumno["estado"] == estado
            )


            if (
                coincide_texto
                and coincide_estado
            ):

                filtrados.append(
                    alumno
                )


        self.mostrar_datos(
            filtrados
        )


    def actualizar_alumnos_disponibles(self):

        ids_inscritos = {
            alumno["id"]
            for alumno
            in self.datos_inscripciones
        }


        valores = []

        self.mapa_alumnos = {}


        for alumno in self.datos_alumnos:

            if alumno["id"] in ids_inscritos:

                continue


            texto = (
                f"{alumno['codigo']} - "
                f"{alumno['nombre']} "
                f"{alumno['apellido']}"
            )

            valores.append(
                texto
            )

            self.mapa_alumnos[
                texto
            ] = alumno["id"]


        self.cmb_alumno[
            "values"
        ] = valores


        self.cmb_alumno.set(
            ""
        )


    def inscribir(self):

        id_seccion = (
            self.obtener_id_seccion()
        )


        if id_seccion is None:

            messagebox.showwarning(
                "Inscripciones",
                "Selecciona una sección."
            )

            return


        alumno_texto = (
            self.cmb_alumno
            .get()
            .strip()
        )


        if alumno_texto not in self.mapa_alumnos:

            messagebox.showwarning(
                "Inscripciones",
                "Selecciona un alumno."
            )

            return


        id_alumno = (
            self.mapa_alumnos[
                alumno_texto
            ]
        )


        confirmar = (
            messagebox.askyesno(
                "Inscribir alumno",
                (
                    "¿Deseas inscribir al alumno "
                    "en esta sección?\n\n"
                    f"{alumno_texto}"
                )
            )
        )


        if not confirmar:

            return


        resultado = (
            self.database
            .llamar_procedimiento(
                "InscribirAlumno",
                (
                    id_alumno,
                    id_seccion
                )
            )
        )


        if resultado is None:

            messagebox.showerror(
                "Inscripciones",
                (
                    "No se pudo realizar "
                    "la inscripción.\n\n"
                    + str(
                        self.database
                        .obtener_ultimo_error()
                    )
                )
            )

            return


        messagebox.showinfo(
            "Inscripciones",
            (
                "Alumno inscrito "
                "correctamente."
            )
        )


        self.cargar_inscripciones()


    def obtener_seleccion(self):

        seleccion = (
            self.tabla.selection()
        )


        if not seleccion:

            messagebox.showwarning(
                "Inscripciones",
                "Selecciona un alumno."
            )

            return None


        valores = self.tabla.item(
            seleccion[0],
            "values"
        )


        return {
            "id_alumno": int(
                valores[0]
            ),
            "codigo": valores[1],
            "nombre": valores[2],
            "apellido": valores[3],
            "fecha_inscripcion": valores[4],
            "fecha_retiro": valores[5],
            "estado": valores[6]
        }


    def retirar(self):

        alumno = (
            self.obtener_seleccion()
        )


        if alumno is None:

            return


        if alumno["estado"] == "RETIRADO":

            messagebox.showinfo(
                "Inscripciones",
                (
                    "El alumno ya fue retirado "
                    "de esta sección."
                )
            )

            return


        id_seccion = (
            self.obtener_id_seccion()
        )


        if id_seccion is None:

            return


        inscripcion = (
            self.database
            .consultar_uno(
                """
                SELECT id
                FROM inscripciones
                WHERE id_alumno = %s
                  AND id_seccion = %s
                """,
                (
                    alumno["id_alumno"],
                    id_seccion
                )
            )
        )


        if inscripcion is None:

            messagebox.showerror(
                "Inscripciones",
                (
                    "No se encontró la "
                    "inscripción seleccionada."
                )
            )

            return


        confirmar = (
            messagebox.askyesno(
                "Retirar alumno",
                (
                    "¿Deseas retirar al alumno "
                    "de esta sección?\n\n"
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
                "RetirarAlumno",
                (
                    inscripcion["id"],
                )
            )
        )


        if resultado is None:

            messagebox.showerror(
                "Inscripciones",
                (
                    "No se pudo retirar "
                    "al alumno.\n\n"
                    + str(
                        self.database
                        .obtener_ultimo_error()
                    )
                )
            )

            return


        messagebox.showinfo(
            "Inscripciones",
            (
                "Alumno retirado "
                "correctamente."
            )
        )


        self.cargar_inscripciones()


    def actualizar(self):

        self.cargar_alumnos()
        self.cargar_secciones()