import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import threading

from sensor_huellas import SensorHuellas


class Asistencia(tk.Frame):

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

        self.sensor = SensorHuellas()

        self.mapa_sesiones = {}

        self.lector_activo = False

        self.id_sesion_lector = None

        self.hilo_lector = None


        self.pack(
            fill="both",
            expand=True
        )


        self.crear_interfaz()

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
            text="Asistencia",
            bg="#F3F3F3",
            fg="#202020",
            font=(
                "Segoe UI",
                24,
                "bold"
            )
        ).pack(
            side="left"
        )


        panel_sesion = tk.Frame(
            self,
            bg="#FFFFFF",
            highlightthickness=1,
            highlightbackground="#DDDDDD"
        )

        panel_sesion.pack(
            fill="x",
            padx=30,
            pady=(0, 15)
        )


        tk.Label(
            panel_sesion,
            text="Sesión",
            bg="#FFFFFF",
            fg="#202020",
            font=(
                "Segoe UI",
                10,
                "bold"
            )
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=(15, 5)
        )


        self.cmb_sesion = ttk.Combobox(
            panel_sesion,
            state="readonly",
            width=75
        )

        self.cmb_sesion.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=(20, 10),
            pady=(0, 15)
        )


        self.cmb_sesion.bind(
            "<<ComboboxSelected>>",
            self.cambiar_sesion
        )


        tk.Button(
            panel_sesion,
            text="Actualizar",
            bg="#E5E5E5",
            fg="#202020",
            activebackground="#D5D5D5",
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 9),
            command=self.cargar_sesiones
        ).grid(
            row=1,
            column=1,
            padx=(0, 20),
            pady=(0, 15),
            ipadx=15,
            ipady=5
        )


        panel_sesion.grid_columnconfigure(
            0,
            weight=1
        )


        panel_sensor = tk.Frame(
            self,
            bg="#FFFFFF",
            highlightthickness=1,
            highlightbackground="#DDDDDD"
        )

        panel_sensor.pack(
            fill="x",
            padx=30,
            pady=(0, 15)
        )


        tk.Label(
            panel_sensor,
            text="Lector de huella",
            bg="#FFFFFF",
            fg="#202020",
            font=(
                "Segoe UI",
                14,
                "bold"
            )
        ).grid(
            row=0,
            column=0,
            columnspan=3,
            sticky="w",
            padx=20,
            pady=(15, 5)
        )


        self.lbl_estado_sensor = tk.Label(
            panel_sensor,
            text=(
                "Selecciona una sesión "
                "y presiona Iniciar lector."
            ),
            bg="#FFFFFF",
            fg="#555555",
            font=("Segoe UI", 10),
            anchor="w"
        )

        self.lbl_estado_sensor.grid(
            row=1,
            column=0,
            columnspan=3,
            sticky="ew",
            padx=20,
            pady=(5, 10)
        )


        self.lbl_ultimo_alumno = tk.Label(
            panel_sensor,
            text="",
            bg="#FFFFFF",
            fg="#0078D4",
            font=(
                "Segoe UI",
                11,
                "bold"
            ),
            anchor="w"
        )

        self.lbl_ultimo_alumno.grid(
            row=2,
            column=0,
            columnspan=3,
            sticky="ew",
            padx=20,
            pady=(0, 15)
        )


        self.btn_iniciar = tk.Button(
            panel_sensor,
            text="Iniciar lector",
            bg="#0078D4",
            fg="#FFFFFF",
            activebackground="#106EBE",
            activeforeground="#FFFFFF",
            relief="flat",
            bd=0,
            cursor="hand2",
            font=(
                "Segoe UI",
                10,
                "bold"
            ),
            command=self.iniciar_lector
        )

        self.btn_iniciar.grid(
            row=3,
            column=0,
            padx=(20, 5),
            pady=(0, 18),
            ipadx=20,
            ipady=6,
            sticky="w"
        )


        self.btn_detener = tk.Button(
            panel_sensor,
            text="Detener lector",
            bg="#E5E5E5",
            fg="#202020",
            activebackground="#D5D5D5",
            relief="flat",
            bd=0,
            cursor="hand2",
            font=(
                "Segoe UI",
                10
            ),
            command=self.detener_lector,
            state="disabled"
        )

        self.btn_detener.grid(
            row=3,
            column=1,
            padx=5,
            pady=(0, 18),
            ipadx=20,
            ipady=6,
            sticky="w"
        )


        panel_sensor.grid_columnconfigure(
            2,
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
            text="Asistencias registradas: 0",
            bg="#F3F3F3",
            fg="#666666",
            font=("Segoe UI", 9)
        )

        self.lbl_resultados.pack(
            side="left"
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
            pady=(0, 10)
        )


        columnas = (
            "id",
            "codigo",
            "alumno",
            "hora",
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
            "alumno",
            text="Alumno"
        )

        self.tabla.heading(
            "hora",
            text="Hora registro"
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
            width=120
        )

        self.tabla.column(
            "alumno",
            width=280
        )

        self.tabla.column(
            "hora",
            width=160,
            anchor="center"
        )

        self.tabla.column(
            "estado",
            width=130,
            anchor="center"
        )


        scroll_vertical = ttk.Scrollbar(
            panel_tabla,
            orient="vertical",
            command=self.tabla.yview
        )


        self.tabla.configure(
            yscrollcommand=
            scroll_vertical.set
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
            text="Cambiar estado manual",
            bg="#E5E5E5",
            fg="#202020",
            activebackground="#D5D5D5",
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 9),
            command=self.cambiar_estado_manual
        ).pack(
            side="left",
            ipadx=12,
            ipady=5
        )


    def cargar_sesiones(self):

        if self.lector_activo:

            self.detener_lector()


        resultados = (
            self.database
            .llamar_procedimiento(
                "ListarSesionesDocente"
            )
        )


        if resultados is None:

            messagebox.showerror(
                "Asistencia",
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


        sesiones = []

        if resultados:

            sesiones = resultados[0]


        valores = []

        self.mapa_sesiones = {}


        for sesion in sesiones:

            hora_inicio = (
                self.formatear_hora(
                    sesion.get(
                        "hora_inicio"
                    )
                )
            )


            texto = (
                f"{sesion['id']} - "
                f"{sesion['curso']} - "
                f"Sección "
                f"{sesion['seccion']} - "
                f"{sesion['fecha']} - "
                f"{hora_inicio} - "
                f"{sesion['estado']}"
            )


            valores.append(
                texto
            )

            self.mapa_sesiones[
                texto
            ] = sesion


        self.cmb_sesion[
            "values"
        ] = valores


        if valores:

            self.cmb_sesion.current(
                0
            )

            self.cargar_asistencias()

        else:

            self.cmb_sesion.set(
                ""
            )

            self.limpiar_tabla()


    def formatear_hora(
        self,
        valor
    ):

        if valor is None:

            return ""


        if isinstance(
            valor,
            timedelta
        ):

            segundos = int(
                valor.total_seconds()
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


        try:

            return valor.strftime(
                "%H:%M"
            )

        except AttributeError:

            return str(
                valor
            )


    def obtener_sesion_seleccionada(
        self
    ):

        texto = (
            self.cmb_sesion
            .get()
            .strip()
        )


        if (
            texto == ""
            or texto
            not in self.mapa_sesiones
        ):

            return None


        return self.mapa_sesiones[
            texto
        ]


    def cambiar_sesion(
        self,
        event=None
    ):

        if self.lector_activo:

            self.detener_lector()


        self.cargar_asistencias()


        self.lbl_estado_sensor.config(
            text=(
                "Presiona Iniciar lector "
                "para comenzar a marcar."
            )
        )


        self.lbl_ultimo_alumno.config(
            text=""
        )


    def cargar_asistencias(self):

        sesion = (
            self.obtener_sesion_seleccionada()
        )


        if sesion is None:

            self.limpiar_tabla()

            return


        resultados = (
            self.database.consultar(
                """
                SELECT
                    id_asistencia,
                    codigo,
                    alumno,
                    hora_registro,
                    estado
                FROM vista_asistencia_alumnos
                WHERE id_sesion = %s
                ORDER BY alumno
                """,
                (
                    sesion["id"],
                )
            )
        )


        if (
            not resultados
            and
            self.database
            .obtener_ultimo_error()
        ):

            messagebox.showerror(
                "Asistencia",
                (
                    "No se pudieron cargar "
                    "las asistencias.\n\n"
                    + str(
                        self.database
                        .obtener_ultimo_error()
                    )
                )
            )

            return


        self.mostrar_asistencias(
            resultados
        )


    def mostrar_asistencias(
        self,
        datos
    ):

        self.limpiar_tabla()


        for registro in datos:

            hora = registro.get(
                "hora_registro"
            )


            if hora is None:

                hora_texto = ""

            else:

                try:

                    hora_texto = (
                        hora.strftime(
                            "%Y-%m-%d "
                            "%H:%M:%S"
                        )
                    )

                except AttributeError:

                    hora_texto = str(
                        hora
                    )


            self.tabla.insert(
                "",
                tk.END,
                values=(
                    registro[
                        "id_asistencia"
                    ],
                    registro[
                        "codigo"
                    ],
                    registro[
                        "alumno"
                    ],
                    hora_texto,
                    registro[
                        "estado"
                    ]
                )
            )


        self.lbl_resultados.config(
            text=(
                "Asistencias registradas: "
                f"{len(datos)}"
            )
        )


    def limpiar_tabla(self):

        for fila in (
            self.tabla
            .get_children()
        ):

            self.tabla.delete(
                fila
            )


        self.lbl_resultados.config(
            text="Asistencias registradas: 0"
        )


    def iniciar_lector(self):

        if self.lector_activo:

            return


        sesion = (
            self.obtener_sesion_seleccionada()
        )


        if sesion is None:

            messagebox.showwarning(
                "Asistencia",
                "Selecciona una sesión."
            )

            return


        if (
            sesion["estado"]
            != "ABIERTA"
        ):

            messagebox.showwarning(
                "Asistencia",
                (
                    "Solamente se puede marcar "
                    "asistencia en una sesión "
                    "ABIERTA."
                )
            )

            return


        self.id_sesion_lector = (
            sesion["id"]
        )


        self.lector_activo = True


        self.cmb_sesion.config(
            state="disabled"
        )


        self.btn_iniciar.config(
            state="disabled"
        )


        self.btn_detener.config(
            state="normal"
        )


        self.lbl_ultimo_alumno.config(
            text=""
        )


        self.lbl_estado_sensor.config(
            text=(
                "Conectando con Arduino "
                "y sensor..."
            )
        )


        self.hilo_lector = (
            threading.Thread(
                target=self.bucle_lector,
                daemon=True
            )
        )


        self.hilo_lector.start()


    def bucle_lector(self):

        while self.lector_activo:

            try:

                resultado = (
                    self.sensor
                    .identificar_huella(
                        callback_estado=
                        self.estado_sensor_hilo
                    )
                )


                if not self.lector_activo:

                    break


                evento = (
                    threading.Event()
                )


                self.after(
                    0,
                    self.procesar_huella,
                    resultado,
                    evento
                )


                evento.wait()


            except Exception as error:

                if not self.lector_activo:

                    break


                mensaje = str(
                    error
                )


                if (
                    "Tiempo agotado"
                    in mensaje
                    or
                    "Tiempo agotado esperando"
                    in mensaje
                ):

                    continue


                if (
                    "Huella no registrada"
                    in mensaje
                ):

                    self.after(
                        0,
                        self.mostrar_estado_error,
                        "Huella no registrada."
                    )

                    continue


                self.after(
                    0,
                    self.error_lector,
                    mensaje
                )

                break


    def estado_sensor_hilo(
        self,
        mensaje
    ):

        try:

            self.after(
                0,
                self.lbl_estado_sensor.config,
                {
                    "text": mensaje
                }
            )

        except tk.TclError:

            pass


    def procesar_huella(
        self,
        resultado_sensor,
        evento
    ):

        try:

            if not self.lector_activo:

                return


            id_template = (
                resultado_sensor[
                    "id_template"
                ]
            )


            confianza = (
                resultado_sensor.get(
                    "confianza",
                    0
                )
            )


            resultado_alumno = (
                self.database
                .llamar_procedimiento(
                    "BuscarAlumnoPorHuella",
                    (
                        id_template,
                    )
                )
            )


            if resultado_alumno is None:

                self.mostrar_estado_error(
                    (
                        "Error buscando al alumno: "
                        + str(
                            self.database
                            .obtener_ultimo_error()
                        )
                    )
                )

                return


            alumno = None


            for conjunto in (
                resultado_alumno
            ):

                if conjunto:

                    alumno = conjunto[0]

                    break


            if alumno is None:

                self.mostrar_estado_error(
                    (
                        "El template "
                        f"{id_template} "
                        "no está relacionado "
                        "con un alumno activo."
                    )
                )

                return


            resultado_registro = (
                self.database
                .llamar_procedimiento(
                    "RegistrarAsistencia",
                    (
                        alumno["id"],
                        self.id_sesion_lector,
                        datetime.now()
                    )
                )
            )


            if resultado_registro is None:

                self.mostrar_estado_error(
                    (
                        f"{alumno['nombre']} "
                        f"{alumno['apellido']}: "
                        + str(
                            self.database
                            .obtener_ultimo_error()
                        )
                    )
                )

                return


            nombre_completo = (
                f"{alumno['nombre']} "
                f"{alumno['apellido']}"
            )


            self.lbl_estado_sensor.config(
                text=(
                    "Asistencia registrada. "
                    "Coloque la siguiente huella."
                ),
                fg="#107C10"
            )


            self.lbl_ultimo_alumno.config(
                text=(
                    f"{nombre_completo} - "
                    f"{alumno['codigo']} - "
                    f"Template {id_template} - "
                    f"Confianza {confianza}"
                ),
                fg="#107C10"
            )


            self.cargar_asistencias()


        finally:

            evento.set()


    def mostrar_estado_error(
        self,
        mensaje
    ):

        self.lbl_estado_sensor.config(
            text=mensaje,
            fg="#C42B1C"
        )


    def error_lector(
        self,
        mensaje
    ):

        self.lector_activo = False


        self.cmb_sesion.config(
            state="readonly"
        )


        self.btn_iniciar.config(
            state="normal"
        )


        self.btn_detener.config(
            state="disabled"
        )


        self.lbl_estado_sensor.config(
            text=(
                "Se detuvo el lector."
            ),
            fg="#C42B1C"
        )


        messagebox.showerror(
            "Sensor de huella",
            mensaje
        )


    def detener_lector(self):

        if not self.lector_activo:

            return


        self.lector_activo = False


        try:

            self.sensor.cerrar()

        except Exception:

            pass


        self.cmb_sesion.config(
            state="readonly"
        )


        self.btn_iniciar.config(
            state="normal"
        )


        self.btn_detener.config(
            state="disabled"
        )


        self.lbl_estado_sensor.config(
            text="Lector detenido.",
            fg="#555555"
        )


    def cambiar_estado_manual(self):

        seleccion = (
            self.tabla.selection()
        )


        if not seleccion:

            messagebox.showwarning(
                "Asistencia",
                (
                    "Selecciona una asistencia "
                    "de la tabla."
                )
            )

            return


        valores = (
            self.tabla.item(
                seleccion[0],
                "values"
            )
        )


        id_asistencia = int(
            valores[0]
        )


        alumno = valores[2]

        estado_actual = valores[4]


        ventana = tk.Toplevel(
            self
        )

        ventana.title(
            "Cambiar estado"
        )

        ventana.geometry(
            "420x300"
        )

        ventana.resizable(
            False,
            False
        )

        ventana.transient(
            self.winfo_toplevel()
        )

        ventana.grab_set()


        contenedor = tk.Frame(
            ventana,
            bg="#FFFFFF"
        )

        contenedor.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )


        tk.Label(
            contenedor,
            text="Cambiar estado manual",
            bg="#FFFFFF",
            fg="#202020",
            font=(
                "Segoe UI",
                15,
                "bold"
            )
        ).pack(
            anchor="w"
        )


        tk.Label(
            contenedor,
            text=alumno,
            bg="#FFFFFF",
            fg="#555555",
            font=(
                "Segoe UI",
                10
            )
        ).pack(
            anchor="w",
            pady=(5, 15)
        )


        tk.Label(
            contenedor,
            text="Nuevo estado",
            bg="#FFFFFF",
            fg="#202020",
            font=("Segoe UI", 9)
        ).pack(
            anchor="w"
        )


        cmb_estado = ttk.Combobox(
            contenedor,
            state="readonly",
            values=(
                "PRESENTE",
                "TARDE",
                "AUSENTE",
                "FUERA_TIEMPO"
            )
        )

        cmb_estado.pack(
            fill="x",
            pady=(5, 12)
        )


        if estado_actual in (
            "PRESENTE",
            "TARDE",
            "AUSENTE",
            "FUERA_TIEMPO"
        ):

            cmb_estado.set(
                estado_actual
            )


        tk.Label(
            contenedor,
            text="Motivo",
            bg="#FFFFFF",
            fg="#202020",
            font=("Segoe UI", 9)
        ).pack(
            anchor="w"
        )


        txt_motivo = ttk.Entry(
            contenedor
        )

        txt_motivo.pack(
            fill="x",
            pady=(5, 15)
        )


        def guardar():

            nuevo_estado = (
                cmb_estado
                .get()
                .strip()
            )

            motivo = (
                txt_motivo
                .get()
                .strip()
            )


            if nuevo_estado == "":

                messagebox.showwarning(
                    "Asistencia",
                    "Selecciona un estado.",
                    parent=ventana
                )

                return


            if motivo == "":

                messagebox.showwarning(
                    "Asistencia",
                    "Escribe el motivo.",
                    parent=ventana
                )

                return


            resultado = (
                self.database
                .llamar_procedimiento(
                    "CambiarAsistenciaManual",
                    (
                        id_asistencia,
                        nuevo_estado,
                        motivo
                    )
                )
            )


            if resultado is None:

                messagebox.showerror(
                    "Asistencia",
                    (
                        "No se pudo cambiar "
                        "la asistencia.\n\n"
                        + str(
                            self.database
                            .obtener_ultimo_error()
                        )
                    ),
                    parent=ventana
                )

                return


            ventana.destroy()

            self.cargar_asistencias()


            messagebox.showinfo(
                "Asistencia",
                (
                    "Estado actualizado "
                    "correctamente."
                )
            )


        tk.Button(
            contenedor,
            text="Guardar cambio",
            bg="#0078D4",
            fg="#FFFFFF",
            activebackground="#106EBE",
            activeforeground="#FFFFFF",
            relief="flat",
            bd=0,
            cursor="hand2",
            font=(
                "Segoe UI",
                10,
                "bold"
            ),
            command=guardar
        ).pack(
            fill="x",
            ipady=6
        )


    def destroy(self):

        self.lector_activo = False


        try:

            self.sensor.cerrar()

        except Exception:

            pass


        super().destroy()