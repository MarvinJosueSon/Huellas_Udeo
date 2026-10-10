import tkinter as tk
from tkinter import ttk, messagebox


class Huellas(tk.Frame):

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

        self.datos_huellas = []
        self.datos_alumnos = []
        self.mapa_alumnos = {}

        self.pack(
            fill="both",
            expand=True
        )

        self.crear_interfaz()
        self.cargar_alumnos()
        self.cargar_huellas()
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
            text="Huellas",
            bg="#F3F3F3",
            fg="#202020",
            font=("Segoe UI", 24, "bold")
        ).pack(
            side="left"
        )


        tk.Button(
            encabezado,
            text="+ Registrar huella",
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


        self.cmb_estado = ttk.Combobox(
            panel_filtros,
            state="readonly",
            values=(
                "TODAS",
                "ACTIVA",
                "INACTIVA"
            ),
            width=15
        )

        self.cmb_estado.set(
            "TODAS"
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
            "id",
            "template",
            "codigo",
            "alumno",
            "dedo",
            "fecha",
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
            "template",
            text="Template"
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
            "dedo",
            text="Dedo"
        )

        self.tabla.heading(
            "fecha",
            text="Fecha registro"
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
            "template",
            width=90,
            anchor="center"
        )

        self.tabla.column(
            "codigo",
            width=110
        )

        self.tabla.column(
            "alumno",
            width=220
        )

        self.tabla.column(
            "dedo",
            width=130
        )

        self.tabla.column(
            "fecha",
            width=150,
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
            text="Registrar huella",
            bg="#FFFFFF",
            fg="#202020",
            font=("Segoe UI", 15, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 20)
        )


        self.crear_etiqueta(
            panel_formulario,
            "Alumno"
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


        self.crear_etiqueta(
            panel_formulario,
            "ID del template"
        )


        self.txt_template = ttk.Entry(
            panel_formulario
        )

        self.txt_template.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )


        self.crear_etiqueta(
            panel_formulario,
            "Dedo registrado"
        )


        self.txt_dedo = ttk.Entry(
            panel_formulario
        )

        self.txt_dedo.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )


        tk.Label(
            panel_formulario,
            text=(
                "El ID del template corresponde "
                "al identificador almacenado por "
                "el sensor de huella."
            ),
            bg="#FFFFFF",
            fg="#666666",
            justify="left",
            wraplength=310,
            font=("Segoe UI", 9)
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 20)
        )


        tk.Button(
            panel_formulario,
            text="Guardar huella",
            bg="#0078D4",
            fg="#FFFFFF",
            activebackground="#106EBE",
            activeforeground="#FFFFFF",
            relief="flat",
            bd=0,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            command=self.guardar
        ).pack(
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
            text="Desactivar huella",
            bg="#E5E5E5",
            fg="#202020",
            activebackground="#D5D5D5",
            relief="flat",
            bd=0,
            font=("Segoe UI", 10),
            cursor="hand2",
            command=self.desactivar
        ).pack(
            side="left",
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
            padx=10,
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


    def cargar_alumnos(self):

        resultados = (
            self.database
            .consultar(
                """
                SELECT
                    id,
                    codigo,
                    nombre,
                    apellido
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
                "Huellas",
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

        valores = []

        self.mapa_alumnos = {}


        for alumno in self.datos_alumnos:

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


    def cargar_huellas(self):

        resultados = (
            self.database
            .consultar(
                """
                SELECT
                    h.id,
                    h.id_template,
                    h.dedo,
                    h.fecha_registro,
                    h.estado,
                    a.codigo,
                    a.nombre,
                    a.apellido
                FROM huellas h
                INNER JOIN alumnos a
                    ON h.id_alumno = a.id
                ORDER BY
                    a.nombre,
                    a.apellido,
                    h.id_template
                """
            )
        )


        if (
            not resultados
            and self.database.obtener_ultimo_error()
        ):

            messagebox.showerror(
                "Huellas",
                (
                    "No se pudieron cargar "
                    "las huellas.\n\n"
                    + str(
                        self.database
                        .obtener_ultimo_error()
                    )
                )
            )

            return


        self.datos_huellas = resultados


        self.mostrar_datos(
            self.datos_huellas
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


        for huella in datos:

            nombre_alumno = (
                f"{huella['nombre']} "
                f"{huella['apellido']}"
            )


            self.tabla.insert(
                "",
                tk.END,
                values=(
                    huella["id"],
                    huella["id_template"],
                    huella["codigo"],
                    nombre_alumno,
                    huella["dedo"],
                    self.formatear_fecha(
                        huella["fecha_registro"]
                    ),
                    huella["estado"]
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


        for huella in self.datos_huellas:

            template = str(
                huella["id_template"]
            ).lower()

            codigo = str(
                huella["codigo"]
            ).lower()

            nombre = str(
                huella["nombre"]
            ).lower()

            apellido = str(
                huella["apellido"]
            ).lower()

            dedo = str(
                huella["dedo"]
            ).lower()


            coincide_texto = (
                texto == ""
                or texto in template
                or texto in codigo
                or texto in nombre
                or texto in apellido
                or texto in dedo
            )


            coincide_estado = (
                estado == "TODAS"
                or huella["estado"] == estado
            )


            if (
                coincide_texto
                and coincide_estado
            ):

                filtradas.append(
                    huella
                )


        self.mostrar_datos(
            filtradas
        )


    def nueva(self):

        self.cmb_alumno.set(
            ""
        )


        self.txt_template.delete(
            0,
            tk.END
        )


        self.txt_dedo.delete(
            0,
            tk.END
        )


        for fila in (
            self.tabla.selection()
        ):

            self.tabla.selection_remove(
                fila
            )


        self.cmb_alumno.focus_set()


    def validar_formulario(self):

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
                "Huellas",
                "Selecciona un alumno."
            )

            return None


        template_texto = (
            self.txt_template
            .get()
            .strip()
        )


        if template_texto == "":

            messagebox.showwarning(
                "Huellas",
                (
                    "Ingresa el ID "
                    "del template."
                )
            )

            return None


        try:

            id_template = int(
                template_texto
            )

        except ValueError:

            messagebox.showwarning(
                "Huellas",
                (
                    "El ID del template "
                    "debe ser un número entero."
                )
            )

            return None


        if id_template < 0:

            messagebox.showwarning(
                "Huellas",
                (
                    "El ID del template "
                    "no puede ser negativo."
                )
            )

            return None


        dedo = (
            self.txt_dedo
            .get()
            .strip()
        )


        if dedo == "":

            messagebox.showwarning(
                "Huellas",
                (
                    "Indica qué dedo "
                    "fue registrado."
                )
            )

            return None


        if len(dedo) > 30:

            messagebox.showwarning(
                "Huellas",
                (
                    "El nombre del dedo "
                    "no puede superar "
                    "30 caracteres."
                )
            )

            return None


        return {
            "id_alumno": self.mapa_alumnos[
                alumno_texto
            ],
            "id_template": id_template,
            "dedo": dedo
        }


    def guardar(self):

        datos = (
            self.validar_formulario()
        )


        if datos is None:

            return


        resultado = (
            self.database
            .llamar_procedimiento(
                "RegistrarHuella",
                (
                    datos["id_alumno"],
                    datos["id_template"],
                    datos["dedo"]
                )
            )
        )


        if resultado is None:

            messagebox.showerror(
                "Huellas",
                (
                    "No se pudo registrar "
                    "la huella.\n\n"
                    + str(
                        self.database
                        .obtener_ultimo_error()
                    )
                )
            )

            return


        messagebox.showinfo(
            "Huellas",
            (
                "Huella registrada "
                "correctamente."
            )
        )


        self.cargar_huellas()

        self.nueva()


    def obtener_seleccion(self):

        seleccion = (
            self.tabla.selection()
        )


        if not seleccion:

            messagebox.showwarning(
                "Huellas",
                "Selecciona una huella."
            )

            return None


        valores = self.tabla.item(
            seleccion[0],
            "values"
        )


        return {
            "id": int(
                valores[0]
            ),
            "id_template": int(
                valores[1]
            ),
            "codigo": valores[2],
            "alumno": valores[3],
            "dedo": valores[4],
            "fecha": valores[5],
            "estado": valores[6]
        }


    def desactivar(self):

        huella = (
            self.obtener_seleccion()
        )


        if huella is None:

            return


        if huella["estado"] == "INACTIVA":

            messagebox.showinfo(
                "Huellas",
                (
                    "La huella ya se encuentra "
                    "inactiva."
                )
            )

            return


        confirmar = (
            messagebox.askyesno(
                "Desactivar huella",
                (
                    "¿Deseas desactivar "
                    "esta huella?\n\n"
                    f"Alumno: "
                    f"{huella['alumno']}\n"
                    f"Template: "
                    f"{huella['id_template']}\n"
                    f"Dedo: "
                    f"{huella['dedo']}"
                )
            )
        )


        if not confirmar:

            return


        resultado = (
            self.database
            .llamar_procedimiento(
                "DesactivarHuella",
                (
                    huella["id_template"],
                )
            )
        )


        if resultado is None:

            messagebox.showerror(
                "Huellas",
                (
                    "No se pudo desactivar "
                    "la huella.\n\n"
                    + str(
                        self.database
                        .obtener_ultimo_error()
                    )
                )
            )

            return


        messagebox.showinfo(
            "Huellas",
            (
                "Huella desactivada "
                "correctamente."
            )
        )


        self.cargar_huellas()

        self.nueva()


    def actualizar(self):

        self.cargar_alumnos()
        self.cargar_huellas()
        self.nueva()