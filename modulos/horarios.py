import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class Horarios(tk.Frame):

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
        self.datos_horarios = []

        self.mapa_secciones = {}

        self.pack(
            fill="both",
            expand=True
        )

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
            text="Horarios",
            bg="#F3F3F3",
            fg="#202020",
            font=("Segoe UI", 24, "bold")
        ).pack(
            side="left"
        )


        tk.Button(
            encabezado,
            text="+ Nuevo horario",
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


        panel_seccion = tk.Frame(
            self,
            bg="#F3F3F3"
        )

        panel_seccion.pack(
            fill="x",
            padx=30,
            pady=(0, 15)
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
            width=55
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
            font=("Segoe UI", 9),
            cursor="hand2",
            command=self.actualizar
        ).pack(
            side="left",
            ipadx=12,
            ipady=4
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
            "dia",
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
            "dia",
            text="Día"
        )

        self.tabla.heading(
            "hora_inicio",
            text="Hora inicio"
        )

        self.tabla.heading(
            "hora_fin",
            text="Hora fin"
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
            "dia",
            width=160,
            anchor="center"
        )

        self.tabla.column(
            "hora_inicio",
            width=130,
            anchor="center"
        )

        self.tabla.column(
            "hora_fin",
            width=130,
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
            text="Nuevo horario",
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
            "Día"
        )


        self.cmb_dia = ttk.Combobox(
            panel_formulario,
            state="readonly",
            values=(
                "LUNES",
                "MARTES",
                "MIERCOLES",
                "JUEVES",
                "VIERNES",
                "SABADO",
                "DOMINGO"
            )
        )

        self.cmb_dia.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )


        self.crear_etiqueta(
            panel_formulario,
            "Hora inicio (HH:MM)"
        )


        self.txt_hora_inicio = ttk.Entry(
            panel_formulario
        )

        self.txt_hora_inicio.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )


        self.crear_etiqueta(
            panel_formulario,
            "Hora fin (HH:MM)"
        )


        self.txt_hora_fin = ttk.Entry(
            panel_formulario
        )

        self.txt_hora_fin.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )


        self.btn_guardar = tk.Button(
            panel_formulario,
            text="Guardar horario",
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


    def cargar_secciones(self):

        seccion_actual = self.obtener_id_seccion_actual()

        resultados = (
            self.database
            .llamar_procedimiento(
                "ListarSeccionesDocente"
            )
        )


        if resultados is None:

            messagebox.showerror(
                "Horarios",
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

            self.limpiar_tabla()

            return


        seleccionado = False


        if seccion_actual is not None:

            for texto, identificador in (
                self.mapa_secciones.items()
            ):

                if identificador == seccion_actual:

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


    def obtener_id_seccion_actual(self):

        texto = (
            self.cmb_seccion.get()
            if hasattr(
                self,
                "cmb_seccion"
            )
            else ""
        )


        return self.mapa_secciones.get(
            texto
        )


    def cambiar_seccion(
        self,
        event=None
    ):

        self.nuevo()
        self.cargar_horarios()


    def cargar_horarios(self):

        id_seccion = (
            self.obtener_id_seccion_actual()
        )


        if id_seccion is None:

            self.datos_horarios = []

            self.limpiar_tabla()

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
                "Horarios",
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


        self.datos_horarios = []


        if resultados:

            self.datos_horarios = (
                resultados[0]
            )


        self.mostrar_datos(
            self.datos_horarios
        )


    def limpiar_tabla(self):

        for fila in (
            self.tabla.get_children()
        ):

            self.tabla.delete(
                fila
            )


    def mostrar_datos(
        self,
        datos
    ):

        self.limpiar_tabla()


        for horario in datos:

            self.tabla.insert(
                "",
                tk.END,
                values=(
                    horario["id"],
                    horario["dia"],
                    self.formatear_hora(
                        horario["hora_inicio"]
                    ),
                    self.formatear_hora(
                        horario["hora_fin"]
                    ),
                    horario["estado"]
                )
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


    def obtener_seleccion(self):

        seleccion = (
            self.tabla.selection()
        )


        if not seleccion:

            messagebox.showwarning(
                "Horarios",
                "Selecciona un horario."
            )

            return None


        valores = self.tabla.item(
            seleccion[0],
            "values"
        )


        return {
            "id": int(valores[0]),
            "dia": valores[1],
            "hora_inicio": valores[2],
            "hora_fin": valores[3],
            "estado": valores[4]
        }


    def nuevo(self):

        self.id_seleccionado = None


        self.lbl_titulo.config(
            text="Nuevo horario"
        )


        self.btn_guardar.config(
            text="Guardar horario"
        )


        self.cmb_dia.set(
            ""
        )


        self.txt_hora_inicio.delete(
            0,
            tk.END
        )


        self.txt_hora_fin.delete(
            0,
            tk.END
        )


        for fila in (
            self.tabla.selection()
        ):

            self.tabla.selection_remove(
                fila
            )


    def editar(
        self,
        event=None
    ):

        horario = (
            self.obtener_seleccion()
        )


        if horario is None:

            return


        self.id_seleccionado = (
            horario["id"]
        )


        self.cmb_dia.set(
            horario["dia"]
        )


        self.txt_hora_inicio.delete(
            0,
            tk.END
        )

        self.txt_hora_inicio.insert(
            0,
            horario["hora_inicio"]
        )


        self.txt_hora_fin.delete(
            0,
            tk.END
        )

        self.txt_hora_fin.insert(
            0,
            horario["hora_fin"]
        )


        self.lbl_titulo.config(
            text="Editar horario"
        )


        self.btn_guardar.config(
            text="Guardar cambios"
        )


    def validar_hora(
        self,
        texto
    ):

        try:

            hora = datetime.strptime(
                texto,
                "%H:%M"
            )

            return hora.strftime(
                "%H:%M:%S"
            )

        except ValueError:

            try:

                hora = datetime.strptime(
                    texto,
                    "%H:%M:%S"
                )

                return hora.strftime(
                    "%H:%M:%S"
                )

            except ValueError:

                return None


    def validar_formulario(self):

        id_seccion = (
            self.obtener_id_seccion_actual()
        )


        if id_seccion is None:

            messagebox.showwarning(
                "Horarios",
                "Selecciona una sección."
            )

            return None


        dia = (
            self.cmb_dia
            .get()
            .strip()
        )


        if dia == "":

            messagebox.showwarning(
                "Horarios",
                "Selecciona un día."
            )

            return None


        hora_inicio_texto = (
            self.txt_hora_inicio
            .get()
            .strip()
        )


        hora_fin_texto = (
            self.txt_hora_fin
            .get()
            .strip()
        )


        hora_inicio = (
            self.validar_hora(
                hora_inicio_texto
            )
        )


        if hora_inicio is None:

            messagebox.showwarning(
                "Horarios",
                (
                    "La hora de inicio debe usar "
                    "el formato HH:MM."
                )
            )

            return None


        hora_fin = (
            self.validar_hora(
                hora_fin_texto
            )
        )


        if hora_fin is None:

            messagebox.showwarning(
                "Horarios",
                (
                    "La hora final debe usar "
                    "el formato HH:MM."
                )
            )

            return None


        return {
            "id_seccion": id_seccion,
            "dia": dia,
            "hora_inicio": hora_inicio,
            "hora_fin": hora_fin
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
                    "CrearHorario",
                    (
                        datos["id_seccion"],
                        datos["dia"],
                        datos["hora_inicio"],
                        datos["hora_fin"]
                    )
                )
            )


            if resultado is None:

                messagebox.showerror(
                    "Horarios",
                    (
                        "No se pudo crear "
                        "el horario.\n\n"
                        + str(
                            self.database
                            .obtener_ultimo_error()
                        )
                    )
                )

                return


            messagebox.showinfo(
                "Horarios",
                "Horario creado correctamente."
            )


        else:

            resultado = (
                self.database
                .llamar_procedimiento(
                    "ModificarHorario",
                    (
                        self.id_seleccionado,
                        datos["dia"],
                        datos["hora_inicio"],
                        datos["hora_fin"]
                    )
                )
            )


            if resultado is None:

                messagebox.showerror(
                    "Horarios",
                    (
                        "No se pudo modificar "
                        "el horario.\n\n"
                        + str(
                            self.database
                            .obtener_ultimo_error()
                        )
                    )
                )

                return


            messagebox.showinfo(
                "Horarios",
                (
                    "Horario modificado "
                    "correctamente."
                )
            )


        self.cargar_horarios()

        self.nuevo()


    def inactivar(self):

        horario = (
            self.obtener_seleccion()
        )


        if horario is None:

            return


        if horario["estado"] == "INACTIVO":

            messagebox.showinfo(
                "Horarios",
                (
                    "El horario ya se encuentra "
                    "inactivo."
                )
            )

            return


        confirmar = (
            messagebox.askyesno(
                "Inactivar horario",
                (
                    "¿Deseas inactivar "
                    "este horario?\n\n"
                    f"{horario['dia']}  "
                    f"{horario['hora_inicio']} - "
                    f"{horario['hora_fin']}"
                )
            )
        )


        if not confirmar:

            return


        resultado = (
            self.database
            .llamar_procedimiento(
                "InactivarHorario",
                (
                    horario["id"],
                )
            )
        )


        if resultado is None:

            messagebox.showerror(
                "Horarios",
                (
                    "No se pudo inactivar "
                    "el horario.\n\n"
                    + str(
                        self.database
                        .obtener_ultimo_error()
                    )
                )
            )

            return


        messagebox.showinfo(
            "Horarios",
            (
                "Horario inactivado "
                "correctamente."
            )
        )


        self.cargar_horarios()

        self.nuevo()


    def actualizar(self):

        self.cargar_secciones()
        self.nuevo()