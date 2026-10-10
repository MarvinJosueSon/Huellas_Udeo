import tkinter as tk
from tkinter import ttk, messagebox


class ConfiguracionAsistencia(tk.Frame):

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

        self.pack(
            fill="both",
            expand=True
        )

        self.crear_interfaz()
        self.cargar_configuracion()


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
            text="Configuración de asistencia",
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
            command=self.cargar_configuracion
        ).pack(
            side="right",
            ipadx=12,
            ipady=4
        )


        contenedor = tk.Frame(
            self,
            bg="#F3F3F3"
        )

        contenedor.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 30)
        )


        panel = tk.Frame(
            contenedor,
            bg="#FFFFFF",
            width=520,
            highlightthickness=1,
            highlightbackground="#DDDDDD"
        )

        panel.pack(
            anchor="n",
            fill="x"
        )


        tk.Label(
            panel,
            text="Configuración activa",
            bg="#FFFFFF",
            fg="#202020",
            font=("Segoe UI", 16, "bold")
        ).pack(
            anchor="w",
            padx=25,
            pady=(25, 8)
        )


        tk.Label(
            panel,
            text=(
                "Estos valores determinan cómo se "
                "clasifica automáticamente la asistencia."
            ),
            bg="#FFFFFF",
            fg="#666666",
            font=("Segoe UI", 10),
            justify="left"
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 20)
        )


        formulario = tk.Frame(
            panel,
            bg="#FFFFFF"
        )

        formulario.pack(
            fill="x",
            padx=25,
            pady=(0, 20)
        )


        self.crear_etiqueta(
            formulario,
            "Minutos para marcar PRESENTE"
        )

        self.txt_presente = ttk.Entry(
            formulario
        )

        self.txt_presente.pack(
            fill="x",
            pady=(0, 15)
        )


        self.crear_etiqueta(
            formulario,
            "Minutos límite para marcar TARDE"
        )

        self.txt_tarde = ttk.Entry(
            formulario
        )

        self.txt_tarde.pack(
            fill="x",
            pady=(0, 15)
        )


        self.crear_etiqueta(
            formulario,
            "Permitir marcar antes del inicio"
        )

        self.cmb_permite_antes = ttk.Combobox(
            formulario,
            state="readonly",
            values=(
                "SÍ",
                "NO"
            )
        )

        self.cmb_permite_antes.pack(
            fill="x",
            pady=(0, 15)
        )


        self.crear_etiqueta(
            formulario,
            "Límite de baja asistencia (%)"
        )

        self.txt_limite_baja = ttk.Entry(
            formulario
        )

        self.txt_limite_baja.pack(
            fill="x",
            pady=(0, 15)
        )


        self.lbl_fecha = tk.Label(
            formulario,
            text="",
            bg="#FFFFFF",
            fg="#666666",
            font=("Segoe UI", 9)
        )

        self.lbl_fecha.pack(
            anchor="w",
            pady=(5, 0)
        )


        tk.Button(
            panel,
            text="Guardar configuración",
            bg="#0078D4",
            fg="#FFFFFF",
            activebackground="#106EBE",
            activeforeground="#FFFFFF",
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            command=self.guardar
        ).pack(
            fill="x",
            padx=25,
            pady=(0, 25),
            ipady=7
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
            pady=(0, 5)
        )


    def cargar_configuracion(self):

        configuracion = (
            self.database
            .consultar_uno(
                """
                SELECT
                    id,
                    minutos_presente,
                    minutos_tarde,
                    permite_antes,
                    limite_baja,
                    estado,
                    fecha_modificacion
                FROM configuracion_asistencia
                WHERE estado = 'ACTIVA'
                LIMIT 1
                """
            )
        )


        if configuracion is None:

            messagebox.showerror(
                "Configuración",
                (
                    "No se encontró una "
                    "configuración activa.\n\n"
                    + str(
                        self.database
                        .obtener_ultimo_error()
                        or ""
                    )
                )
            )

            return


        self.txt_presente.delete(
            0,
            tk.END
        )

        self.txt_presente.insert(
            0,
            configuracion[
                "minutos_presente"
            ]
        )


        self.txt_tarde.delete(
            0,
            tk.END
        )

        self.txt_tarde.insert(
            0,
            configuracion[
                "minutos_tarde"
            ]
        )


        if configuracion[
            "permite_antes"
        ] == 1:

            self.cmb_permite_antes.set(
                "SÍ"
            )

        else:

            self.cmb_permite_antes.set(
                "NO"
            )


        self.txt_limite_baja.delete(
            0,
            tk.END
        )

        self.txt_limite_baja.insert(
            0,
            configuracion[
                "limite_baja"
            ]
        )


        fecha = configuracion[
            "fecha_modificacion"
        ]


        if fecha is None:

            self.lbl_fecha.config(
                text=""
            )

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


            self.lbl_fecha.config(
                text=(
                    "Última modificación: "
                    + fecha_texto
                )
            )


    def validar_formulario(self):

        presente_texto = (
            self.txt_presente
            .get()
            .strip()
        )

        tarde_texto = (
            self.txt_tarde
            .get()
            .strip()
        )

        limite_texto = (
            self.txt_limite_baja
            .get()
            .strip()
        )

        permite_texto = (
            self.cmb_permite_antes
            .get()
            .strip()
        )


        if presente_texto == "":

            messagebox.showwarning(
                "Configuración",
                (
                    "Ingresa los minutos "
                    "para PRESENTE."
                )
            )

            return None


        try:

            minutos_presente = int(
                presente_texto
            )

        except ValueError:

            messagebox.showwarning(
                "Configuración",
                (
                    "Los minutos de PRESENTE "
                    "deben ser un número entero."
                )
            )

            return None


        if tarde_texto == "":

            messagebox.showwarning(
                "Configuración",
                (
                    "Ingresa los minutos "
                    "para TARDE."
                )
            )

            return None


        try:

            minutos_tarde = int(
                tarde_texto
            )

        except ValueError:

            messagebox.showwarning(
                "Configuración",
                (
                    "Los minutos de TARDE "
                    "deben ser un número entero."
                )
            )

            return None


        if permite_texto not in (
            "SÍ",
            "NO"
        ):

            messagebox.showwarning(
                "Configuración",
                (
                    "Selecciona si se permite "
                    "marcar antes del inicio."
                )
            )

            return None


        if limite_texto == "":

            messagebox.showwarning(
                "Configuración",
                (
                    "Ingresa el límite "
                    "de baja asistencia."
                )
            )

            return None


        try:

            limite_baja = float(
                limite_texto
            )

        except ValueError:

            messagebox.showwarning(
                "Configuración",
                (
                    "El límite de baja asistencia "
                    "debe ser numérico."
                )
            )

            return None


        permite_antes = (
            1
            if permite_texto == "SÍ"
            else 0
        )


        return {
            "minutos_presente":
                minutos_presente,
            "minutos_tarde":
                minutos_tarde,
            "permite_antes":
                permite_antes,
            "limite_baja":
                limite_baja
        }


    def guardar(self):

        datos = (
            self.validar_formulario()
        )


        if datos is None:

            return


        confirmar = (
            messagebox.askyesno(
                "Configuración",
                (
                    "¿Deseas guardar la nueva "
                    "configuración de asistencia?\n\n"
                    f"PRESENTE: hasta "
                    f"{datos['minutos_presente']} min\n"
                    f"TARDE: hasta "
                    f"{datos['minutos_tarde']} min\n"
                    f"Permitir antes: "
                    f"{'Sí' if datos['permite_antes'] == 1 else 'No'}\n"
                    f"Baja asistencia: "
                    f"{datos['limite_baja']}%"
                )
            )
        )


        if not confirmar:

            return


        resultado = (
            self.database
            .llamar_procedimiento(
                "ActualizarConfiguracionAsistencia",
                (
                    datos[
                        "minutos_presente"
                    ],
                    datos[
                        "minutos_tarde"
                    ],
                    datos[
                        "permite_antes"
                    ],
                    datos[
                        "limite_baja"
                    ]
                )
            )
        )


        if resultado is None:

            messagebox.showerror(
                "Configuración",
                (
                    "No se pudo actualizar "
                    "la configuración.\n\n"
                    + str(
                        self.database
                        .obtener_ultimo_error()
                    )
                )
            )

            return


        messagebox.showinfo(
            "Configuración",
            (
                "Configuración actualizada "
                "correctamente."
            )
        )


        self.cargar_configuracion()