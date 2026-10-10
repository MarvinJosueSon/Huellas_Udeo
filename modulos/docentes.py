import tkinter as tk
from tkinter import ttk, messagebox


class Docentes(tk.Frame):

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
        self.datos_docentes = []

        self.pack(
            fill="both",
            expand=True
        )

        self.crear_interfaz()
        self.cargar_docentes()
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
            text="Docentes",
            bg="#F3F3F3",
            fg="#202020",
            font=("Segoe UI", 24, "bold")
        ).pack(
            side="left"
        )


        tk.Button(
            encabezado,
            text="+ Nuevo docente",
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
                "ACTIVO",
                "INACTIVO"
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
            "id",
            "codigo",
            "nombre",
            "apellido",
            "correo",
            "usuario",
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
            "correo",
            text="Correo"
        )

        self.tabla.heading(
            "usuario",
            text="Usuario"
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
            "correo",
            width=220
        )

        self.tabla.column(
            "usuario",
            width=150
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
            width=350,
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
            text="Nuevo docente",
            bg="#FFFFFF",
            fg="#202020",
            font=("Segoe UI", 15, "bold")
        )

        self.lbl_titulo.pack(
            anchor="w",
            padx=20,
            pady=(20, 20)
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
            pady=(0, 15)
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
            pady=(0, 15)
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
            pady=(0, 20)
        )


        tk.Label(
            panel_formulario,
            text=(
                "El correo, usuario y contraseña "
                "se generan automáticamente."
            ),
            bg="#FFFFFF",
            fg="#666666",
            justify="left",
            wraplength=300,
            font=("Segoe UI", 9)
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 20)
        )


        self.btn_guardar = tk.Button(
            panel_formulario,
            text="Guardar docente",
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
            text="Restablecer contraseña",
            bg="#E5E5E5",
            fg="#202020",
            activebackground="#D5D5D5",
            relief="flat",
            bd=0,
            font=("Segoe UI", 10),
            cursor="hand2",
            command=self.restablecer_contrasena
        ).pack(
            side="left",
            padx=(0, 10),
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


    def cargar_docentes(self):

        resultados = (
            self.database
            .consultar(
                """
                SELECT
                    d.id,
                    d.codigo,
                    d.nombre,
                    d.apellido,
                    d.correo,
                    u.usuario,
                    d.estado
                FROM docentes d
                LEFT JOIN usuarios u
                    ON d.id_usuario = u.id
                ORDER BY d.nombre, d.apellido
                """
            )
        )


        if (
            not resultados
            and self.database.obtener_ultimo_error()
        ):

            messagebox.showerror(
                "Docentes",
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


        self.datos_docentes = (
            resultados
        )


        self.mostrar_datos(
            self.datos_docentes
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


        for docente in datos:

            self.tabla.insert(
                "",
                tk.END,
                values=(
                    docente["id"],
                    docente["codigo"],
                    docente["nombre"],
                    docente["apellido"],
                    docente["correo"],
                    docente["usuario"] or "",
                    docente["estado"]
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
            self.cmb_estado
            .get()
        )


        filtrados = []


        for docente in self.datos_docentes:

            codigo = str(
                docente["codigo"]
            ).lower()

            nombre = str(
                docente["nombre"]
            ).lower()

            apellido = str(
                docente["apellido"]
            ).lower()

            correo = str(
                docente["correo"]
            ).lower()

            usuario = str(
                docente["usuario"] or ""
            ).lower()


            coincide_texto = (
                texto == ""
                or texto in codigo
                or texto in nombre
                or texto in apellido
                or texto in correo
                or texto in usuario
            )


            coincide_estado = (
                estado == "TODOS"
                or docente["estado"] == estado
            )


            if (
                coincide_texto
                and coincide_estado
            ):

                filtrados.append(
                    docente
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
                "Docentes",
                "Selecciona un docente."
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
            "correo": valores[4],
            "usuario": valores[5],
            "estado": valores[6]
        }


    def nuevo(self):

        self.id_seleccionado = None


        self.lbl_titulo.config(
            text="Nuevo docente"
        )


        self.btn_guardar.config(
            text="Guardar docente"
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

        docente = (
            self.obtener_seleccion()
        )


        if docente is None:

            return


        self.id_seleccionado = (
            docente["id"]
        )


        self.txt_codigo.delete(
            0,
            tk.END
        )

        self.txt_codigo.insert(
            0,
            docente["codigo"]
        )


        self.txt_nombre.delete(
            0,
            tk.END
        )

        self.txt_nombre.insert(
            0,
            docente["nombre"]
        )


        self.txt_apellido.delete(
            0,
            tk.END
        )

        self.txt_apellido.insert(
            0,
            docente["apellido"]
        )


        self.lbl_titulo.config(
            text="Editar docente"
        )


        self.btn_guardar.config(
            text="Guardar cambios"
        )


        self.txt_codigo.focus_set()


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


        if codigo == "":

            messagebox.showwarning(
                "Docentes",
                "Ingresa el código del docente."
            )

            self.txt_codigo.focus_set()

            return None


        if len(codigo) > 30:

            messagebox.showwarning(
                "Docentes",
                (
                    "El código no puede superar "
                    "30 caracteres."
                )
            )

            return None


        if nombre == "":

            messagebox.showwarning(
                "Docentes",
                "Ingresa el nombre del docente."
            )

            self.txt_nombre.focus_set()

            return None


        if len(nombre) > 80:

            messagebox.showwarning(
                "Docentes",
                (
                    "El nombre no puede superar "
                    "80 caracteres."
                )
            )

            return None


        if apellido == "":

            messagebox.showwarning(
                "Docentes",
                "Ingresa el apellido del docente."
            )

            self.txt_apellido.focus_set()

            return None


        if len(apellido) > 80:

            messagebox.showwarning(
                "Docentes",
                (
                    "El apellido no puede superar "
                    "80 caracteres."
                )
            )

            return None


        return {
            "codigo": codigo,
            "nombre": nombre,
            "apellido": apellido
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
                    "CrearDocente",
                    (
                        datos["codigo"],
                        datos["nombre"],
                        datos["apellido"]
                    )
                )
            )


            if resultado is None:

                messagebox.showerror(
                    "Docentes",
                    (
                        "No se pudo crear "
                        "el docente.\n\n"
                        + str(
                            self.database
                            .obtener_ultimo_error()
                        )
                    )
                )

                return


            mensaje = (
                "Docente creado correctamente."
            )


            if resultado and resultado[0]:

                docente = resultado[0][0]

                mensaje += (
                    "\n\n"
                    f"Correo: {docente['correo']}\n"
                    f"Usuario: {docente['usuario']}\n"
                    f"Contraseña inicial: "
                    f"{docente['contrasena_inicial']}"
                )


            messagebox.showinfo(
                "Docentes",
                mensaje
            )


        else:

            resultado = (
                self.database
                .llamar_procedimiento(
                    "ModificarDocente",
                    (
                        self.id_seleccionado,
                        datos["codigo"],
                        datos["nombre"],
                        datos["apellido"]
                    )
                )
            )


            if resultado is None:

                messagebox.showerror(
                    "Docentes",
                    (
                        "No se pudo modificar "
                        "el docente.\n\n"
                        + str(
                            self.database
                            .obtener_ultimo_error()
                        )
                    )
                )

                return


            messagebox.showinfo(
                "Docentes",
                (
                    "Docente modificado "
                    "correctamente."
                )
            )


        self.cargar_docentes()

        self.nuevo()


    def inactivar(self):

        docente = (
            self.obtener_seleccion()
        )


        if docente is None:

            return


        if docente["estado"] == "INACTIVO":

            messagebox.showinfo(
                "Docentes",
                (
                    "El docente ya se encuentra "
                    "inactivo."
                )
            )

            return


        confirmar = (
            messagebox.askyesno(
                "Inactivar docente",
                (
                    "¿Deseas inactivar al docente?\n\n"
                    f"{docente['codigo']} - "
                    f"{docente['nombre']} "
                    f"{docente['apellido']}"
                )
            )
        )


        if not confirmar:

            return


        resultado = (
            self.database
            .llamar_procedimiento(
                "InactivarDocente",
                (
                    docente["id"],
                )
            )
        )


        if resultado is None:

            messagebox.showerror(
                "Docentes",
                (
                    "No se pudo inactivar "
                    "el docente.\n\n"
                    + str(
                        self.database
                        .obtener_ultimo_error()
                    )
                )
            )

            return


        messagebox.showinfo(
            "Docentes",
            (
                "Docente inactivado "
                "correctamente."
            )
        )


        self.cargar_docentes()

        self.nuevo()


    def restablecer_contrasena(self):

        docente = (
            self.obtener_seleccion()
        )


        if docente is None:

            return


        confirmar = (
            messagebox.askyesno(
                "Restablecer contraseña",
                (
                    "¿Deseas restablecer la "
                    "contraseña del docente?\n\n"
                    f"{docente['nombre']} "
                    f"{docente['apellido']}"
                )
            )
        )


        if not confirmar:

            return


        resultado = (
            self.database
            .llamar_procedimiento(
                "RestablecerContrasenaDocente",
                (
                    docente["id"],
                )
            )
        )


        if resultado is None:

            messagebox.showerror(
                "Docentes",
                (
                    "No se pudo restablecer "
                    "la contraseña.\n\n"
                    + str(
                        self.database
                        .obtener_ultimo_error()
                    )
                )
            )

            return


        if not resultado or not resultado[0]:

            messagebox.showerror(
                "Docentes",
                (
                    "La base de datos no devolvió "
                    "las nuevas credenciales."
                )
            )

            return


        credenciales = (
            resultado[0][0]
        )


        messagebox.showinfo(
            "Credenciales",
            (
                "Contraseña restablecida "
                "correctamente.\n\n"
                f"Usuario: "
                f"{credenciales['usuario']}\n"
                f"Contraseña: "
                f"{credenciales['contrasena_inicial']}"
            )
        )


    def actualizar(self):

        self.cargar_docentes()

        self.nuevo()