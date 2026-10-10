import tkinter as tk
from tkinter import ttk, messagebox


class Puntuacion(tk.Frame):

    def __init__(self, master, database):
        super().__init__(master, bg="#F3F3F3")

        self.database = database

        self.mapa_secciones = {}
        self.mapa_alumnos = {}

        self.datos_reglas = []
        self.datos_rangos = []

        self.id_regla_seleccionada = None
        self.id_rango_edicion = None

        self.pack(fill="both", expand=True)

        self.crear_interfaz()
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
            text="Puntuación",
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


        panel_seccion = tk.Frame(
            self,
            bg="#FFFFFF",
            highlightthickness=1,
            highlightbackground="#DDDDDD"
        )

        panel_seccion.pack(
            fill="x",
            padx=30,
            pady=(0, 15)
        )


        tk.Label(
            panel_seccion,
            text="Sección:",
            bg="#FFFFFF",
            fg="#202020",
            font=("Segoe UI", 10, "bold")
        ).pack(
            side="left",
            padx=(20, 8),
            pady=15
        )


        self.cmb_seccion = ttk.Combobox(
            panel_seccion,
            state="readonly",
            width=70
        )

        self.cmb_seccion.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 20),
            pady=15
        )

        self.cmb_seccion.bind(
            "<<ComboboxSelected>>",
            self.cambiar_seccion
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


        self.tab_reglas = tk.Frame(
            self.notebook,
            bg="#F3F3F3"
        )

        self.tab_calculo = tk.Frame(
            self.notebook,
            bg="#F3F3F3"
        )


        self.notebook.add(
            self.tab_reglas,
            text="Reglas y rangos"
        )

        self.notebook.add(
            self.tab_calculo,
            text="Cálculo por alumno"
        )


        self.crear_tab_reglas()
        self.crear_tab_calculo()


    def crear_tab_reglas(self):

        cuerpo = tk.Frame(
            self.tab_reglas,
            bg="#F3F3F3"
        )

        cuerpo.pack(
            fill="both",
            expand=True,
            pady=(15, 0)
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
            weight=1
        )


        panel_reglas = tk.Frame(
            cuerpo,
            bg="#FFFFFF",
            highlightthickness=1,
            highlightbackground="#DDDDDD"
        )

        panel_reglas.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 7)
        )


        tk.Label(
            panel_reglas,
            text="Reglas de puntuación",
            bg="#FFFFFF",
            fg="#202020",
            font=("Segoe UI", 14, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 15)
        )


        tabla_reglas_frame = tk.Frame(
            panel_reglas,
            bg="#FFFFFF"
        )

        tabla_reglas_frame.pack(
            fill="both",
            expand=True,
            padx=20
        )


        columnas_reglas = (
            "id",
            "nombre",
            "estado",
            "fecha"
        )


        self.tabla_reglas = ttk.Treeview(
            tabla_reglas_frame,
            columns=columnas_reglas,
            show="headings",
            selectmode="browse",
            height=8
        )


        self.tabla_reglas.heading(
            "id",
            text="ID"
        )

        self.tabla_reglas.heading(
            "nombre",
            text="Nombre"
        )

        self.tabla_reglas.heading(
            "estado",
            text="Estado"
        )

        self.tabla_reglas.heading(
            "fecha",
            text="Fecha"
        )


        self.tabla_reglas.column(
            "id",
            width=50,
            anchor="center"
        )

        self.tabla_reglas.column(
            "nombre",
            width=180
        )

        self.tabla_reglas.column(
            "estado",
            width=90,
            anchor="center"
        )

        self.tabla_reglas.column(
            "fecha",
            width=140,
            anchor="center"
        )


        scroll_reglas = ttk.Scrollbar(
            tabla_reglas_frame,
            orient="vertical",
            command=self.tabla_reglas.yview
        )

        self.tabla_reglas.configure(
            yscrollcommand=scroll_reglas.set
        )


        self.tabla_reglas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scroll_reglas.pack(
            side="right",
            fill="y"
        )


        self.tabla_reglas.bind(
            "<<TreeviewSelect>>",
            self.seleccionar_regla
        )


        formulario_regla = tk.Frame(
            panel_reglas,
            bg="#FFFFFF"
        )

        formulario_regla.pack(
            fill="x",
            padx=20,
            pady=15
        )


        tk.Label(
            formulario_regla,
            text="Nombre de nueva regla",
            bg="#FFFFFF",
            fg="#202020",
            font=("Segoe UI", 9)
        ).pack(
            anchor="w"
        )


        self.txt_nombre_regla = ttk.Entry(
            formulario_regla
        )

        self.txt_nombre_regla.pack(
            fill="x",
            pady=(5, 10)
        )


        tk.Button(
            formulario_regla,
            text="Crear regla",
            bg="#0078D4",
            fg="#FFFFFF",
            activebackground="#106EBE",
            activeforeground="#FFFFFF",
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            command=self.crear_regla
        ).pack(
            fill="x",
            ipady=5
        )


        tk.Button(
            formulario_regla,
            text="Inactivar regla seleccionada",
            bg="#E5E5E5",
            fg="#202020",
            activebackground="#D5D5D5",
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 10),
            command=self.inactivar_regla
        ).pack(
            fill="x",
            pady=(8, 0),
            ipady=5
        )


        panel_rangos = tk.Frame(
            cuerpo,
            bg="#FFFFFF",
            highlightthickness=1,
            highlightbackground="#DDDDDD"
        )

        panel_rangos.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(7, 0)
        )


        self.lbl_rangos = tk.Label(
            panel_rangos,
            text="Rangos de puntuación",
            bg="#FFFFFF",
            fg="#202020",
            font=("Segoe UI", 14, "bold")
        )

        self.lbl_rangos.pack(
            anchor="w",
            padx=20,
            pady=(20, 15)
        )


        tabla_rangos_frame = tk.Frame(
            panel_rangos,
            bg="#FFFFFF"
        )

        tabla_rangos_frame.pack(
            fill="both",
            expand=True,
            padx=20
        )


        columnas_rangos = (
            "id",
            "minimo",
            "maximo",
            "puntos"
        )


        self.tabla_rangos = ttk.Treeview(
            tabla_rangos_frame,
            columns=columnas_rangos,
            show="headings",
            selectmode="browse",
            height=8
        )


        self.tabla_rangos.heading(
            "id",
            text="ID"
        )

        self.tabla_rangos.heading(
            "minimo",
            text="Mínimo %"
        )

        self.tabla_rangos.heading(
            "maximo",
            text="Máximo %"
        )

        self.tabla_rangos.heading(
            "puntos",
            text="Puntos"
        )


        self.tabla_rangos.column(
            "id",
            width=50,
            anchor="center"
        )

        self.tabla_rangos.column(
            "minimo",
            width=100,
            anchor="center"
        )

        self.tabla_rangos.column(
            "maximo",
            width=100,
            anchor="center"
        )

        self.tabla_rangos.column(
            "puntos",
            width=100,
            anchor="center"
        )


        scroll_rangos = ttk.Scrollbar(
            tabla_rangos_frame,
            orient="vertical",
            command=self.tabla_rangos.yview
        )

        self.tabla_rangos.configure(
            yscrollcommand=scroll_rangos.set
        )


        self.tabla_rangos.pack(
            side="left",
            fill="both",
            expand=True
        )

        scroll_rangos.pack(
            side="right",
            fill="y"
        )


        self.tabla_rangos.bind(
            "<Double-1>",
            self.editar_rango
        )


        formulario_rango = tk.Frame(
            panel_rangos,
            bg="#FFFFFF"
        )

        formulario_rango.pack(
            fill="x",
            padx=20,
            pady=15
        )


        campos = tk.Frame(
            formulario_rango,
            bg="#FFFFFF"
        )

        campos.pack(
            fill="x"
        )


        campos.grid_columnconfigure(
            0,
            weight=1
        )

        campos.grid_columnconfigure(
            1,
            weight=1
        )

        campos.grid_columnconfigure(
            2,
            weight=1
        )


        tk.Label(
            campos,
            text="Mínimo %",
            bg="#FFFFFF",
            fg="#202020",
            font=("Segoe UI", 9)
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=(0, 5)
        )


        tk.Label(
            campos,
            text="Máximo %",
            bg="#FFFFFF",
            fg="#202020",
            font=("Segoe UI", 9)
        ).grid(
            row=0,
            column=1,
            sticky="w",
            padx=5
        )


        tk.Label(
            campos,
            text="Puntos",
            bg="#FFFFFF",
            fg="#202020",
            font=("Segoe UI", 9)
        ).grid(
            row=0,
            column=2,
            sticky="w",
            padx=(5, 0)
        )


        self.txt_minimo = ttk.Entry(
            campos
        )

        self.txt_minimo.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=(0, 5),
            pady=(5, 10)
        )


        self.txt_maximo = ttk.Entry(
            campos
        )

        self.txt_maximo.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=5,
            pady=(5, 10)
        )


        self.txt_puntos = ttk.Entry(
            campos
        )

        self.txt_puntos.grid(
            row=1,
            column=2,
            sticky="ew",
            padx=(5, 0),
            pady=(5, 10)
        )


        self.btn_guardar_rango = tk.Button(
            formulario_rango,
            text="Agregar rango",
            bg="#0078D4",
            fg="#FFFFFF",
            activebackground="#106EBE",
            activeforeground="#FFFFFF",
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            command=self.guardar_rango
        )

        self.btn_guardar_rango.pack(
            fill="x",
            ipady=5
        )


        botones_rango = tk.Frame(
            formulario_rango,
            bg="#FFFFFF"
        )

        botones_rango.pack(
            fill="x",
            pady=(8, 0)
        )


        tk.Button(
            botones_rango,
            text="Editar seleccionado",
            bg="#E5E5E5",
            fg="#202020",
            activebackground="#D5D5D5",
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 9),
            command=self.editar_rango
        ).pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 4),
            ipady=4
        )


        tk.Button(
            botones_rango,
            text="Eliminar seleccionado",
            bg="#E5E5E5",
            fg="#202020",
            activebackground="#D5D5D5",
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 9),
            command=self.eliminar_rango
        ).pack(
            side="left",
            fill="x",
            expand=True,
            padx=(4, 0),
            ipady=4
        )


        tk.Button(
            formulario_rango,
            text="Cancelar edición",
            bg="#F2F2F2",
            fg="#202020",
            activebackground="#E2E2E2",
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 9),
            command=self.limpiar_formulario_rango
        ).pack(
            fill="x",
            pady=(8, 0),
            ipady=4
        )


    def crear_tab_calculo(self):

        panel = tk.Frame(
            self.tab_calculo,
            bg="#FFFFFF",
            highlightthickness=1,
            highlightbackground="#DDDDDD"
        )

        panel.pack(
            fill="both",
            expand=True,
            pady=(15, 0)
        )


        tk.Label(
            panel,
            text="Cálculo de asistencia y puntos",
            bg="#FFFFFF",
            fg="#202020",
            font=("Segoe UI", 15, "bold")
        ).pack(
            anchor="w",
            padx=25,
            pady=(25, 15)
        )


        tk.Label(
            panel,
            text="Alumno",
            bg="#FFFFFF",
            fg="#202020",
            font=("Segoe UI", 9)
        ).pack(
            anchor="w",
            padx=25
        )


        self.cmb_alumno = ttk.Combobox(
            panel,
            state="readonly",
            width=60
        )

        self.cmb_alumno.pack(
            fill="x",
            padx=25,
            pady=(5, 20)
        )


        tk.Button(
            panel,
            text="Calcular",
            bg="#0078D4",
            fg="#FFFFFF",
            activebackground="#106EBE",
            activeforeground="#FFFFFF",
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            command=self.calcular
        ).pack(
            anchor="w",
            padx=25,
            ipadx=30,
            ipady=6
        )


        resultado = tk.Frame(
            panel,
            bg="#F7F7F7",
            highlightthickness=1,
            highlightbackground="#E0E0E0"
        )

        resultado.pack(
            fill="x",
            padx=25,
            pady=25
        )


        self.lbl_total = self.crear_resultado(
            resultado,
            "Total de clases:"
        )

        self.lbl_presentes = self.crear_resultado(
            resultado,
            "Presentes:"
        )

        self.lbl_tardes = self.crear_resultado(
            resultado,
            "Tardes:"
        )

        self.lbl_justificadas = self.crear_resultado(
            resultado,
            "Justificadas:"
        )

        self.lbl_ausentes = self.crear_resultado(
            resultado,
            "Ausentes:"
        )

        self.lbl_fuera = self.crear_resultado(
            resultado,
            "Fuera de tiempo:"
        )

        self.lbl_validas = self.crear_resultado(
            resultado,
            "Asistencias válidas:"
        )

        self.lbl_porcentaje = self.crear_resultado(
            resultado,
            "Porcentaje:"
        )

        self.lbl_puntos = self.crear_resultado(
            resultado,
            "Puntos:"
        )


    def crear_resultado(
        self,
        padre,
        texto
    ):

        fila = tk.Frame(
            padre,
            bg="#F7F7F7"
        )

        fila.pack(
            fill="x",
            padx=20,
            pady=4
        )


        tk.Label(
            fila,
            text=texto,
            bg="#F7F7F7",
            fg="#404040",
            font=("Segoe UI", 10)
        ).pack(
            side="left"
        )


        valor = tk.Label(
            fila,
            text="-",
            bg="#F7F7F7",
            fg="#202020",
            font=("Segoe UI", 10, "bold")
        )

        valor.pack(
            side="right"
        )

        return valor


    def cargar_secciones(self):

        id_anterior = (
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
                "Puntuación",
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

            self.limpiar_datos()

            return


        seleccionado = False


        if id_anterior is not None:

            for texto, identificador in (
                self.mapa_secciones.items()
            ):

                if identificador == id_anterior:

                    self.cmb_seccion.set(
                        texto
                    )

                    seleccionado = True

                    break


        if not seleccionado:

            self.cmb_seccion.current(
                0
            )


        self.cargar_datos_seccion()


    def obtener_id_seccion(self):

        if not hasattr(
            self,
            "cmb_seccion"
        ):

            return None


        return self.mapa_secciones.get(
            self.cmb_seccion.get()
        )


    def cambiar_seccion(
        self,
        event=None
    ):

        self.id_regla_seleccionada = None
        self.id_rango_edicion = None

        self.cargar_datos_seccion()


    def cargar_datos_seccion(self):

        self.cargar_reglas()
        self.cargar_alumnos()
        self.limpiar_resultados()


    def cargar_reglas(self):

        id_seccion = (
            self.obtener_id_seccion()
        )


        self.id_regla_seleccionada = None

        self.limpiar_formulario_rango()


        if id_seccion is None:

            self.datos_reglas = []
            self.mostrar_reglas([])
            self.mostrar_rangos([])
            return


        resultados = (
            self.database
            .consultar(
                """
                SELECT
                    id,
                    nombre,
                    estado,
                    fecha_registro
                FROM reglas_puntuacion
                WHERE id_seccion = %s
                ORDER BY
                    CASE
                        WHEN estado = 'ACTIVA'
                        THEN 0
                        ELSE 1
                    END,
                    id DESC
                """,
                (
                    id_seccion,
                )
            )
        )


        if (
            not resultados
            and self.database.obtener_ultimo_error()
        ):

            messagebox.showerror(
                "Puntuación",
                (
                    "No se pudieron cargar "
                    "las reglas.\n\n"
                    + str(
                        self.database
                        .obtener_ultimo_error()
                    )
                )
            )

            return


        self.datos_reglas = resultados

        self.mostrar_reglas(
            self.datos_reglas
        )


        if self.datos_reglas:

            primer_item = (
                self.tabla_reglas
                .get_children()[0]
            )

            self.tabla_reglas.selection_set(
                primer_item
            )

            self.tabla_reglas.focus(
                primer_item
            )

            self.seleccionar_regla()


        else:

            self.mostrar_rangos([])


    def mostrar_reglas(
        self,
        datos
    ):

        for fila in (
            self.tabla_reglas
            .get_children()
        ):

            self.tabla_reglas.delete(
                fila
            )


        for regla in datos:

            self.tabla_reglas.insert(
                "",
                tk.END,
                values=(
                    regla["id"],
                    regla["nombre"],
                    regla["estado"],
                    self.formatear_fecha_hora(
                        regla["fecha_registro"]
                    )
                )
            )


    def seleccionar_regla(
        self,
        event=None
    ):

        seleccion = (
            self.tabla_reglas.selection()
        )


        if not seleccion:

            self.id_regla_seleccionada = None
            self.mostrar_rangos([])
            return


        valores = (
            self.tabla_reglas
            .item(
                seleccion[0],
                "values"
            )
        )


        self.id_regla_seleccionada = int(
            valores[0]
        )


        self.lbl_rangos.config(
            text=(
                "Rangos - "
                + str(
                    valores[1]
                )
            )
        )


        self.cargar_rangos()


    def cargar_rangos(self):

        if self.id_regla_seleccionada is None:

            self.datos_rangos = []
            self.mostrar_rangos([])
            return


        resultados = (
            self.database
            .consultar(
                """
                SELECT
                    id,
                    minimo,
                    maximo,
                    puntos
                FROM rangos_puntuacion
                WHERE id_regla = %s
                ORDER BY minimo
                """,
                (
                    self.id_regla_seleccionada,
                )
            )
        )


        if (
            not resultados
            and self.database.obtener_ultimo_error()
        ):

            messagebox.showerror(
                "Puntuación",
                (
                    "No se pudieron cargar "
                    "los rangos.\n\n"
                    + str(
                        self.database
                        .obtener_ultimo_error()
                    )
                )
            )

            return


        self.datos_rangos = resultados

        self.mostrar_rangos(
            self.datos_rangos
        )

        self.limpiar_formulario_rango()


    def mostrar_rangos(
        self,
        datos
    ):

        for fila in (
            self.tabla_rangos
            .get_children()
        ):

            self.tabla_rangos.delete(
                fila
            )


        for rango in datos:

            self.tabla_rangos.insert(
                "",
                tk.END,
                values=(
                    rango["id"],
                    rango["minimo"],
                    rango["maximo"],
                    rango["puntos"]
                )
            )


    def crear_regla(self):

        id_seccion = (
            self.obtener_id_seccion()
        )


        if id_seccion is None:

            messagebox.showwarning(
                "Puntuación",
                "Selecciona una sección."
            )

            return


        nombre = (
            self.txt_nombre_regla
            .get()
            .strip()
        )


        if nombre == "":

            messagebox.showwarning(
                "Puntuación",
                (
                    "Ingresa el nombre "
                    "de la regla."
                )
            )

            return


        if len(nombre) > 80:

            messagebox.showwarning(
                "Puntuación",
                (
                    "El nombre no puede superar "
                    "80 caracteres."
                )
            )

            return


        resultado = (
            self.database
            .llamar_procedimiento(
                "CrearReglaPuntuacion",
                (
                    id_seccion,
                    nombre
                )
            )
        )


        if resultado is None:

            messagebox.showerror(
                "Puntuación",
                (
                    "No se pudo crear "
                    "la regla.\n\n"
                    + str(
                        self.database
                        .obtener_ultimo_error()
                    )
                )
            )

            return


        messagebox.showinfo(
            "Puntuación",
            (
                "Regla creada "
                "correctamente."
            )
        )


        self.txt_nombre_regla.delete(
            0,
            tk.END
        )

        self.cargar_reglas()


    def obtener_regla_seleccionada(self):

        seleccion = (
            self.tabla_reglas.selection()
        )


        if not seleccion:

            messagebox.showwarning(
                "Puntuación",
                "Selecciona una regla."
            )

            return None


        valores = (
            self.tabla_reglas
            .item(
                seleccion[0],
                "values"
            )
        )


        return {
            "id": int(
                valores[0]
            ),
            "nombre": valores[1],
            "estado": valores[2]
        }


    def inactivar_regla(self):

        regla = (
            self.obtener_regla_seleccionada()
        )


        if regla is None:

            return


        if regla["estado"] == "INACTIVA":

            messagebox.showinfo(
                "Puntuación",
                (
                    "La regla ya se encuentra "
                    "inactiva."
                )
            )

            return


        confirmar = (
            messagebox.askyesno(
                "Inactivar regla",
                (
                    "¿Deseas inactivar "
                    "esta regla?\n\n"
                    f"{regla['nombre']}"
                )
            )
        )


        if not confirmar:

            return


        resultado = (
            self.database
            .llamar_procedimiento(
                "InactivarReglaPuntuacion",
                (
                    regla["id"],
                )
            )
        )


        if resultado is None:

            messagebox.showerror(
                "Puntuación",
                (
                    "No se pudo inactivar "
                    "la regla.\n\n"
                    + str(
                        self.database
                        .obtener_ultimo_error()
                    )
                )
            )

            return


        messagebox.showinfo(
            "Puntuación",
            (
                "Regla inactivada "
                "correctamente."
            )
        )


        self.cargar_reglas()


    def validar_rango(self):

        minimo_texto = (
            self.txt_minimo
            .get()
            .strip()
        )

        maximo_texto = (
            self.txt_maximo
            .get()
            .strip()
        )

        puntos_texto = (
            self.txt_puntos
            .get()
            .strip()
        )


        try:

            minimo = float(
                minimo_texto
            )

            maximo = float(
                maximo_texto
            )

            puntos = float(
                puntos_texto
            )

        except ValueError:

            messagebox.showwarning(
                "Puntuación",
                (
                    "Mínimo, máximo y puntos "
                    "deben ser valores numéricos."
                )
            )

            return None


        return {
            "minimo": minimo,
            "maximo": maximo,
            "puntos": puntos
        }


    def guardar_rango(self):

        if self.id_regla_seleccionada is None:

            messagebox.showwarning(
                "Puntuación",
                (
                    "Selecciona primero "
                    "una regla."
                )
            )

            return


        datos = (
            self.validar_rango()
        )


        if datos is None:

            return


        if self.id_rango_edicion is None:

            resultado = (
                self.database
                .llamar_procedimiento(
                    "AgregarRangoPuntuacion",
                    (
                        self.id_regla_seleccionada,
                        datos["minimo"],
                        datos["maximo"],
                        datos["puntos"]
                    )
                )
            )


            mensaje = (
                "Rango agregado "
                "correctamente."
            )


        else:

            resultado = (
                self.database
                .llamar_procedimiento(
                    "ModificarRangoPuntuacion",
                    (
                        self.id_rango_edicion,
                        datos["minimo"],
                        datos["maximo"],
                        datos["puntos"]
                    )
                )
            )


            mensaje = (
                "Rango modificado "
                "correctamente."
            )


        if resultado is None:

            messagebox.showerror(
                "Puntuación",
                (
                    "No se pudo guardar "
                    "el rango.\n\n"
                    + str(
                        self.database
                        .obtener_ultimo_error()
                    )
                )
            )

            return


        messagebox.showinfo(
            "Puntuación",
            mensaje
        )


        self.cargar_rangos()


    def obtener_rango_seleccionado(self):

        seleccion = (
            self.tabla_rangos.selection()
        )


        if not seleccion:

            messagebox.showwarning(
                "Puntuación",
                "Selecciona un rango."
            )

            return None


        valores = (
            self.tabla_rangos
            .item(
                seleccion[0],
                "values"
            )
        )


        return {
            "id": int(
                valores[0]
            ),
            "minimo": valores[1],
            "maximo": valores[2],
            "puntos": valores[3]
        }


    def editar_rango(
        self,
        event=None
    ):

        rango = (
            self.obtener_rango_seleccionado()
        )


        if rango is None:

            return


        self.id_rango_edicion = (
            rango["id"]
        )


        self.txt_minimo.delete(
            0,
            tk.END
        )

        self.txt_minimo.insert(
            0,
            rango["minimo"]
        )


        self.txt_maximo.delete(
            0,
            tk.END
        )

        self.txt_maximo.insert(
            0,
            rango["maximo"]
        )


        self.txt_puntos.delete(
            0,
            tk.END
        )

        self.txt_puntos.insert(
            0,
            rango["puntos"]
        )


        self.btn_guardar_rango.config(
            text="Guardar cambios"
        )


    def eliminar_rango(self):

        rango = (
            self.obtener_rango_seleccionado()
        )


        if rango is None:

            return


        confirmar = (
            messagebox.askyesno(
                "Eliminar rango",
                (
                    "¿Deseas eliminar "
                    "este rango?\n\n"
                    f"{rango['minimo']}% - "
                    f"{rango['maximo']}% "
                    f"= {rango['puntos']} puntos"
                )
            )
        )


        if not confirmar:

            return


        resultado = (
            self.database
            .llamar_procedimiento(
                "EliminarRangoPuntuacion",
                (
                    rango["id"],
                )
            )
        )


        if resultado is None:

            messagebox.showerror(
                "Puntuación",
                (
                    "No se pudo eliminar "
                    "el rango.\n\n"
                    + str(
                        self.database
                        .obtener_ultimo_error()
                    )
                )
            )

            return


        messagebox.showinfo(
            "Puntuación",
            (
                "Rango eliminado "
                "correctamente."
            )
        )


        self.cargar_rangos()


    def limpiar_formulario_rango(self):

        self.id_rango_edicion = None


        if hasattr(
            self,
            "txt_minimo"
        ):

            self.txt_minimo.delete(
                0,
                tk.END
            )

            self.txt_maximo.delete(
                0,
                tk.END
            )

            self.txt_puntos.delete(
                0,
                tk.END
            )


        if hasattr(
            self,
            "btn_guardar_rango"
        ):

            self.btn_guardar_rango.config(
                text="Agregar rango"
            )


    def cargar_alumnos(self):

        id_seccion = (
            self.obtener_id_seccion()
        )


        self.mapa_alumnos = {}

        self.cmb_alumno.set(
            ""
        )

        self.cmb_alumno[
            "values"
        ] = []


        if id_seccion is None:

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
                "Puntuación",
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


        alumnos = []

        if resultados:

            alumnos = resultados[0]


        valores = []


        for alumno in alumnos:

            texto = (
                f"{alumno['codigo']} - "
                f"{alumno['nombre']} "
                f"{alumno['apellido']} "
                f"({alumno['estado']})"
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


        if valores:

            self.cmb_alumno.current(
                0
            )


    def calcular(self):

        id_seccion = (
            self.obtener_id_seccion()
        )


        if id_seccion is None:

            messagebox.showwarning(
                "Puntuación",
                "Selecciona una sección."
            )

            return


        alumno_texto = (
            self.cmb_alumno
            .get()
            .strip()
        )


        if (
            alumno_texto
            not in self.mapa_alumnos
        ):

            messagebox.showwarning(
                "Puntuación",
                "Selecciona un alumno."
            )

            return


        id_alumno = (
            self.mapa_alumnos[
                alumno_texto
            ]
        )


        resultado_asistencia = (
            self.database
            .llamar_procedimiento(
                "CalcularAsistencia",
                (
                    id_alumno,
                    id_seccion
                )
            )
        )


        if resultado_asistencia is None:

            messagebox.showerror(
                "Puntuación",
                (
                    "No se pudo calcular "
                    "la asistencia.\n\n"
                    + str(
                        self.database
                        .obtener_ultimo_error()
                    )
                )
            )

            return


        if (
            not resultado_asistencia
            or not resultado_asistencia[0]
        ):

            messagebox.showwarning(
                "Puntuación",
                (
                    "No se obtuvo información "
                    "de asistencia."
                )
            )

            return


        asistencia = (
            resultado_asistencia[0][0]
        )


        self.lbl_total.config(
            text=asistencia[
                "total_clases"
            ]
        )

        self.lbl_presentes.config(
            text=asistencia[
                "presentes"
            ]
        )

        self.lbl_tardes.config(
            text=asistencia[
                "tardes"
            ]
        )

        self.lbl_justificadas.config(
            text=asistencia[
                "justificadas"
            ]
        )

        self.lbl_ausentes.config(
            text=asistencia[
                "ausentes"
            ]
        )

        self.lbl_fuera.config(
            text=asistencia[
                "fuera_tiempo"
            ]
        )

        self.lbl_validas.config(
            text=asistencia[
                "asistencias_validas"
            ]
        )

        self.lbl_porcentaje.config(
            text=(
                f"{asistencia['porcentaje']}%"
            )
        )


        resultado_puntos = (
            self.database
            .llamar_procedimiento(
                "CalcularPuntos",
                (
                    id_alumno,
                    id_seccion
                )
            )
        )


        if resultado_puntos is None:

            self.lbl_puntos.config(
                text="-"
            )

            messagebox.showerror(
                "Puntuación",
                (
                    "La asistencia fue calculada, "
                    "pero no se pudieron calcular "
                    "los puntos.\n\n"
                    + str(
                        self.database
                        .obtener_ultimo_error()
                    )
                )
            )

            return


        if (
            resultado_puntos
            and resultado_puntos[0]
        ):

            puntos = (
                resultado_puntos[0][0]
            )

            self.lbl_puntos.config(
                text=puntos["puntos"]
            )

        else:

            self.lbl_puntos.config(
                text="-"
            )


    def limpiar_resultados(self):

        controles = [
            self.lbl_total,
            self.lbl_presentes,
            self.lbl_tardes,
            self.lbl_justificadas,
            self.lbl_ausentes,
            self.lbl_fuera,
            self.lbl_validas,
            self.lbl_porcentaje,
            self.lbl_puntos
        ]


        for control in controles:

            control.config(
                text="-"
            )


    def limpiar_datos(self):

        self.datos_reglas = []
        self.datos_rangos = []

        self.mostrar_reglas([])
        self.mostrar_rangos([])

        self.cmb_alumno.set("")
        self.cmb_alumno["values"] = []

        self.limpiar_resultados()


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

        self.cargar_secciones()