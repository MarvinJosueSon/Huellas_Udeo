import tkinter as tk
from tkinter import ttk, messagebox


class Secciones(tk.Frame):

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
        self.datos_secciones = []

        self.mapa_cursos = {}
        self.mapa_docentes = {}
        self.mapa_periodos = {}
        self.mapa_jornadas = {}

        self.pack(
            fill="both",
            expand=True
        )

        self.crear_interfaz()
        self.cargar_catalogos()
        self.cargar_secciones()
        self.nueva()


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
            text="Secciones",
            bg="#F3F3F3",
            fg="#202020",
            font=("Segoe UI", 24, "bold")
        ).pack(
            side="left"
        )


        tk.Button(
            encabezado,
            text="+ Nueva sección",
            bg="#0078D4",
            fg="#FFFFFF",
            activebackground="#106EBE",
            activeforeground="#FFFFFF",
            relief="flat",
            bd=0,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            command=self.nueva
        ).pack(
            side="right",
            ipadx=15,
            ipady=6
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


        self.cmb_estado_filtro = ttk.Combobox(
            panel_filtros,
            state="readonly",
            values=(
                "TODAS",
                "ACTIVA",
                "INACTIVA"
            ),
            width=15
        )

        self.cmb_estado_filtro.set(
            "TODAS"
        )

        self.cmb_estado_filtro.pack(
            side="left",
            padx=8
        )

        self.cmb_estado_filtro.bind(
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
            "id",
            "curso",
            "seccion",
            "docente",
            "periodo",
            "jornada",
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
            "curso",
            text="Curso"
        )

        self.tabla.heading(
            "seccion",
            text="Sección"
        )

        self.tabla.heading(
            "docente",
            text="Docente"
        )

        self.tabla.heading(
            "periodo",
            text="Periodo"
        )

        self.tabla.heading(
            "jornada",
            text="Jornada"
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
            "curso",
            width=180
        )

        self.tabla.column(
            "seccion",
            width=80,
            anchor="center"
        )

        self.tabla.column(
            "docente",
            width=180
        )

        self.tabla.column(
            "periodo",
            width=160
        )

        self.tabla.column(
            "jornada",
            width=130
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
            width=380,
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
            text="Nueva sección",
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
            "Curso"
        )

        self.cmb_curso = ttk.Combobox(
            panel_formulario,
            state="readonly"
        )

        self.cmb_curso.pack(
            fill="x",
            padx=20,
            pady=(0, 12)
        )


        self.crear_etiqueta(
            panel_formulario,
            "Docente"
        )

        self.cmb_docente = ttk.Combobox(
            panel_formulario,
            state="readonly"
        )

        self.cmb_docente.pack(
            fill="x",
            padx=20,
            pady=(0, 12)
        )


        self.crear_etiqueta(
            panel_formulario,
            "Periodo académico"
        )

        self.cmb_periodo = ttk.Combobox(
            panel_formulario,
            state="readonly"
        )

        self.cmb_periodo.pack(
            fill="x",
            padx=20,
            pady=(0, 12)
        )


        self.crear_etiqueta(
            panel_formulario,
            "Jornada"
        )

        self.cmb_jornada = ttk.Combobox(
            panel_formulario,
            state="readonly"
        )

        self.cmb_jornada.pack(
            fill="x",
            padx=20,
            pady=(0, 12)
        )


        self.crear_etiqueta(
            panel_formulario,
            "Sección"
        )

        self.txt_seccion = ttk.Entry(
            panel_formulario
        )

        self.txt_seccion.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )


        self.btn_guardar = tk.Button(
            panel_formulario,
            text="Guardar sección",
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
            command=self.nueva
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


    def cargar_catalogos(self):

        self.cargar_cursos()
        self.cargar_docentes()
        self.cargar_periodos()
        self.cargar_jornadas()


    def cargar_cursos(self):

        datos = self.database.consultar(
            """
            SELECT
                id,
                codigo,
                nombre,
                estado
            FROM cursos
            ORDER BY nombre
            """
        )


        if (
            not datos
            and self.database.obtener_ultimo_error()
        ):

            messagebox.showerror(
                "Secciones",
                (
                    "No se pudieron cargar "
                    "los cursos.\n\n"
                    + str(
                        self.database
                        .obtener_ultimo_error()
                    )
                )
            )

            return


        valores = []
        self.mapa_cursos = {}


        for curso in datos:

            texto = (
                f"{curso['id']} - "
                f"{curso['codigo']} - "
                f"{curso['nombre']} "
                f"({curso['estado']})"
            )

            valores.append(
                texto
            )

            self.mapa_cursos[
                texto
            ] = curso["id"]


        self.cmb_curso[
            "values"
        ] = valores


    def cargar_docentes(self):

        datos = self.database.consultar(
            """
            SELECT
                id,
                codigo,
                nombre,
                apellido,
                estado
            FROM docentes
            ORDER BY nombre, apellido
            """
        )


        if (
            not datos
            and self.database.obtener_ultimo_error()
        ):

            messagebox.showerror(
                "Secciones",
                (
                    "No se pudieron cargar "
                    "los docentes.\n\n"
                    + str(
                        self.database
                        .obtener_ultimo_error()
                    )
                )
            )

            return


        valores = []
        self.mapa_docentes = {}


        for docente in datos:

            texto = (
                f"{docente['id']} - "
                f"{docente['nombre']} "
                f"{docente['apellido']} "
                f"({docente['estado']})"
            )

            valores.append(
                texto
            )

            self.mapa_docentes[
                texto
            ] = docente["id"]


        self.cmb_docente[
            "values"
        ] = valores


    def cargar_periodos(self):

        datos = self.database.consultar(
            """
            SELECT
                id,
                nombre,
                estado
            FROM periodos_academicos
            ORDER BY fecha_inicio
            """
        )


        if (
            not datos
            and self.database.obtener_ultimo_error()
        ):

            messagebox.showerror(
                "Secciones",
                (
                    "No se pudieron cargar "
                    "los periodos.\n\n"
                    + str(
                        self.database
                        .obtener_ultimo_error()
                    )
                )
            )

            return


        valores = []
        self.mapa_periodos = {}


        for periodo in datos:

            texto = (
                f"{periodo['id']} - "
                f"{periodo['nombre']} "
                f"({periodo['estado']})"
            )

            valores.append(
                texto
            )

            self.mapa_periodos[
                texto
            ] = periodo["id"]


        self.cmb_periodo[
            "values"
        ] = valores


    def cargar_jornadas(self):

        datos = self.database.consultar(
            """
            SELECT
                id,
                nombre,
                estado
            FROM jornadas
            ORDER BY nombre
            """
        )


        if (
            not datos
            and self.database.obtener_ultimo_error()
        ):

            messagebox.showerror(
                "Secciones",
                (
                    "No se pudieron cargar "
                    "las jornadas.\n\n"
                    + str(
                        self.database
                        .obtener_ultimo_error()
                    )
                )
            )

            return


        valores = []
        self.mapa_jornadas = {}


        for jornada in datos:

            texto = (
                f"{jornada['id']} - "
                f"{jornada['nombre']} "
                f"({jornada['estado']})"
            )

            valores.append(
                texto
            )

            self.mapa_jornadas[
                texto
            ] = jornada["id"]


        self.cmb_jornada[
            "values"
        ] = valores


    def cargar_secciones(self):

        resultados = (
            self.database
            .llamar_procedimiento(
                "ListarSeccionesDocente"
            )
        )


        if resultados is None:

            messagebox.showerror(
                "Secciones",
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


        self.datos_secciones = []


        if resultados:

            self.datos_secciones = (
                resultados[0]
            )


        self.mostrar_datos(
            self.datos_secciones
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


        for seccion in datos:

            docente = (
                seccion.get(
                    "docente",
                    ""
                )
            )


            self.tabla.insert(
                "",
                tk.END,
                values=(
                    seccion["id"],
                    seccion["curso"],
                    seccion["seccion"],
                    docente,
                    seccion["periodo"],
                    seccion["jornada"],
                    seccion["estado"]
                )
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
            self.cmb_estado_filtro
            .get()
        )


        filtrados = []


        for seccion in self.datos_secciones:

            curso = str(
                seccion.get(
                    "curso",
                    ""
                )
            ).lower()

            nombre_seccion = str(
                seccion.get(
                    "seccion",
                    ""
                )
            ).lower()

            docente = str(
                seccion.get(
                    "docente",
                    ""
                )
            ).lower()

            periodo = str(
                seccion.get(
                    "periodo",
                    ""
                )
            ).lower()

            jornada = str(
                seccion.get(
                    "jornada",
                    ""
                )
            ).lower()


            coincide_texto = (
                texto == ""
                or texto in curso
                or texto in nombre_seccion
                or texto in docente
                or texto in periodo
                or texto in jornada
            )


            coincide_estado = (
                estado == "TODAS"
                or seccion["estado"]
                == estado
            )


            if (
                coincide_texto
                and coincide_estado
            ):

                filtrados.append(
                    seccion
                )


        self.mostrar_datos(
            filtrados
        )


    def obtener_seleccion(self):

        seleccion = (
            self.tabla.selection()
        )


        if not seleccion:

            messagebox.showwarning(
                "Secciones",
                "Selecciona una sección."
            )

            return None


        valores = self.tabla.item(
            seleccion[0],
            "values"
        )


        return {
            "id": int(valores[0]),
            "curso": valores[1],
            "seccion": valores[2],
            "docente": valores[3],
            "periodo": valores[4],
            "jornada": valores[5],
            "estado": valores[6]
        }


    def obtener_detalle_seccion(
        self,
        id_seccion
    ):

        resultado = (
            self.database
            .consultar_uno(
                """
                SELECT
                    id,
                    id_curso,
                    id_docente,
                    id_periodo,
                    id_jornada,
                    seccion,
                    estado
                FROM secciones_curso
                WHERE id = %s
                """,
                (
                    id_seccion,
                )
            )
        )


        if resultado is None:

            messagebox.showerror(
                "Secciones",
                (
                    "No se pudo obtener "
                    "la información de la sección.\n\n"
                    + str(
                        self.database
                        .obtener_ultimo_error()
                        or ""
                    )
                )
            )

            return None


        return resultado


    def nueva(self):

        self.id_seleccionado = None


        self.lbl_titulo.config(
            text="Nueva sección"
        )


        self.btn_guardar.config(
            text="Guardar sección"
        )


        self.cmb_curso.set(
            ""
        )

        self.cmb_docente.set(
            ""
        )

        self.cmb_periodo.set(
            ""
        )

        self.cmb_jornada.set(
            ""
        )

        self.txt_seccion.delete(
            0,
            tk.END
        )


        for fila in (
            self.tabla.selection()
        ):

            self.tabla.selection_remove(
                fila
            )


        self.cmb_curso.focus_set()


    def editar(
        self,
        event=None
    ):

        seccion = (
            self.obtener_seleccion()
        )


        if seccion is None:

            return


        detalle = (
            self.obtener_detalle_seccion(
                seccion["id"]
            )
        )


        if detalle is None:

            return


        self.id_seleccionado = (
            detalle["id"]
        )


        self.seleccionar_combo(
            self.cmb_curso,
            self.mapa_cursos,
            detalle["id_curso"]
        )


        self.seleccionar_combo(
            self.cmb_docente,
            self.mapa_docentes,
            detalle["id_docente"]
        )


        self.seleccionar_combo(
            self.cmb_periodo,
            self.mapa_periodos,
            detalle["id_periodo"]
        )


        self.seleccionar_combo(
            self.cmb_jornada,
            self.mapa_jornadas,
            detalle["id_jornada"]
        )


        self.txt_seccion.delete(
            0,
            tk.END
        )

        self.txt_seccion.insert(
            0,
            detalle["seccion"]
        )


        self.lbl_titulo.config(
            text="Editar sección"
        )


        self.btn_guardar.config(
            text="Guardar cambios"
        )


    def seleccionar_combo(
        self,
        combo,
        mapa,
        identificador
    ):

        for texto, id_elemento in (
            mapa.items()
        ):

            if id_elemento == identificador:

                combo.set(
                    texto
                )

                return


        combo.set(
            ""
        )


    def validar_formulario(self):

        curso_texto = (
            self.cmb_curso
            .get()
            .strip()
        )

        docente_texto = (
            self.cmb_docente
            .get()
            .strip()
        )

        periodo_texto = (
            self.cmb_periodo
            .get()
            .strip()
        )

        jornada_texto = (
            self.cmb_jornada
            .get()
            .strip()
        )

        seccion = (
            self.txt_seccion
            .get()
            .strip()
        )


        if (
            curso_texto
            not in self.mapa_cursos
        ):

            messagebox.showwarning(
                "Secciones",
                "Selecciona un curso."
            )

            return None


        if (
            docente_texto
            not in self.mapa_docentes
        ):

            messagebox.showwarning(
                "Secciones",
                "Selecciona un docente."
            )

            return None


        if (
            periodo_texto
            not in self.mapa_periodos
        ):

            messagebox.showwarning(
                "Secciones",
                "Selecciona un periodo."
            )

            return None


        if (
            jornada_texto
            not in self.mapa_jornadas
        ):

            messagebox.showwarning(
                "Secciones",
                "Selecciona una jornada."
            )

            return None


        if seccion == "":

            messagebox.showwarning(
                "Secciones",
                "Ingresa el nombre de la sección."
            )

            self.txt_seccion.focus_set()

            return None


        if len(seccion) > 20:

            messagebox.showwarning(
                "Secciones",
                (
                    "La sección no puede superar "
                    "20 caracteres."
                )
            )

            return None


        return {
            "id_curso": self.mapa_cursos[
                curso_texto
            ],
            "id_docente": self.mapa_docentes[
                docente_texto
            ],
            "id_periodo": self.mapa_periodos[
                periodo_texto
            ],
            "id_jornada": self.mapa_jornadas[
                jornada_texto
            ],
            "seccion": seccion
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
                    "CrearSeccion",
                    (
                        datos["id_curso"],
                        datos["id_docente"],
                        datos["id_periodo"],
                        datos["id_jornada"],
                        datos["seccion"]
                    )
                )
            )


            if resultado is None:

                messagebox.showerror(
                    "Secciones",
                    (
                        "No se pudo crear "
                        "la sección.\n\n"
                        + str(
                            self.database
                            .obtener_ultimo_error()
                        )
                    )
                )

                return


            messagebox.showinfo(
                "Secciones",
                "Sección creada correctamente."
            )


        else:

            resultado = (
                self.database
                .llamar_procedimiento(
                    "ModificarSeccion",
                    (
                        self.id_seleccionado,
                        datos["id_curso"],
                        datos["id_docente"],
                        datos["id_periodo"],
                        datos["id_jornada"],
                        datos["seccion"]
                    )
                )
            )


            if resultado is None:

                messagebox.showerror(
                    "Secciones",
                    (
                        "No se pudo modificar "
                        "la sección.\n\n"
                        + str(
                            self.database
                            .obtener_ultimo_error()
                        )
                    )
                )

                return


            messagebox.showinfo(
                "Secciones",
                (
                    "Sección modificada "
                    "correctamente."
                )
            )


        self.cargar_secciones()

        self.nueva()


    def inactivar(self):

        seccion = (
            self.obtener_seleccion()
        )


        if seccion is None:

            return


        if seccion["estado"] == "INACTIVA":

            messagebox.showinfo(
                "Secciones",
                (
                    "La sección ya se encuentra "
                    "inactiva."
                )
            )

            return


        confirmar = (
            messagebox.askyesno(
                "Inactivar sección",
                (
                    "¿Deseas inactivar "
                    "la sección?\n\n"
                    f"{seccion['curso']} - "
                    f"{seccion['seccion']}"
                )
            )
        )


        if not confirmar:

            return


        resultado = (
            self.database
            .llamar_procedimiento(
                "InactivarSeccion",
                (
                    seccion["id"],
                )
            )
        )


        if resultado is None:

            messagebox.showerror(
                "Secciones",
                (
                    "No se pudo inactivar "
                    "la sección.\n\n"
                    + str(
                        self.database
                        .obtener_ultimo_error()
                    )
                )
            )

            return


        messagebox.showinfo(
            "Secciones",
            (
                "Sección inactivada "
                "correctamente."
            )
        )


        self.cargar_secciones()

        self.nueva()


    def actualizar(self):

        self.cargar_catalogos()
        self.cargar_secciones()
        self.nueva()