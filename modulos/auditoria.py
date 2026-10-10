import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class Auditoria(tk.Frame):

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

        self.datos_auditoria = []

        self.pack(
            fill="both",
            expand=True
        )

        self.crear_interfaz()
        self.cargar_auditoria()


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
            text="Auditoría",
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
            command=self.cargar_auditoria
        ).pack(
            side="right",
            ipadx=12,
            ipady=4
        )


        panel_filtros = tk.Frame(
            self,
            bg="#FFFFFF",
            highlightthickness=1,
            highlightbackground="#DDDDDD"
        )

        panel_filtros.pack(
            fill="x",
            padx=30,
            pady=(0, 15)
        )


        tk.Label(
            panel_filtros,
            text="Buscar:",
            bg="#FFFFFF",
            fg="#202020",
            font=("Segoe UI", 9)
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=(20, 5),
            pady=(12, 5)
        )


        self.txt_buscar = ttk.Entry(
            panel_filtros
        )

        self.txt_buscar.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=(20, 10),
            pady=(0, 15)
        )

        self.txt_buscar.bind(
            "<KeyRelease>",
            self.filtrar
        )


        tk.Label(
            panel_filtros,
            text="Tabla:",
            bg="#FFFFFF",
            fg="#202020",
            font=("Segoe UI", 9)
        ).grid(
            row=0,
            column=1,
            sticky="w",
            padx=5,
            pady=(12, 5)
        )


        self.cmb_tabla = ttk.Combobox(
            panel_filtros,
            state="readonly"
        )

        self.cmb_tabla.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=5,
            pady=(0, 15)
        )

        self.cmb_tabla.bind(
            "<<ComboboxSelected>>",
            self.filtrar
        )


        tk.Label(
            panel_filtros,
            text="Acción:",
            bg="#FFFFFF",
            fg="#202020",
            font=("Segoe UI", 9)
        ).grid(
            row=0,
            column=2,
            sticky="w",
            padx=5,
            pady=(12, 5)
        )


        self.cmb_accion = ttk.Combobox(
            panel_filtros,
            state="readonly"
        )

        self.cmb_accion.grid(
            row=1,
            column=2,
            sticky="ew",
            padx=5,
            pady=(0, 15)
        )

        self.cmb_accion.bind(
            "<<ComboboxSelected>>",
            self.filtrar
        )


        tk.Label(
            panel_filtros,
            text="Usuario:",
            bg="#FFFFFF",
            fg="#202020",
            font=("Segoe UI", 9)
        ).grid(
            row=0,
            column=3,
            sticky="w",
            padx=5,
            pady=(12, 5)
        )


        self.cmb_usuario = ttk.Combobox(
            panel_filtros,
            state="readonly"
        )

        self.cmb_usuario.grid(
            row=1,
            column=3,
            sticky="ew",
            padx=(5, 20),
            pady=(0, 15)
        )

        self.cmb_usuario.bind(
            "<<ComboboxSelected>>",
            self.filtrar
        )


        panel_filtros.grid_columnconfigure(
            0,
            weight=2
        )

        panel_filtros.grid_columnconfigure(
            1,
            weight=1
        )

        panel_filtros.grid_columnconfigure(
            2,
            weight=1
        )

        panel_filtros.grid_columnconfigure(
            3,
            weight=1
        )


        panel_info = tk.Frame(
            self,
            bg="#F3F3F3"
        )

        panel_info.pack(
            fill="x",
            padx=30,
            pady=(0, 8)
        )


        self.lbl_resultados = tk.Label(
            panel_info,
            text="Registros: 0",
            bg="#F3F3F3",
            fg="#666666",
            font=("Segoe UI", 9)
        )

        self.lbl_resultados.pack(
            side="left"
        )


        cuerpo = tk.Frame(
            self,
            bg="#F3F3F3"
        )

        cuerpo.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 20)
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
            weight=1
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
            "fecha",
            "usuario",
            "tabla",
            "registro",
            "accion",
            "motivo"
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
            "fecha",
            text="Fecha / hora"
        )

        self.tabla.heading(
            "usuario",
            text="Usuario"
        )

        self.tabla.heading(
            "tabla",
            text="Tabla"
        )

        self.tabla.heading(
            "registro",
            text="Registro"
        )

        self.tabla.heading(
            "accion",
            text="Acción"
        )

        self.tabla.heading(
            "motivo",
            text="Motivo"
        )


        self.tabla.column(
            "id",
            width=55,
            anchor="center"
        )

        self.tabla.column(
            "fecha",
            width=155,
            anchor="center"
        )

        self.tabla.column(
            "usuario",
            width=110
        )

        self.tabla.column(
            "tabla",
            width=150
        )

        self.tabla.column(
            "registro",
            width=80,
            anchor="center"
        )

        self.tabla.column(
            "accion",
            width=110,
            anchor="center"
        )

        self.tabla.column(
            "motivo",
            width=240
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
            "<<TreeviewSelect>>",
            self.mostrar_detalle
        )


        panel_detalle = tk.Frame(
            cuerpo,
            bg="#FFFFFF",
            width=340,
            highlightthickness=1,
            highlightbackground="#DDDDDD"
        )

        panel_detalle.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        panel_detalle.grid_propagate(
            False
        )


        tk.Label(
            panel_detalle,
            text="Detalle",
            bg="#FFFFFF",
            fg="#202020",
            font=("Segoe UI", 15, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 15)
        )


        tk.Label(
            panel_detalle,
            text="Valor anterior",
            bg="#FFFFFF",
            fg="#202020",
            font=("Segoe UI", 9)
        ).pack(
            anchor="w",
            padx=20
        )


        self.txt_anterior = tk.Text(
            panel_detalle,
            height=6,
            wrap="word",
            font=("Segoe UI", 9),
            state="disabled"
        )

        self.txt_anterior.pack(
            fill="x",
            padx=20,
            pady=(5, 15)
        )


        tk.Label(
            panel_detalle,
            text="Valor nuevo",
            bg="#FFFFFF",
            fg="#202020",
            font=("Segoe UI", 9)
        ).pack(
            anchor="w",
            padx=20
        )


        self.txt_nuevo = tk.Text(
            panel_detalle,
            height=6,
            wrap="word",
            font=("Segoe UI", 9),
            state="disabled"
        )

        self.txt_nuevo.pack(
            fill="x",
            padx=20,
            pady=(5, 15)
        )


        tk.Label(
            panel_detalle,
            text="Motivo",
            bg="#FFFFFF",
            fg="#202020",
            font=("Segoe UI", 9)
        ).pack(
            anchor="w",
            padx=20
        )


        self.txt_motivo = tk.Text(
            panel_detalle,
            height=5,
            wrap="word",
            font=("Segoe UI", 9),
            state="disabled"
        )

        self.txt_motivo.pack(
            fill="x",
            padx=20,
            pady=(5, 20)
        )


    def cargar_auditoria(self):

        resultados = (
            self.database
            .llamar_procedimiento(
                "ReporteAuditoria"
            )
        )


        if resultados is None:

            messagebox.showerror(
                "Auditoría",
                (
                    "No se pudo cargar "
                    "la auditoría.\n\n"
                    + str(
                        self.database
                        .obtener_ultimo_error()
                    )
                )
            )

            return


        self.datos_auditoria = []


        if resultados:

            self.datos_auditoria = (
                resultados[0]
            )


        self.cargar_filtros()

        self.mostrar_datos(
            self.datos_auditoria
        )

        self.limpiar_detalle()


    def cargar_filtros(self):

        tablas = sorted(
            {
                str(
                    registro[
                        "tabla_afectada"
                    ]
                )
                for registro
                in self.datos_auditoria
            }
        )


        acciones = sorted(
            {
                str(
                    registro[
                        "accion"
                    ]
                )
                for registro
                in self.datos_auditoria
            }
        )


        usuarios = sorted(
            {
                str(
                    registro[
                        "usuario"
                    ]
                )
                for registro
                in self.datos_auditoria
            }
        )


        self.cmb_tabla[
            "values"
        ] = [
            "TODAS"
        ] + tablas

        self.cmb_accion[
            "values"
        ] = [
            "TODAS"
        ] + acciones

        self.cmb_usuario[
            "values"
        ] = [
            "TODOS"
        ] + usuarios


        self.cmb_tabla.set(
            "TODAS"
        )

        self.cmb_accion.set(
            "TODAS"
        )

        self.cmb_usuario.set(
            "TODOS"
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


        for registro in datos:

            self.tabla.insert(
                "",
                tk.END,
                values=(
                    registro[
                        "id"
                    ],
                    self.formatear_fecha(
                        registro[
                            "fecha_hora"
                        ]
                    ),
                    registro[
                        "usuario"
                    ],
                    registro[
                        "tabla_afectada"
                    ],
                    registro[
                        "id_registro"
                    ],
                    registro[
                        "accion"
                    ],
                    registro[
                        "motivo"
                    ] or ""
                )
            )


        self.lbl_resultados.config(
            text=(
                f"Registros: "
                f"{len(datos)}"
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


        tabla = (
            self.cmb_tabla
            .get()
        )


        accion = (
            self.cmb_accion
            .get()
        )


        usuario = (
            self.cmb_usuario
            .get()
        )


        filtrados = []


        for registro in (
            self.datos_auditoria
        ):

            texto_registro = (
                " ".join(
                    [
                        str(
                            registro.get(
                                "id",
                                ""
                            )
                        ),
                        str(
                            registro.get(
                                "usuario",
                                ""
                            )
                        ),
                        str(
                            registro.get(
                                "tabla_afectada",
                                ""
                            )
                        ),
                        str(
                            registro.get(
                                "id_registro",
                                ""
                            )
                        ),
                        str(
                            registro.get(
                                "accion",
                                ""
                            )
                        ),
                        str(
                            registro.get(
                                "valor_anterior",
                                ""
                            )
                            or ""
                        ),
                        str(
                            registro.get(
                                "valor_nuevo",
                                ""
                            )
                            or ""
                        ),
                        str(
                            registro.get(
                                "motivo",
                                ""
                            )
                            or ""
                        ),
                        self.formatear_fecha(
                            registro.get(
                                "fecha_hora"
                            )
                        )
                    ]
                )
                .lower()
            )


            coincide_texto = (
                texto == ""
                or texto in texto_registro
            )


            coincide_tabla = (
                tabla == "TODAS"
                or registro[
                    "tabla_afectada"
                ] == tabla
            )


            coincide_accion = (
                accion == "TODAS"
                or registro[
                    "accion"
                ] == accion
            )


            coincide_usuario = (
                usuario == "TODOS"
                or registro[
                    "usuario"
                ] == usuario
            )


            if (
                coincide_texto
                and coincide_tabla
                and coincide_accion
                and coincide_usuario
            ):

                filtrados.append(
                    registro
                )


        self.mostrar_datos(
            filtrados
        )

        self.limpiar_detalle()


    def obtener_registro_seleccionado(
        self
    ):

        seleccion = (
            self.tabla.selection()
        )


        if not seleccion:

            return None


        valores = (
            self.tabla.item(
                seleccion[0],
                "values"
            )
        )


        if not valores:

            return None


        id_auditoria = int(
            valores[0]
        )


        for registro in (
            self.datos_auditoria
        ):

            if (
                registro["id"]
                == id_auditoria
            ):

                return registro


        return None


    def mostrar_detalle(
        self,
        event=None
    ):

        registro = (
            self.obtener_registro_seleccionado()
        )


        if registro is None:

            self.limpiar_detalle()

            return


        self.establecer_texto(
            self.txt_anterior,
            registro[
                "valor_anterior"
            ] or ""
        )


        self.establecer_texto(
            self.txt_nuevo,
            registro[
                "valor_nuevo"
            ] or ""
        )


        self.establecer_texto(
            self.txt_motivo,
            registro[
                "motivo"
            ] or ""
        )


    def limpiar_detalle(self):

        self.establecer_texto(
            self.txt_anterior,
            ""
        )

        self.establecer_texto(
            self.txt_nuevo,
            ""
        )

        self.establecer_texto(
            self.txt_motivo,
            ""
        )


    def establecer_texto(
        self,
        control,
        texto
    ):

        control.config(
            state="normal"
        )

        control.delete(
            "1.0",
            tk.END
        )

        control.insert(
            "1.0",
            str(
                texto
            )
        )

        control.config(
            state="disabled"
        )


    def formatear_fecha(
        self,
        fecha
    ):

        if fecha is None:

            return ""


        if isinstance(
            fecha,
            datetime
        ):

            return fecha.strftime(
                "%Y-%m-%d %H:%M:%S"
            )


        return str(
            fecha
        )