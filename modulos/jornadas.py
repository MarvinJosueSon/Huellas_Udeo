import tkinter as tk
from tkinter import ttk, messagebox


class Jornadas(tk.Frame):

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
        self.datos_jornadas = []

        self.pack(
            fill="both",
            expand=True
        )

        self.crear_interfaz()
        self.cargar_jornadas()
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
            text="Jornadas",
            bg="#F3F3F3",
            fg="#202020",
            font=("Segoe UI", 24, "bold")
        ).pack(
            side="left"
        )


        tk.Button(
            encabezado,
            text="+ Nueva jornada",
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
            "nombre",
            text="Nombre de la jornada"
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
            "nombre",
            width=400
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
            width=330,
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
            text="Nueva jornada",
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
            text="Nombre de la jornada",
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
            text="Guardar jornada",
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


    def cargar_jornadas(self):

        resultados = (
            self.database
            .llamar_procedimiento(
                "ListarJornadas"
            )
        )


        if resultados is None:

            messagebox.showerror(
                "Jornadas",
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


        self.datos_jornadas = []


        if resultados:

            self.datos_jornadas = (
                resultados[0]
            )


        self.mostrar_datos(
            self.datos_jornadas
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


        for jornada in datos:

            self.tabla.insert(
                "",
                tk.END,
                values=(
                    jornada["id"],
                    jornada["nombre"],
                    jornada["estado"]
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


        for jornada in self.datos_jornadas:

            coincide_texto = (
                texto == ""
                or texto in jornada[
                    "nombre"
                ].lower()
            )


            coincide_estado = (
                estado == "TODAS"
                or jornada["estado"]
                == estado
            )


            if (
                coincide_texto
                and coincide_estado
            ):

                filtrados.append(
                    jornada
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
                "Jornadas",
                "Selecciona una jornada."
            )

            return None


        valores = self.tabla.item(
            seleccion[0],
            "values"
        )


        return {
            "id": int(valores[0]),
            "nombre": valores[1],
            "estado": valores[2]
        }


    def nueva(self):

        self.id_seleccionado = None


        self.lbl_titulo.config(
            text="Nueva jornada"
        )


        self.btn_guardar.config(
            text="Guardar jornada"
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


        self.txt_nombre.focus_set()


    def editar(
        self,
        event=None
    ):

        jornada = (
            self.obtener_seleccion()
        )


        if jornada is None:

            return


        self.id_seleccionado = (
            jornada["id"]
        )


        self.txt_nombre.delete(
            0,
            tk.END
        )

        self.txt_nombre.insert(
            0,
            jornada["nombre"]
        )


        self.lbl_titulo.config(
            text="Editar jornada"
        )


        self.btn_guardar.config(
            text="Guardar cambios"
        )


        self.txt_nombre.focus_set()


    def guardar(self):

        nombre = (
            self.txt_nombre
            .get()
            .strip()
        )


        if nombre == "":

            messagebox.showwarning(
                "Jornadas",
                (
                    "Ingresa el nombre "
                    "de la jornada."
                )
            )

            self.txt_nombre.focus_set()

            return


        if len(nombre) > 50:

            messagebox.showwarning(
                "Jornadas",
                (
                    "El nombre no puede "
                    "superar 50 caracteres."
                )
            )

            return


        if self.id_seleccionado is None:

            resultado = (
                self.database
                .llamar_procedimiento(
                    "CrearJornada",
                    (
                        nombre,
                    )
                )
            )


            if resultado is None:

                messagebox.showerror(
                    "Jornadas",
                    (
                        "No se pudo crear "
                        "la jornada.\n\n"
                        + str(
                            self.database
                            .obtener_ultimo_error()
                        )
                    )
                )

                return


            messagebox.showinfo(
                "Jornadas",
                "Jornada creada correctamente."
            )


        else:

            resultado = (
                self.database
                .llamar_procedimiento(
                    "ModificarJornada",
                    (
                        self.id_seleccionado,
                        nombre
                    )
                )
            )


            if resultado is None:

                messagebox.showerror(
                    "Jornadas",
                    (
                        "No se pudo modificar "
                        "la jornada.\n\n"
                        + str(
                            self.database
                            .obtener_ultimo_error()
                        )
                    )
                )

                return


            messagebox.showinfo(
                "Jornadas",
                (
                    "Jornada modificada "
                    "correctamente."
                )
            )


        self.cargar_jornadas()

        self.nueva()


    def inactivar(self):

        jornada = (
            self.obtener_seleccion()
        )


        if jornada is None:

            return


        if jornada["estado"] == "INACTIVA":

            messagebox.showinfo(
                "Jornadas",
                (
                    "La jornada ya se "
                    "encuentra inactiva."
                )
            )

            return


        confirmar = (
            messagebox.askyesno(
                "Inactivar jornada",
                (
                    "¿Deseas inactivar "
                    "la jornada?\n\n"
                    f"{jornada['nombre']}"
                )
            )
        )


        if not confirmar:

            return


        resultado = (
            self.database
            .llamar_procedimiento(
                "InactivarJornada",
                (
                    jornada["id"],
                )
            )
        )


        if resultado is None:

            messagebox.showerror(
                "Jornadas",
                (
                    "No se pudo inactivar "
                    "la jornada.\n\n"
                    + str(
                        self.database
                        .obtener_ultimo_error()
                    )
                )
            )

            return


        messagebox.showinfo(
            "Jornadas",
            "Jornada inactivada correctamente."
        )


        self.cargar_jornadas()

        self.nueva()


    def actualizar(self):

        self.cargar_jornadas()

        self.nueva()