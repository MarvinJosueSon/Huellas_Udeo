import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class Sesiones(tk.Frame):

    def __init__(
        self,
        master,
        database,
        sesion
    ):
        super().__init__(
            master,
            bg="#F3F3F3"
        )

        self.database = database
        self.sesion = sesion

        self.datos_sesiones = []

        self.mapa_secciones = {}
        self.mapa_horarios = {}

        self.pack(
            fill="both",
            expand=True
        )

        self.crear_interfaz()
        self.cargar_secciones()
        self.cargar_sesiones()


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
            text="Sesiones de asistencia",
            bg="#F3F3F3",
            fg="#202020",
            font=("Segoe UI", 24, "bold")
        ).pack(
            side="left"
        )


        panel_apertura = tk.Frame(
            self,
            bg="#FFFFFF",
            highlightthickness=1,
            highlightbackground="#DDDDDD"
        )

        panel_apertura.pack(
            fill="x",
            padx=30,
            pady=(0, 15)
        )


        tk.Label(
            panel_apertura,
            text="Abrir nueva sesión",
            bg="#FFFFFF",
            fg="#202020",
            font=("Segoe UI", 14, "bold")
        ).grid(
            row=0,
            column=0,
            columnspan=4,
            sticky="w",
            padx=20,
            pady=(15, 12)
        )


        tk.Label(
            panel_apertura,
            text="Sección",
            bg="#FFFFFF",
            fg="#202020",
            font=("Segoe UI", 9)
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=(20, 5),
            pady=(0, 5)
        )


        self.cmb_seccion = ttk.Combobox(
            panel_apertura,
            state="readonly",
            width=45
        )

        self.cmb_seccion.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=(20, 10),
            pady=(0, 15)
        )

        self.cmb_seccion.bind(
            "<<ComboboxSelected>>",
            self.cambiar_seccion
        )


        tk.Label(
            panel_apertura,
            text="Horario",
            bg="#FFFFFF",
            fg="#202020",
            font=("Segoe UI", 9)
        ).grid(
            row=1,
            column=1,
            sticky="w",
            padx=5,
            pady=(0, 5)
        )


        self.cmb_horario = ttk.Combobox(
            panel_apertura,
            state="readonly",
            width=28
        )

        self.cmb_horario.grid(
            row=2,
            column=1,
            sticky="ew",
            padx=5,
            pady=(0, 15)
        )


        tk.Label(
            panel_apertura,
            text="Fecha (AAAA-MM-DD)",
            bg="#FFFFFF",
            fg="#202020",
            font=("Segoe UI", 9)
        ).grid(
            row=1,
            column=2,
            sticky="w",
            padx=5,
            pady=(0, 5)
        )


        self.txt_fecha = ttk.Entry(
            panel_apertura,
            width=18
        )

        self.txt_fecha.grid(
            row=2,
            column=2,
            sticky="ew",
            padx=5,
            pady=(0, 15)
        )

        self.txt_fecha.insert(
            0,
            datetime.now().strftime(
                "%Y-%m-%d"
            )
        )


        tk.Button(
            panel_apertura,
            text="Abrir sesión",
            bg="#0078D4",
            fg="#FFFFFF",
            activebackground="#106EBE",
            activeforeground="#FFFFFF",
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            command=self.abrir_sesion
        ).grid(
            row=2,
            column=3,
            padx=(15, 20),
            pady=(0, 15),
            ipadx=18,
            ipady=5
        )


        panel_apertura.grid_columnconfigure(
            0,
            weight=3
        )

        panel_apertura.grid_columnconfigure(
            1,
            weight=2
        )

        panel_apertura.grid_columnconfigure(
            2,
            weight=1
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
                "ABIERTA",
                "FINALIZADA",
                "CANCELADA"
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


        tk.Button(
            panel_filtros,
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


        panel_tabla = tk.Frame(
            self,
            bg="#FFFFFF",
            highlightthickness=1,
            highlightbackground="#DDDDDD"
        )

        panel_tabla.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 15)
        )


        columnas = (
            "id",
            "curso",
            "seccion",
            "fecha",
            "hora_inicio",
            "hora_fin",
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
            "fecha",
            text="Fecha"
        )

        self.tabla.heading(
            "hora_inicio",
            text="Inicio"
        )

        self.tabla.heading(
            "hora_fin",
            text="Fin"
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
            "curso",
            width=260
        )

        self.tabla.column(
            "seccion",
            width=90,
            anchor="center"
        )

        self.tabla.column(
            "fecha",
            width=110,
            anchor="center"
        )

        self.tabla.column(
            "hora_inicio",
            width=100,
            anchor="center"
        )

        self.tabla.column(
            "hora_fin",
            width=100,
            anchor="center"
        )

        self.tabla.column(
            "estado",
            width=110,
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
            text="Finalizar clase",
            bg="#E5E5E5",
            fg="#202020",
            activebackground="#D5D5D5",
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 10),
            command=self.finalizar
        ).pack(
            side="left",
            ipadx=15,
            ipady=5
        )


        tk.Button(
            panel_acciones,
            text="Cancelar sesión",
            bg="#E5E5E5",
            fg="#202020",
            activebackground="#D5D5D5",
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 10),
            command=self.cancelar
        ).pack(
            side="left",
            padx=10,
            ipadx=15,
            ipady=5
        )


        if self.sesion.es_superadmin():

            tk.Button(
                panel_acciones,
                text="Reabrir sesión",
                bg="#E5E5E5",
                fg="#202020",
                activebackground="#D5D5D5",
                relief="flat",
                bd=0,
                cursor="hand2",
                font=("Segoe UI", 10),
                command=self.reabrir
            ).pack(
                side="left",
                ipadx=15,
                ipady=5
            )


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
                "Sesiones",
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

            if seccion["estado"] != "ACTIVA":

                continue


            texto = (
                f"{seccion['id']} - "
                f"{seccion['curso']} - "
                f"Sección {seccion['seccion']} - "
                f"{seccion['periodo']} - "
                f"{seccion['jornada']}"
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

            self.cmb_horario.set(
                ""
            )

            self.cmb_horario[
                "values"
            ] = []

            self.mapa_horarios = {}

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


        self.cargar_horarios()


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

        self.cargar_horarios()


    def cargar_horarios(self):

        id_seccion = (
            self.obtener_id_seccion()
        )


        self.mapa_horarios = {}

        self.cmb_horario.set(
            ""
        )

        self.cmb_horario[
            "values"
        ] = []


        if id_seccion is None:

            return


        resultados = (
            self.database
            .llamar_procedimiento(
                "ListarHorariosSeccion",
                (
                    id_seccion,
                )
            )
        )


        if resultados is None:

            messagebox.showerror(
                "Sesiones",
                (
                    "No se pudieron cargar "
                    "los horarios.\n\n"
                    + str(
                        self.database
                        .obtener_ultimo_error()
                    )
                )
            )

            return


        horarios = []

        if resultados:

            horarios = resultados[0]


        valores = []


        for horario in horarios:

            if horario["estado"] != "ACTIVO":

                continue


            texto = (
                f"{horario['dia']} - "
                f"{self.formatear_hora(horario['hora_inicio'])}"
                f" a "
                f"{self.formatear_hora(horario['hora_fin'])}"
            )

            valores.append(
                texto
            )

            self.mapa_horarios[
                texto
            ] = horario["id"]


        self.cmb_horario[
            "values"
        ] = valores


        if valores:

            self.cmb_horario.current(
                0
            )


    def cargar_sesiones(self):

        resultados = (
            self.database
            .llamar_procedimiento(
                "ListarSesionesDocente"
            )
        )


        if resultados is None:

            messagebox.showerror(
                "Sesiones",
                (
                    "No se pudieron cargar "
                    "las sesiones.\n\n"
                    + str(
                        self.database
                        .obtener_ultimo_error()
                    )
                )
            )

            return


        self.datos_sesiones = []


        if resultados:

            self.datos_sesiones = (
                resultados[0]
            )


        self.mostrar_datos(
            self.datos_sesiones
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


        for sesion in datos:

            self.tabla.insert(
                "",
                tk.END,
                values=(
                    sesion["id"],
                    sesion["curso"],
                    sesion["seccion"],
                    self.formatear_fecha(
                        sesion["fecha"]
                    ),
                    self.formatear_hora(
                        sesion["hora_inicio"]
                    ),
                    self.formatear_hora(
                        sesion["hora_fin"]
                    ),
                    sesion["estado"]
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


    def formatear_hora(
        self,
        hora
    ):

        if hora is None:

            return ""


        if hasattr(
            hora,
            "total_seconds"
        ):

            segundos = int(
                hora.total_seconds()
            )

            horas = (
                segundos // 3600
            )

            minutos = (
                segundos % 3600
            ) // 60

            return (
                f"{horas:02d}:"
                f"{minutos:02d}"
            )


        texto = str(
            hora
        )


        if len(texto) >= 5:

            return texto[:5]


        return texto


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


        for sesion in self.datos_sesiones:

            curso = str(
                sesion["curso"]
            ).lower()

            seccion = str(
                sesion["seccion"]
            ).lower()

            fecha = self.formatear_fecha(
                sesion["fecha"]
            ).lower()


            coincide_texto = (
                texto == ""
                or texto in curso
                or texto in seccion
                or texto in fecha
            )


            coincide_estado = (
                estado == "TODAS"
                or sesion["estado"] == estado
            )


            if (
                coincide_texto
                and coincide_estado
            ):

                filtradas.append(
                    sesion
                )


        self.mostrar_datos(
            filtradas
        )


    def abrir_sesion(self):

        id_seccion = (
            self.obtener_id_seccion()
        )


        if id_seccion is None:

            messagebox.showwarning(
                "Sesiones",
                "Selecciona una sección."
            )

            return


        horario_texto = (
            self.cmb_horario
            .get()
            .strip()
        )


        if (
            horario_texto
            not in self.mapa_horarios
        ):

            messagebox.showwarning(
                "Sesiones",
                "Selecciona un horario."
            )

            return


        fecha = (
            self.txt_fecha
            .get()
            .strip()
        )


        try:

            datetime.strptime(
                fecha,
                "%Y-%m-%d"
            )

        except ValueError:

            messagebox.showwarning(
                "Sesiones",
                (
                    "La fecha debe utilizar "
                    "el formato AAAA-MM-DD."
                )
            )

            return


        id_horario = (
            self.mapa_horarios[
                horario_texto
            ]
        )


        resultado = (
            self.database
            .llamar_procedimiento(
                "AbrirSesion",
                (
                    id_seccion,
                    id_horario,
                    fecha
                )
            )
        )


        if resultado is None:

            messagebox.showerror(
                "Sesiones",
                (
                    "No se pudo abrir "
                    "la sesión.\n\n"
                    + str(
                        self.database
                        .obtener_ultimo_error()
                    )
                )
            )

            return


        messagebox.showinfo(
            "Sesiones",
            (
                "Sesión abierta "
                "correctamente."
            )
        )


        self.cargar_sesiones()


    def obtener_seleccion(self):

        seleccion = (
            self.tabla.selection()
        )


        if not seleccion:

            messagebox.showwarning(
                "Sesiones",
                "Selecciona una sesión."
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
            "curso": valores[1],
            "seccion": valores[2],
            "fecha": valores[3],
            "hora_inicio": valores[4],
            "hora_fin": valores[5],
            "estado": valores[6]
        }


    def finalizar(self):

        sesion = (
            self.obtener_seleccion()
        )


        if sesion is None:

            return


        if sesion["estado"] != "ABIERTA":

            messagebox.showinfo(
                "Sesiones",
                (
                    "Solo se puede finalizar "
                    "una sesión abierta."
                )
            )

            return


        ventana = tk.Toplevel(
            self
        )

        ventana.title(
            "Finalizar clase"
        )

        ventana.geometry(
            "400x240"
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
            text="Finalizar clase",
            font=("Segoe UI", 15, "bold")
        ).pack(
            pady=(20, 5)
        )


        tk.Label(
            ventana,
            text=(
                f"{sesion['curso']} - "
                f"Sección {sesion['seccion']}"
            ),
            font=("Segoe UI", 10)
        ).pack(
            pady=(0, 15)
        )


        tk.Label(
            ventana,
            text=(
                "Fecha y hora final "
                "(AAAA-MM-DD HH:MM:SS)"
            ),
            font=("Segoe UI", 9)
        ).pack()


        txt_fecha_hora = ttk.Entry(
            ventana,
            width=28
        )

        txt_fecha_hora.pack(
            pady=(5, 20)
        )

        txt_fecha_hora.insert(
            0,
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )


        def confirmar_finalizacion():

            fecha_hora = (
                txt_fecha_hora
                .get()
                .strip()
            )


            try:

                datetime.strptime(
                    fecha_hora,
                    "%Y-%m-%d %H:%M:%S"
                )

            except ValueError:

                messagebox.showwarning(
                    "Sesiones",
                    (
                        "Utiliza el formato "
                        "AAAA-MM-DD HH:MM:SS."
                    ),
                    parent=ventana
                )

                return


            resultado = (
                self.database
                .llamar_procedimiento(
                    "FinalizarClase",
                    (
                        sesion["id"],
                        fecha_hora
                    )
                )
            )


            if resultado is None:

                messagebox.showerror(
                    "Sesiones",
                    (
                        "No se pudo finalizar "
                        "la clase.\n\n"
                        + str(
                            self.database
                            .obtener_ultimo_error()
                        )
                    ),
                    parent=ventana
                )

                return


            messagebox.showinfo(
                "Sesiones",
                (
                    "Clase finalizada "
                    "correctamente."
                ),
                parent=ventana
            )


            ventana.destroy()

            self.cargar_sesiones()


        tk.Button(
            ventana,
            text="Finalizar clase",
            bg="#0078D4",
            fg="#FFFFFF",
            activebackground="#106EBE",
            activeforeground="#FFFFFF",
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            command=confirmar_finalizacion
        ).pack(
            ipadx=20,
            ipady=5
        )


    def cancelar(self):

        sesion = (
            self.obtener_seleccion()
        )


        if sesion is None:

            return


        if sesion["estado"] != "ABIERTA":

            messagebox.showinfo(
                "Sesiones",
                (
                    "Solo se puede cancelar "
                    "una sesión abierta."
                )
            )

            return


        ventana = tk.Toplevel(
            self
        )

        ventana.title(
            "Cancelar sesión"
        )

        ventana.geometry(
            "430x260"
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
            text="Cancelar sesión",
            font=("Segoe UI", 15, "bold")
        ).pack(
            pady=(20, 5)
        )


        tk.Label(
            ventana,
            text=(
                f"{sesion['curso']} - "
                f"Sección {sesion['seccion']}"
            ),
            font=("Segoe UI", 10)
        ).pack(
            pady=(0, 15)
        )


        tk.Label(
            ventana,
            text="Motivo",
            font=("Segoe UI", 9)
        ).pack()


        txt_motivo = ttk.Entry(
            ventana,
            width=45
        )

        txt_motivo.pack(
            pady=(5, 20)
        )


        def confirmar_cancelacion():

            motivo = (
                txt_motivo
                .get()
                .strip()
            )


            resultado = (
                self.database
                .llamar_procedimiento(
                    "CancelarSesion",
                    (
                        sesion["id"],
                        motivo
                    )
                )
            )


            if resultado is None:

                messagebox.showerror(
                    "Sesiones",
                    (
                        "No se pudo cancelar "
                        "la sesión.\n\n"
                        + str(
                            self.database
                            .obtener_ultimo_error()
                        )
                    ),
                    parent=ventana
                )

                return


            messagebox.showinfo(
                "Sesiones",
                (
                    "Sesión cancelada "
                    "correctamente."
                ),
                parent=ventana
            )


            ventana.destroy()

            self.cargar_sesiones()


        tk.Button(
            ventana,
            text="Cancelar sesión",
            bg="#0078D4",
            fg="#FFFFFF",
            activebackground="#106EBE",
            activeforeground="#FFFFFF",
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            command=confirmar_cancelacion
        ).pack(
            ipadx=20,
            ipady=5
        )


    def reabrir(self):

        sesion = (
            self.obtener_seleccion()
        )


        if sesion is None:

            return


        if sesion["estado"] != "FINALIZADA":

            messagebox.showinfo(
                "Sesiones",
                (
                    "Solo se puede reabrir "
                    "una sesión finalizada."
                )
            )

            return


        ventana = tk.Toplevel(
            self
        )

        ventana.title(
            "Reabrir sesión"
        )

        ventana.geometry(
            "430x260"
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
            text="Reabrir sesión",
            font=("Segoe UI", 15, "bold")
        ).pack(
            pady=(20, 5)
        )


        tk.Label(
            ventana,
            text=(
                f"{sesion['curso']} - "
                f"Sección {sesion['seccion']}"
            ),
            font=("Segoe UI", 10)
        ).pack(
            pady=(0, 15)
        )


        tk.Label(
            ventana,
            text="Motivo de reapertura",
            font=("Segoe UI", 9)
        ).pack()


        txt_motivo = ttk.Entry(
            ventana,
            width=45
        )

        txt_motivo.pack(
            pady=(5, 20)
        )


        def confirmar_reapertura():

            motivo = (
                txt_motivo
                .get()
                .strip()
            )


            if motivo == "":

                messagebox.showwarning(
                    "Sesiones",
                    (
                        "Debes indicar el motivo "
                        "de reapertura."
                    ),
                    parent=ventana
                )

                return


            resultado = (
                self.database
                .llamar_procedimiento(
                    "ReabrirSesion",
                    (
                        sesion["id"],
                        motivo
                    )
                )
            )


            if resultado is None:

                messagebox.showerror(
                    "Sesiones",
                    (
                        "No se pudo reabrir "
                        "la sesión.\n\n"
                        + str(
                            self.database
                            .obtener_ultimo_error()
                        )
                    ),
                    parent=ventana
                )

                return


            messagebox.showinfo(
                "Sesiones",
                (
                    "Sesión reabierta "
                    "correctamente."
                ),
                parent=ventana
            )


            ventana.destroy()

            self.cargar_sesiones()


        tk.Button(
            ventana,
            text="Reabrir sesión",
            bg="#0078D4",
            fg="#FFFFFF",
            activebackground="#106EBE",
            activeforeground="#FFFFFF",
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            command=confirmar_reapertura
        ).pack(
            ipadx=20,
            ipady=5
        )


    def actualizar(self):

        self.cargar_secciones()
        self.cargar_sesiones()