import tkinter as tk
from tkinter import ttk, messagebox


class Cursos(tk.Frame):

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
        self.datos_cursos = []

        self.pack(
            fill="both",
            expand=True
        )

        self.crear_interfaz()
        self.cargar_cursos()
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
            text="Cursos",
            bg="#F3F3F3",
            fg="#202020",
            font=("Segoe UI", 24, "bold")
        ).pack(
            side="left"
        )


        tk.Button(
            encabezado,
            text="+ Nuevo curso",
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
            width=30
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
            weight=3
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
            text="Nombre del curso"
        )

        self.tabla.heading(
            "estado",
            text="Estado"
        )


        self.tabla.column(
            "id",
            width=60,
            anchor="center"
        )

        self.tabla.column(
            "codigo",
            width=140
        )

        self.tabla.column(
            "nombre",
            width=350
        )

        self.tabla.column(
            "estado",
            width=120,
            anchor="center"
        )


        scroll = ttk.Scrollbar(
            panel_tabla,
            orient="vertical",
            command=self.tabla.yview
        )

        self.tabla.configure(
            yscrollcommand=scroll.set
        )


        self.tabla.pack(
            side="left",
            fill="both",
            expand=True
        )

        scroll.pack(
            side="right",
            fill="y"
        )


        self.tabla.bind(
            "<Double-1>",
            self.editar
        )


        panel_formulario = tk.Frame(
            cuerpo,
            bg="#FFFFFF",
            width=340,
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
            text="Nuevo curso",
            bg="#FFFFFF",
            fg="#202020",
            font=("Segoe UI", 15, "bold")
        )

        self.lbl_titulo.pack(
            anchor="w",
            padx=20,
            pady=(20, 20)
        )


        tk.Label(
            panel_formulario,
            text="Código",
            bg="#FFFFFF",
            fg="#202020",
            font=("Segoe UI", 9)
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 5)
        )


        self.txt_codigo = ttk.Entry(
            panel_formulario
        )

        self.txt_codigo.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )


        tk.Label(
            panel_formulario,
            text="Nombre del curso",
            bg="#FFFFFF",
            fg="#202020",
            font=("Segoe UI", 9)
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 5)
        )


        self.txt_nombre = ttk.Entry(
            panel_formulario
        )

        self.txt_nombre.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )


        self.btn_guardar = tk.Button(
            panel_formulario,
            text="Guardar curso",
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


    def cargar_cursos(self):

        resultados = (
            self.database
            .llamar_procedimiento(
                "ListarCursos"
            )
        )


        if resultados is None:

            messagebox.showerror(
                "Cursos",
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


        self.datos_cursos = []


        if resultados:

            self.datos_cursos = (
                resultados[0]
            )


        self.mostrar_datos(
            self.datos_cursos
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


        for curso in datos:

            self.tabla.insert(
                "",
                tk.END,
                values=(
                    curso["id"],
                    curso["codigo"],
                    curso["nombre"],
                    curso["estado"]
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


        for curso in self.datos_cursos:

            codigo = (
                curso["codigo"]
                .lower()
            )

            nombre = (
                curso["nombre"]
                .lower()
            )


            coincide_texto = (
                texto == ""
                or texto in codigo
                or texto in nombre
            )


            coincide_estado = (
                estado == "TODOS"
                or curso["estado"]
                == estado
            )


            if (
                coincide_texto
                and coincide_estado
            ):

                filtrados.append(
                    curso
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
                "Cursos",
                "Selecciona un curso."
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
            "estado": valores[3]
        }


    def nuevo(self):

        self.id_seleccionado = None


        self.lbl_titulo.config(
            text="Nuevo curso"
        )


        self.btn_guardar.config(
            text="Guardar curso"
        )


        self.txt_codigo.delete(
            0,
            tk.END
        )

        self.txt_nombre.delete(
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

        curso = (
            self.obtener_seleccion()
        )


        if curso is None:

            return


        self.id_seleccionado = (
            curso["id"]
        )


        self.txt_codigo.delete(
            0,
            tk.END
        )

        self.txt_codigo.insert(
            0,
            curso["codigo"]
        )


        self.txt_nombre.delete(
            0,
            tk.END
        )

        self.txt_nombre.insert(
            0,
            curso["nombre"]
        )


        self.lbl_titulo.config(
            text="Editar curso"
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


        if codigo == "":

            messagebox.showwarning(
                "Cursos",
                "Ingresa el código del curso."
            )

            self.txt_codigo.focus_set()

            return None


        if len(codigo) > 30:

            messagebox.showwarning(
                "Cursos",
                (
                    "El código no puede "
                    "superar 30 caracteres."
                )
            )

            return None


        if nombre == "":

            messagebox.showwarning(
                "Cursos",
                "Ingresa el nombre del curso."
            )

            self.txt_nombre.focus_set()

            return None


        if len(nombre) > 100:

            messagebox.showwarning(
                "Cursos",
                (
                    "El nombre no puede "
                    "superar 100 caracteres."
                )
            )

            return None


        return {
            "codigo": codigo,
            "nombre": nombre
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
                    "CrearCurso",
                    (
                        datos["codigo"],
                        datos["nombre"]
                    )
                )
            )


            if resultado is None:

                messagebox.showerror(
                    "Cursos",
                    (
                        "No se pudo crear "
                        "el curso.\n\n"
                        + str(
                            self.database
                            .obtener_ultimo_error()
                        )
                    )
                )

                return


            messagebox.showinfo(
                "Cursos",
                "Curso creado correctamente."
            )


        else:

            resultado = (
                self.database
                .llamar_procedimiento(
                    "ModificarCurso",
                    (
                        self.id_seleccionado,
                        datos["codigo"],
                        datos["nombre"]
                    )
                )
            )


            if resultado is None:

                messagebox.showerror(
                    "Cursos",
                    (
                        "No se pudo modificar "
                        "el curso.\n\n"
                        + str(
                            self.database
                            .obtener_ultimo_error()
                        )
                    )
                )

                return


            messagebox.showinfo(
                "Cursos",
                "Curso modificado correctamente."
            )


        self.cargar_cursos()

        self.nuevo()


    def inactivar(self):

        curso = (
            self.obtener_seleccion()
        )


        if curso is None:

            return


        if curso["estado"] == "INACTIVO":

            messagebox.showinfo(
                "Cursos",
                (
                    "El curso ya se encuentra "
                    "inactivo."
                )
            )

            return


        confirmar = (
            messagebox.askyesno(
                "Inactivar curso",
                (
                    "¿Deseas inactivar "
                    "el curso?\n\n"
                    f"{curso['codigo']} - "
                    f"{curso['nombre']}"
                )
            )
        )


        if not confirmar:

            return


        resultado = (
            self.database
            .llamar_procedimiento(
                "InactivarCurso",
                (
                    curso["id"],
                )
            )
        )


        if resultado is None:

            messagebox.showerror(
                "Cursos",
                (
                    "No se pudo inactivar "
                    "el curso.\n\n"
                    + str(
                        self.database
                        .obtener_ultimo_error()
                    )
                )
            )

            return


        messagebox.showinfo(
            "Cursos",
            "Curso inactivado correctamente."
        )


        self.cargar_cursos()

        self.nuevo()


    def actualizar(self):

        self.cargar_cursos()

        self.nuevo()