import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os


class Login(tk.Frame):

    def __init__(
        self,
        master,
        database,
        al_iniciar_sesion
    ):
        super().__init__(
            master,
            bg="#F4F2F0"
        )

        self.database = database
        self.al_iniciar_sesion = al_iniciar_sesion

        self.imagen_escudo = None

        self.pack(
            fill="both",
            expand=True
        )

        self.crear_interfaz()


    def crear_interfaz(self):

        contenedor = tk.Frame(
            self,
            bg="#FFFFFF",
            width=380,
            height=480,
            highlightthickness=1,
            highlightbackground="#D8D5D2"
        )

        contenedor.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        contenedor.pack_propagate(False)


        # ESCUDO UDEO

        ruta_escudo = os.path.join(
            os.path.dirname(__file__),
            "assets",
            "escudo_udeo.png"
        )


        if os.path.exists(
            ruta_escudo
        ):

            imagen = Image.open(
                ruta_escudo
            )

            imagen.thumbnail(
                (105, 125),
                Image.Resampling.LANCZOS
            )

            self.imagen_escudo = (
                ImageTk.PhotoImage(
                    imagen
                )
            )


            tk.Label(
                contenedor,
                image=self.imagen_escudo,
                bg="#FFFFFF",
                bd=0
            ).pack(
                pady=(20, 5)
            )


        tk.Label(
            contenedor,
            text="UDEO Assistance Digital",
            bg="#FFFFFF",
            fg="#46384E",
            font=("Segoe UI", 20, "bold")
        ).pack(
            pady=(5, 5)
        )


        tk.Label(
            contenedor,
            text="Control de asistencia",
            bg="#FFFFFF",
            fg="#666666",
            font=("Segoe UI", 10)
        ).pack(
            pady=(0, 22)
        )


        formulario = tk.Frame(
            contenedor,
            bg="#FFFFFF"
        )

        formulario.pack(
            fill="x",
            padx=40
        )


        tk.Label(
            formulario,
            text="Usuario",
            bg="#FFFFFF",
            fg="#202020",
            font=("Segoe UI", 10)
        ).pack(
            anchor="w",
            pady=(0, 5)
        )


        self.txt_usuario = ttk.Entry(
            formulario,
            font=("Segoe UI", 11)
        )

        self.txt_usuario.pack(
            fill="x",
            ipady=5,
            pady=(0, 15)
        )


        tk.Label(
            formulario,
            text="Contraseña",
            bg="#FFFFFF",
            fg="#202020",
            font=("Segoe UI", 10)
        ).pack(
            anchor="w",
            pady=(0, 5)
        )


        self.txt_contrasena = ttk.Entry(
            formulario,
            show="*",
            font=("Segoe UI", 11)
        )

        self.txt_contrasena.pack(
            fill="x",
            ipady=5,
            pady=(0, 22)
        )


        self.btn_ingresar = tk.Button(
            formulario,
            text="Ingresar",
            bg="#DDA62F",
            fg="#202020",
            activebackground="#C99326",
            activeforeground="#202020",
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            command=self.iniciar_sesion
        )

        self.btn_ingresar.pack(
            fill="x",
            ipady=7
        )


        self.txt_usuario.bind(
            "<Return>",
            self.enfocar_contrasena
        )

        self.txt_contrasena.bind(
            "<Return>",
            self.iniciar_sesion
        )


        self.txt_usuario.focus_set()


    def enfocar_contrasena(
        self,
        event=None
    ):
        self.txt_contrasena.focus_set()


    def iniciar_sesion(
        self,
        event=None
    ):

        usuario = (
            self.txt_usuario
            .get()
            .strip()
        )

        contrasena = (
            self.txt_contrasena
            .get()
        )


        if usuario == "":

            messagebox.showwarning(
                "Inicio de sesión",
                "Ingresa tu usuario."
            )

            self.txt_usuario.focus_set()

            return


        if contrasena == "":

            messagebox.showwarning(
                "Inicio de sesión",
                "Ingresa tu contraseña."
            )

            self.txt_contrasena.focus_set()

            return


        self.btn_ingresar.config(
            state="disabled"
        )


        resultado = (
            self.database
            .llamar_procedimiento_uno(
                "IniciarSesion",
                (
                    usuario,
                    contrasena
                )
            )
        )


        self.btn_ingresar.config(
            state="normal"
        )


        if resultado is None:

            error = (
                self.database
                .obtener_ultimo_error()
            )


            if not error:

                error = (
                    "No se pudo iniciar sesión."
                )


            messagebox.showerror(
                "Inicio de sesión",
                error
            )

            self.txt_contrasena.delete(
                0,
                tk.END
            )

            self.txt_contrasena.focus_set()

            return


        datos_usuario = {
            "id": resultado["id"],
            "usuario": resultado["usuario"],
            "rol": resultado["rol"],
            "id_docente": resultado["id_docente"]
        }


        self.al_iniciar_sesion(
            datos_usuario
        )