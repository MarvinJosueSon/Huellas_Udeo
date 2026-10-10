import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class Periodos(tk.Frame):

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
        self.datos_periodos = []

        self.pack(
            fill="both",
            expand=True
        )

        self.crear_interfaz()
        self.cargar_periodos()
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
            text="Periodos académicos",
            bg="#F3F3F3",
            fg="#202020",
            font=("Segoe UI", 24, "bold")
        ).pack(
            side="left"
        )


        tk.Button(
            encabezado,
            text="+ Nuevo periodo",
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


        self.cmb_estado_filtro = ttk.Combobox(
            panel_filtros,
            state="readonly",
            values=(
                "TODOS",
                "ACTIVO",
                "FINALIZADO",
                "INACTIVO"
            ),
            width=15
        )

        self.cmb_estado_filtro.set(
            "TODOS"
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
            "fecha_inicio",
            "fecha_fin",
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
            text="Periodo"
        )

        self.tabla.heading(
            "fecha_inicio",
            text="Fecha inicio"
        )

        self.tabla.heading(
            "fecha_fin",
            text="Fecha fin"
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
            "nombre",
            width=250
        )

        self.tabla.column(
            "fecha_inicio",
            width=120,
            anchor="center"
        )

        self.tabla.column(
            "fecha_fin",
            width=120,
            anchor="center"
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
            text="Nuevo periodo",
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
            "Nombre del periodo"
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
            "Fecha inicio (AAAA-MM-DD)"
        )

        self.txt_fecha_inicio = ttk.Entry(
            panel_formulario
        )

        self.txt_fecha_inicio.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )


        self.crear_etiqueta(
            panel_formulario,
            "Fecha fin (AAAA-MM-DD)"
        )

        self.txt_fecha_fin = ttk.Entry(
            panel_formulario
        )

        self.txt_fecha_fin.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )


        self.btn_guardar = tk.Button(
            panel_formulario,
            text="Guardar periodo",
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
            text="Cambiar estado",
            bg="#E5E5E5",
            fg="#202020",
            activebackground="#D5D5D5",
            relief="flat",
            bd=0,
            font=("Segoe UI", 10),
            cursor="hand2",
            command=self.cambiar_estado
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


    def cargar_periodos(self):

        resultados = (
            self.database
            .llamar_procedimiento(
                "ListarPeriodos"
            )
        )


        if resultados is None:

            messagebox.showerror(
                "Periodos",
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


        self.datos_periodos = []


        if resultados:

            self.datos_periodos = (
                resultados[0]
            )


        self.mostrar_datos(
            self.datos_periodos
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


        for periodo in datos:

            fecha_inicio = (
                self.formatear_fecha(
                    periodo["fecha_inicio"]
                )
            )

            fecha_fin = (
                self.formatear_fecha(
                    periodo["fecha_fin"]
                )
            )


            self.tabla.insert(
                "",
                tk.END,
                values=(
                    periodo["id"],
                    periodo["nombre"],
                    fecha_inicio,
                    fecha_fin,
                    periodo["estado"]
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

            return str(fecha)


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


        for periodo in self.datos_periodos:

            nombre = (
                periodo["nombre"]
                .lower()
            )

            fecha_inicio = (
                self.formatear_fecha(
                    periodo["fecha_inicio"]
                )
                .lower()
            )

            fecha_fin = (
                self.formatear_fecha(
                    periodo["fecha_fin"]
                )
                .lower()
            )


            coincide_texto = (
                texto == ""
                or texto in nombre
                or texto in fecha_inicio
                or texto in fecha_fin
            )


            coincide_estado = (
                estado == "TODOS"
                or periodo["estado"]
                == estado
            )


            if (
                coincide_texto
                and coincide_estado
            ):

                filtrados.append(
                    periodo
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
                "Periodos",
                "Selecciona un periodo."
            )

            return None


        valores = self.tabla.item(
            seleccion[0],
            "values"
        )


        return {
            "id": int(valores[0]),
            "nombre": valores[1],
            "fecha_inicio": valores[2],
            "fecha_fin": valores[3],
            "estado": valores[4]
        }


    def nuevo(self):

        self.id_seleccionado = None


        self.lbl_titulo.config(
            text="Nuevo periodo"
        )


        self.btn_guardar.config(
            text="Guardar periodo"
        )


        self.txt_nombre.delete(
            0,
            tk.END
        )

        self.txt_fecha_inicio.delete(
            0,
            tk.END
        )

        self.txt_fecha_fin.delete(
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

        periodo = (
            self.obtener_seleccion()
        )


        if periodo is None:

            return


        self.id_seleccionado = (
            periodo["id"]
        )


        self.txt_nombre.delete(
            0,
            tk.END
        )

        self.txt_nombre.insert(
            0,
            periodo["nombre"]
        )


        self.txt_fecha_inicio.delete(
            0,
            tk.END
        )

        self.txt_fecha_inicio.insert(
            0,
            periodo["fecha_inicio"]
        )


        self.txt_fecha_fin.delete(
            0,
            tk.END
        )

        self.txt_fecha_fin.insert(
            0,
            periodo["fecha_fin"]
        )


        self.lbl_titulo.config(
            text="Editar periodo"
        )


        self.btn_guardar.config(
            text="Guardar cambios"
        )


    def validar_formulario(self):

        nombre = (
            self.txt_nombre
            .get()
            .strip()
        )

        fecha_inicio = (
            self.txt_fecha_inicio
            .get()
            .strip()
        )

        fecha_fin = (
            self.txt_fecha_fin
            .get()
            .strip()
        )


        if nombre == "":

            messagebox.showwarning(
                "Periodos",
                "Ingresa el nombre del periodo."
            )

            return None


        if len(nombre) > 80:

            messagebox.showwarning(
                "Periodos",
                (
                    "El nombre no puede "
                    "superar 80 caracteres."
                )
            )

            return None


        try:

            inicio = datetime.strptime(
                fecha_inicio,
                "%Y-%m-%d"
            ).date()

        except ValueError:

            messagebox.showwarning(
                "Periodos",
                (
                    "La fecha de inicio debe usar "
                    "el formato AAAA-MM-DD."
                )
            )

            return None


        try:

            fin = datetime.strptime(
                fecha_fin,
                "%Y-%m-%d"
            ).date()

        except ValueError:

            messagebox.showwarning(
                "Periodos",
                (
                    "La fecha final debe usar "
                    "el formato AAAA-MM-DD."
                )
            )

            return None


        if fin < inicio:

            messagebox.showwarning(
                "Periodos",
                (
                    "La fecha final no puede ser "
                    "menor que la fecha inicial."
                )
            )

            return None


        return {
            "nombre": nombre,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin
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
                    "CrearPeriodo",
                    (
                        datos["nombre"],
                        datos["fecha_inicio"],
                        datos["fecha_fin"]
                    )
                )
            )


            if resultado is None:

                messagebox.showerror(
                    "Periodos",
                    (
                        "No se pudo crear "
                        "el periodo.\n\n"
                        + str(
                            self.database
                            .obtener_ultimo_error()
                        )
                    )
                )

                return


            messagebox.showinfo(
                "Periodos",
                "Periodo creado correctamente."
            )


        else:

            resultado = (
                self.database
                .llamar_procedimiento(
                    "ModificarPeriodo",
                    (
                        self.id_seleccionado,
                        datos["nombre"],
                        datos["fecha_inicio"],
                        datos["fecha_fin"]
                    )
                )
            )


            if resultado is None:

                messagebox.showerror(
                    "Periodos",
                    (
                        "No se pudo modificar "
                        "el periodo.\n\n"
                        + str(
                            self.database
                            .obtener_ultimo_error()
                        )
                    )
                )

                return


            messagebox.showinfo(
                "Periodos",
                (
                    "Periodo modificado "
                    "correctamente."
                )
            )


        self.cargar_periodos()

        self.nuevo()


    def cambiar_estado(self):

        periodo = (
            self.obtener_seleccion()
        )


        if periodo is None:

            return


        ventana = tk.Toplevel(
            self
        )

        ventana.title(
            "Cambiar estado"
        )

        ventana.geometry(
            "350x210"
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
            text="Cambiar estado del periodo",
            font=("Segoe UI", 13, "bold")
        ).pack(
            pady=(20, 10)
        )


        tk.Label(
            ventana,
            text=periodo["nombre"],
            font=("Segoe UI", 10)
        ).pack(
            pady=(0, 15)
        )


        cmb_nuevo_estado = ttk.Combobox(
            ventana,
            state="readonly",
            values=(
                "ACTIVO",
                "FINALIZADO",
                "INACTIVO"
            ),
            width=20
        )

        cmb_nuevo_estado.set(
            periodo["estado"]
        )

        cmb_nuevo_estado.pack(
            pady=(0, 20)
        )


        def guardar_estado():

            nuevo_estado = (
                cmb_nuevo_estado.get()
            )


            if nuevo_estado == periodo["estado"]:

                ventana.destroy()

                return


            resultado = (
                self.database
                .llamar_procedimiento(
                    "CambiarEstadoPeriodo",
                    (
                        periodo["id"],
                        nuevo_estado
                    )
                )
            )


            if resultado is None:

                messagebox.showerror(
                    "Periodos",
                    (
                        "No se pudo cambiar "
                        "el estado.\n\n"
                        + str(
                            self.database
                            .obtener_ultimo_error()
                        )
                    ),
                    parent=ventana
                )

                return


            messagebox.showinfo(
                "Periodos",
                "Estado actualizado correctamente.",
                parent=ventana
            )


            ventana.destroy()

            self.cargar_periodos()

            self.nuevo()


        tk.Button(
            ventana,
            text="Guardar",
            bg="#0078D4",
            fg="#FFFFFF",
            activebackground="#106EBE",
            activeforeground="#FFFFFF",
            relief="flat",
            bd=0,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            command=guardar_estado
        ).pack(
            ipadx=25,
            ipady=5
        )


    def actualizar(self):

        self.cargar_periodos()

        self.nuevo()