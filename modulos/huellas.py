import tkinter as tk
from tkinter import ttk, messagebox
import threading

from sensor_huellas import SensorHuellas


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

        self.sensor = (
            SensorHuellas()
        )

        self.datos_huellas = []
        self.mapa_alumnos = {}

        self.capturando = False

        self.pack(
            fill="both",
            expand=True
        )

        self.crear_interfaz()
        self.cargar_alumnos()
        self.cargar_huellas()


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
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            command=self.nueva_huella
        ).pack(
            side="right",
            ipadx=14,
            ipady=7
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
            font=("Segoe UI", 9)
        ).pack(
            side="left"
        )


        self.txt_buscar = ttk.Entry(
            panel_filtros,
            width=30
        )

        self.txt_buscar.pack(
            side="left",
            padx=(8, 25)
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
            font=("Segoe UI", 9)
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
            padx=30
        )


        cuerpo.grid_rowconfigure(
            0,
            weight=1
        )

        cuerpo.grid_columnconfigure(
            0,
            weight=1
        )


        panel_tabla = tk.Frame(
            cuerpo,
            bg="#FFFFFF",
            highlightthickness=1,
            highlightbackground="#A0A0A0"
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
            width=110,
            anchor="center"
        )

        self.tabla.column(
            "alumno",
            width=220
        )

        self.tabla.column(
            "dedo",
            width=120,
            anchor="center"
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


        self.panel_formulario = tk.Frame(
            cuerpo,
            bg="#FFFFFF",
            width=290,
            highlightthickness=1,
            highlightbackground="#A0A0A0"
        )

        self.panel_formulario.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        self.panel_formulario.grid_propagate(
            False
        )


        tk.Label(
            self.panel_formulario,
            text="Registrar huella",
            bg="#FFFFFF",
            fg="#202020",
            font=("Segoe UI", 15, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(28, 25)
        )


        tk.Label(
            self.panel_formulario,
            text="Alumno",
            bg="#FFFFFF",
            fg="#202020",
            font=("Segoe UI", 9)
        ).pack(
            anchor="w",
            padx=20
        )


        self.cmb_alumno = ttk.Combobox(
            self.panel_formulario,
            state="readonly"
        )

        self.cmb_alumno.pack(
            fill="x",
            padx=20,
            pady=(5, 20)
        )


        tk.Label(
            self.panel_formulario,
            text="Dedo registrado",
            bg="#FFFFFF",
            fg="#202020",
            font=("Segoe UI", 9)
        ).pack(
            anchor="w",
            padx=20
        )


        self.cmb_dedo = ttk.Combobox(
            self.panel_formulario,
            state="readonly",
            values=(
                "Pulgar derecho",
                "Índice derecho",
                "Medio derecho",
                "Anular derecho",
                "Meñique derecho",
                "Pulgar izquierdo",
                "Índice izquierdo",
                "Medio izquierdo",
                "Anular izquierdo",
                "Meñique izquierdo"
            )
        )

        self.cmb_dedo.pack(
            fill="x",
            padx=20,
            pady=(5, 20)
        )


        tk.Label(
            self.panel_formulario,
            text="Template asignado por el sensor",
            bg="#FFFFFF",
            fg="#202020",
            font=("Segoe UI", 9)
        ).pack(
            anchor="w",
            padx=20
        )


        self.lbl_template = tk.Label(
            self.panel_formulario,
            text="—",
            bg="#FFFFFF",
            fg="#0078D4",
            font=("Segoe UI", 14, "bold")
        )

        self.lbl_template.pack(
            anchor="w",
            padx=20,
            pady=(5, 15)
        )


        tk.Label(
            self.panel_formulario,
            text=(
                "El template se obtiene "
                "automáticamente del sensor. "
                "No necesitas escribir ningún ID."
            ),
            bg="#FFFFFF",
            fg="#666666",
            wraplength=240,
            justify="left",
            font=("Segoe UI", 9)
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )


        self.lbl_estado_sensor = tk.Label(
            self.panel_formulario,
            text="Sensor listo para conectar",
            bg="#FFFFFF",
            fg="#555555",
            wraplength=240,
            justify="left",
            font=("Segoe UI", 9)
        )

        self.lbl_estado_sensor.pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )


        self.btn_capturar = tk.Button(
            self.panel_formulario,
            text="Capturar y guardar huella",
            bg="#0078D4",
            fg="#FFFFFF",
            activebackground="#106EBE",
            activeforeground="#FFFFFF",
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            command=self.capturar_huella
        )

        self.btn_capturar.pack(
            fill="x",
            padx=20,
            ipady=7
        )


        tk.Button(
            self.panel_formulario,
            text="Cancelar",
            bg="#E5E5E5",
            fg="#202020",
            activebackground="#D5D5D5",
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 9),
            command=self.nueva_huella
        ).pack(
            fill="x",
            padx=20,
            pady=(8, 0),
            ipady=6
        )


        panel_acciones = tk.Frame(
            self,
            bg="#F3F3F3"
        )

        panel_acciones.pack(
            fill="x",
            padx=30,
            pady=(15, 20)
        )


        tk.Button(
            panel_acciones,
            text="Desactivar huella",
            bg="#E5E5E5",
            fg="#202020",
            activebackground="#D5D5D5",
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 9),
            command=self.desactivar_huella
        ).pack(
            side="left",
            ipadx=12,
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
            cursor="hand2",
            font=("Segoe UI", 9),
            command=self.actualizar
        ).pack(
            side="left",
            padx=8,
            ipadx=12,
            ipady=5
        )


    def cargar_alumnos(self):

        resultados = (
            self.database.consultar(
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


        valores = []

        self.mapa_alumnos = {}


        for alumno in resultados:

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


        if valores:

            self.cmb_alumno.current(
                0
            )

        else:

            self.cmb_alumno.set(
                ""
            )


    def cargar_huellas(self):

        resultados = (
            self.database.consultar(
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


        self.datos_huellas = (
            resultados
        )


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

            fecha = (
                huella[
                    "fecha_registro"
                ]
            )


            if fecha is None:

                fecha_texto = ""

            else:

                try:

                    fecha_texto = (
                        fecha.strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                    )

                except AttributeError:

                    fecha_texto = str(
                        fecha
                    )


            self.tabla.insert(
                "",
                tk.END,
                values=(
                    huella["id"],
                    huella["id_template"],
                    huella["codigo"],
                    (
                        f"{huella['nombre']} "
                        f"{huella['apellido']}"
                    ),
                    huella["dedo"],
                    fecha_texto,
                    huella["estado"]
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


        filtradas = []


        for huella in (
            self.datos_huellas
        ):

            contenido = (
                f"{huella['id_template']} "
                f"{huella['codigo']} "
                f"{huella['nombre']} "
                f"{huella['apellido']} "
                f"{huella['dedo']}"
            ).lower()


            coincide_texto = (
                texto == ""
                or texto in contenido
            )


            coincide_estado = (
                estado == "TODAS"
                or huella[
                    "estado"
                ] == estado
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


    def nueva_huella(self):

        self.lbl_template.config(
            text="—"
        )

        self.lbl_estado_sensor.config(
            text="Sensor listo para conectar"
        )


        self.cmb_dedo.set(
            ""
        )


        if (
            self.cmb_alumno[
                "values"
            ]
        ):

            self.cmb_alumno.current(
                0
            )


    def capturar_huella(self):

        if self.capturando:
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
                "Huellas",
                "Selecciona un alumno."
            )

            return


        dedo = (
            self.cmb_dedo
            .get()
            .strip()
        )


        if dedo == "":

            messagebox.showwarning(
                "Huellas",
                (
                    "Selecciona el dedo "
                    "que vas a registrar."
                )
            )

            return


        id_alumno = (
            self.mapa_alumnos[
                alumno_texto
            ]
        )


        self.capturando = True


        self.btn_capturar.config(
            state="disabled",
            text="Capturando..."
        )


        self.lbl_template.config(
            text="—"
        )


        self.lbl_estado_sensor.config(
            text=(
                "Conectando con Arduino "
                "y sensor..."
            )
        )


        hilo = threading.Thread(
            target=self.proceso_captura,
            args=(
                id_alumno,
                alumno_texto,
                dedo
            ),
            daemon=True
        )

        hilo.start()


    def proceso_captura(
        self,
        id_alumno,
        alumno_texto,
        dedo
    ):

        try:

            id_template = (
                self.sensor
                .enrolar_automatico(
                    callback_estado=
                    self.estado_desde_hilo
                )
            )


            self.after(
                0,
                self.guardar_huella_bd,
                id_alumno,
                alumno_texto,
                dedo,
                id_template
            )


        except Exception as error:

            self.after(
                0,
                self.error_sensor,
                str(error)
            )


    def estado_desde_hilo(
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


    def guardar_huella_bd(
        self,
        id_alumno,
        alumno_texto,
        dedo,
        id_template
    ):

        self.lbl_template.config(
            text=str(
                id_template
            )
        )


        self.lbl_estado_sensor.config(
            text=(
                "Huella capturada. "
                "Guardando en la base de datos..."
            )
        )


        resultado = (
            self.database
            .llamar_procedimiento(
                "RegistrarHuella",
                (
                    id_alumno,
                    id_template,
                    dedo
                )
            )
        )


        if resultado is None:

            error_bd = str(
                self.database
                .obtener_ultimo_error()
            )


            self.lbl_estado_sensor.config(
                text=(
                    "Error al guardar. "
                    "Revirtiendo template "
                    "del sensor..."
                )
            )


            hilo = threading.Thread(
                target=self.revertir_template,
                args=(
                    id_template,
                    error_bd
                ),
                daemon=True
            )

            hilo.start()

            return


        self.capturando = False


        self.btn_capturar.config(
            state="normal",
            text="Capturar y guardar huella"
        )


        self.lbl_estado_sensor.config(
            text="Huella registrada correctamente."
        )


        messagebox.showinfo(
            "Huellas",
            (
                "Huella registrada "
                "correctamente.\n\n"
                f"Alumno: {alumno_texto}\n"
                f"Template: {id_template}\n"
                f"Dedo: {dedo}"
            )
        )


        self.cargar_huellas()


    def revertir_template(
        self,
        id_template,
        error_bd
    ):

        eliminado = False
        error_sensor = ""


        try:

            self.sensor.eliminar_template(
                id_template
            )

            eliminado = True


        except Exception as error:

            error_sensor = str(
                error
            )


        self.after(
            0,
            self.finalizar_error_bd,
            error_bd,
            eliminado,
            error_sensor
        )


    def finalizar_error_bd(
        self,
        error_bd,
        eliminado,
        error_sensor
    ):

        self.capturando = False


        self.btn_capturar.config(
            state="normal",
            text="Capturar y guardar huella"
        )


        if eliminado:

            self.lbl_template.config(
                text="—"
            )

            self.lbl_estado_sensor.config(
                text=(
                    "No se guardó la huella. "
                    "El template fue retirado "
                    "del sensor."
                )
            )


            mensaje = (
                "No se pudo guardar la huella "
                "en la base de datos.\n\n"
                f"{error_bd}\n\n"
                "El template creado en el "
                "sensor fue eliminado "
                "automáticamente."
            )


        else:

            self.lbl_estado_sensor.config(
                text=(
                    "Error de sincronización "
                    "entre BD y sensor."
                )
            )


            mensaje = (
                "No se pudo guardar la huella "
                "en la base de datos.\n\n"
                f"{error_bd}\n\n"
                "Además, no se pudo eliminar "
                "el template del sensor:\n"
                f"{error_sensor}"
            )


        messagebox.showerror(
            "Huellas",
            mensaje
        )


    def error_sensor(
        self,
        mensaje
    ):

        self.capturando = False


        self.btn_capturar.config(
            state="normal",
            text="Capturar y guardar huella"
        )


        self.lbl_template.config(
            text="—"
        )


        self.lbl_estado_sensor.config(
            text="No se pudo registrar la huella."
        )


        messagebox.showerror(
            "Sensor de huella",
            mensaje
        )


    def obtener_huella_seleccionada(
        self
    ):

        seleccion = (
            self.tabla.selection()
        )


        if not seleccion:

            messagebox.showwarning(
                "Huellas",
                "Selecciona una huella."
            )

            return None


        valores = (
            self.tabla.item(
                seleccion[0],
                "values"
            )
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
            "estado": valores[6]
        }


    def desactivar_huella(self):

        huella = (
            self.obtener_huella_seleccionada()
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
                    huella[
                        "id_template"
                    ],
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


    def actualizar(self):

        self.cargar_alumnos()
        self.cargar_huellas()


    def destroy(self):

        try:
            self.sensor.cerrar()
        except Exception:
            pass

        super().destroy()