
"""Ventana principal del Gestor de Contactos."""

import tkinter as tk
from tkinter import messagebox

from datos.contactos import GestorContactos
from interfaz.estilos import Estilos as E


class VentanaPrincipal(tk.Tk):

    def __init__(self):
        super().__init__()

        self.gestor = GestorContactos()
        self.title("Agenda | Gestor de Contactos")
        self.geometry("1160x740")
        self.minsize(950, 620)
        self.configure(bg=E.FONDO)

        self.botones_nav = {}

        self.crear_estructura()
        self.mostrar_inicio()

    # ------------------------------------------
    # ESTRUCTURA GENERAL
    # ------------------------------------------

    def crear_estructura(self):
        self.barra = tk.Frame(
            self, bg=E.BARRA, height=76
        )
        self.barra.pack(side="top", fill="x")
        self.barra.pack_propagate(False)

        marca = tk.Frame(self.barra, bg=E.BARRA)
        marca.pack(side="left", padx=34)

        tk.Label(
            marca, text="AGENDA",
            bg=E.BARRA, fg=E.BARRA_TEXTO,
            font=(E.FUENTE, 19, "bold")
        ).pack(anchor="w")

        tk.Label(
            marca, text="Gestión de contactos",
            bg=E.BARRA, fg=E.BARRA_SUAVE,
            font=(E.FUENTE, 9)
        ).pack(anchor="w")

        navegacion = tk.Frame(self.barra, bg=E.BARRA)
        navegacion.pack(side="right", padx=28)

        opciones = [
            ("inicio", "Resumen", self.mostrar_inicio),
            ("directorio", "Directorio", self.mostrar_directorio),
            ("nuevo", "+ Nuevo contacto", self.mostrar_formulario),
        ]

        for clave, texto, comando in opciones:
            boton = tk.Button(
                navegacion,
                text=texto,
                command=comando,
                font=E.NORMAL,
                bg=E.BARRA,
                fg=E.BARRA_SUAVE,
                activebackground=E.PRIMARIO,
                activeforeground="white",
                relief="flat",
                bd=0,
                padx=15,
                pady=12,
                cursor="hand2"
            )
            boton.pack(side="left", padx=3, pady=14)
            self.botones_nav[clave] = boton

        pie = tk.Frame(
            self, bg=E.SUPERFICIE, height=34,
            highlightbackground=E.BORDE,
            highlightthickness=1
        )
        pie.pack(side="bottom", fill="x")

        tk.Label(
            pie, text="Agenda de contactos",
            bg=E.SUPERFICIE,
            fg=E.TEXTO_SECUNDARIO,
            font=(E.FUENTE, 9)
        ).pack(side="left", padx=30, pady=7)

        tk.Label(
            pie, text="Laboratorio 05-A  |  Versión 2.0",
            bg=E.SUPERFICIE,
            fg=E.TEXTO_SECUNDARIO,
            font=(E.FUENTE, 9)
        ).pack(side="right", padx=30)

        self.contenido = tk.Frame(
            self, bg=E.FONDO
        )
        self.contenido.pack(
            fill="both", expand=True
        )

    def activar(self, clave):
        for nombre, boton in self.botones_nav.items():
            activo = nombre == clave
            boton.configure(
                bg=E.PRIMARIO if activo else E.BARRA,
                fg="white" if activo else E.BARRA_SUAVE
            )

    def limpiar(self):
        for widget in self.contenido.winfo_children():
            widget.destroy()

    def boton(self, padre, texto, comando, secundario=False):
        return tk.Button(
            padre,
            text=texto,
            command=comando,
            bg=E.SUPERFICIE if secundario else E.PRIMARIO,
            fg=E.TEXTO if secundario else "white",
            activebackground=(
                E.SUPERFICIE_ALT if secundario
                else E.PRIMARIO_HOVER
            ),
            activeforeground=E.TEXTO if secundario else "white",
            font=E.BOTON,
            relief="solid" if secundario else "flat",
            bd=1 if secundario else 0,
            cursor="hand2",
            padx=19,
            pady=10
        )

    def encabezado(self, titulo, descripcion, accion=None):
        fila = tk.Frame(self.contenido, bg=E.FONDO)
        fila.pack(fill="x", padx=34, pady=(30, 22))

        izquierdo = tk.Frame(fila, bg=E.FONDO)
        izquierdo.pack(side="left", fill="x", expand=True)

        tk.Label(
            izquierdo, text=titulo,
            bg=E.FONDO, fg=E.TEXTO,
            font=E.TITULO
        ).pack(anchor="w")

        tk.Label(
            izquierdo, text=descripcion,
            bg=E.FONDO, fg=E.TEXTO_SECUNDARIO,
            font=E.SUBTITULO
        ).pack(anchor="w", pady=(6, 0))

        if accion:
            self.boton(
                fila, "+ Añadir contacto",
                self.mostrar_formulario
            ).pack(side="right", padx=(12, 0))

    def panel(self, padre):
        return tk.Frame(
            padre,
            bg=E.SUPERFICIE,
            highlightbackground=E.BORDE,
            highlightthickness=1
        )

    # ------------------------------------------
    # TABLA CON LINEAS VISIBLES
    # ------------------------------------------

    def crear_fila_tabla(self, padre, valores, cabecera=False):
        fila = tk.Frame(padre, bg=E.BORDE)

        pesos = (1, 3, 2, 4)

        for indice, peso in enumerate(pesos):
            fila.grid_columnconfigure(indice, weight=peso)

        for indice, valor in enumerate(valores):
            tk.Label(
                fila,
                text=str(valor),
                bg=E.SUPERFICIE_ALT if cabecera
                   else E.SUPERFICIE,
                fg=E.TEXTO if cabecera
                   else E.TEXTO_SECUNDARIO,
                font=E.BOTON if cabecera
                     else E.NORMAL,
                anchor="w",
                padx=12,
                pady=12,
                highlightbackground=E.BORDE,
                highlightthickness=1
            ).grid(
                row=0,
                column=indice,
                sticky="nsew"
            )

        fila.pack(fill="x")
        return fila

    def crear_tabla(self, padre, registros, alto=260):
        encabezados = (
            "ID", "NOMBRE COMPLETO",
            "TELÉFONO", "CORREO"
        )
        self.crear_fila_tabla(
            padre, encabezados, cabecera=True
        )

        zona = tk.Frame(padre, bg=E.SUPERFICIE)
        zona.pack(fill="both", expand=True)

        canvas = tk.Canvas(
            zona,
            bg=E.SUPERFICIE,
            highlightthickness=0,
            height=alto
        )

        scroll = tk.Scrollbar(
            zona, orient="vertical",
            command=canvas.yview
        )
        canvas.configure(
            yscrollcommand=scroll.set
        )

        scroll.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        interior = tk.Frame(
            canvas, bg=E.SUPERFICIE
        )

        ventana = canvas.create_window(
            (0, 0),
            window=interior,
            anchor="nw"
        )

        interior.bind(
            "<Configure>",
            lambda evento: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        canvas.bind(
            "<Configure>",
            lambda evento: canvas.itemconfigure(
                ventana, width=evento.width
            )
        )

        if not registros:
            tk.Label(
                interior,
                text="No hay contactos para mostrar.",
                bg=E.SUPERFICIE,
                fg=E.TEXTO_SECUNDARIO,
                font=E.NORMAL,
                pady=35
            ).pack(fill="x")
        else:
            for contacto in registros:
                self.crear_fila_tabla(
                    interior,
                    (
                        contacto["id"],
                        contacto["nombre"],
                        contacto["telefono"],
                        contacto["correo"] or "—"
                    )
                )

    # ------------------------------------------
    # RESUMEN
    # ------------------------------------------

    def tarjeta_estadistica(self, padre, titulo, valor, detalle):
        tarjeta = self.panel(padre)

        tk.Label(
            tarjeta, text=titulo,
            bg=E.SUPERFICIE,
            fg=E.TEXTO_SECUNDARIO,
            font=E.BOTON
        ).pack(anchor="w", padx=22, pady=(19, 7))

        tk.Label(
            tarjeta, text=str(valor),
            bg=E.SUPERFICIE,
            fg=E.TEXTO,
            font=E.NUMERO
        ).pack(anchor="w", padx=22)

        tk.Label(
            tarjeta, text=detalle,
            bg=E.SUPERFICIE,
            fg=E.TEXTO_SECUNDARIO,
            font=E.NORMAL
        ).pack(anchor="w", padx=22, pady=(5, 20))

        return tarjeta

    def mostrar_inicio(self):
        self.limpiar()
        self.activar("inicio")

        self.encabezado(
            "Resumen de contactos",
            "Información general de tu agenda personal.",
            accion=True
        )

        contactos = self.gestor.listar()
        con_correo = sum(
            1 for c in contactos if c["correo"]
        )

        indicadores = tk.Frame(
            self.contenido, bg=E.FONDO
        )
        indicadores.pack(
            fill="x", padx=34, pady=(0, 22)
        )

        indicadores.grid_columnconfigure(0, weight=1)
        indicadores.grid_columnconfigure(1, weight=1)

        self.tarjeta_estadistica(
            indicadores,
            "CONTACTOS REGISTRADOS",
            len(contactos),
            "Total en tu agenda"
        ).grid(
            row=0, column=0,
            sticky="nsew", padx=(0, 9)
        )

        self.tarjeta_estadistica(
            indicadores,
            "CONTACTOS CON CORREO",
            con_correo,
            "Registros con correo electrónico"
        ).grid(
            row=0, column=1,
            sticky="nsew", padx=(9, 0)
        )

        bloque = tk.Frame(
            self.contenido, bg=E.FONDO
        )
        bloque.pack(
            fill="both", expand=True,
            padx=34, pady=(0, 25)
        )

        bloque.grid_columnconfigure(0, weight=4)
        bloque.grid_columnconfigure(1, weight=1)
        bloque.grid_rowconfigure(0, weight=1)

        recientes = self.panel(bloque)
        recientes.grid(
            row=0, column=0,
            sticky="nsew", padx=(0, 16)
        )

        tk.Label(
            recientes, text="Últimos contactos",
            bg=E.SUPERFICIE,
            fg=E.TEXTO,
            font=(E.FUENTE, 13, "bold")
        ).pack(
            anchor="w", padx=20, pady=18
        )

        self.crear_tabla(
            recientes,
            contactos[-5:][::-1],
            alto=210
        )

        lateral = self.panel(bloque)
        lateral.grid(
            row=0, column=1, sticky="nsew"
        )

        tk.Label(
            lateral, text="Accesos rápidos",
            bg=E.SUPERFICIE,
            fg=E.TEXTO,
            font=(E.FUENTE, 12, "bold")
        ).pack(
            anchor="w", padx=18, pady=(20, 15)
        )

        self.boton(
            lateral, "Ver directorio",
            self.mostrar_directorio,
            secundario=True
        ).pack(fill="x", padx=14, pady=5)

        self.boton(
            lateral, "Nuevo contacto",
            self.mostrar_formulario
        ).pack(fill="x", padx=14, pady=5)

    # ------------------------------------------
    # DIRECTORIO
    # ------------------------------------------

    def mostrar_directorio(self):
        self.limpiar()
        self.activar("directorio")

        self.encabezado(
            "Directorio",
            "Consulta y busca contactos registrados.",
            accion=True
        )

        filtro = self.panel(self.contenido)
        filtro.pack(
            fill="x", padx=34, pady=(0, 16)
        )

        tk.Label(
            filtro, text="Buscar contacto",
            bg=E.SUPERFICIE, fg=E.TEXTO,
            font=E.BOTON
        ).pack(
            side="left", padx=(18, 12), pady=16
        )

        self.busqueda = tk.StringVar()

        entrada = tk.Entry(
            filtro,
            textvariable=self.busqueda,
            font=E.NORMAL,
            bg=E.SUPERFICIE,
            fg=E.TEXTO,
            relief="solid",
            bd=1
        )
        entrada.pack(
            side="left", fill="x",
            expand=True, padx=(0, 18),
            pady=14, ipady=7
        )

        self.resultados = self.panel(self.contenido)
        self.resultados.pack(
            fill="both", expand=True,
            padx=34, pady=(0, 28)
        )

        self.busqueda.trace_add(
            "write",
            lambda *_: self.actualizar_directorio()
        )
        self.actualizar_directorio()

    def actualizar_directorio(self):
        for widget in self.resultados.winfo_children():
            widget.destroy()

        encontrados = self.gestor.buscar(
            self.busqueda.get()
        )

        tk.Label(
            self.resultados,
            text=f"Contactos encontrados: {len(encontrados)}",
            bg=E.SUPERFICIE,
            fg=E.TEXTO_SECUNDARIO,
            font=E.NORMAL
        ).pack(
            anchor="w", padx=18, pady=14
        )

        self.crear_tabla(
            self.resultados, encontrados,
            alto=340
        )

    # ------------------------------------------
    # REGISTRO
    # ------------------------------------------

    def crear_campo(self, padre, texto):
        tk.Label(
            padre, text=texto,
            bg=E.SUPERFICIE,
            fg=E.TEXTO,
            font=E.BOTON
        ).pack(
            anchor="w", pady=(13, 6)
        )

        entrada = tk.Entry(
            padre,
            bg=E.SUPERFICIE,
            fg=E.TEXTO,
            font=E.NORMAL,
            relief="solid",
            bd=1
        )
        entrada.pack(fill="x", ipady=10)
        return entrada

    def mostrar_formulario(self):
        self.limpiar()
        self.activar("nuevo")

        self.encabezado(
            "Registrar contacto",
            "Añade una nueva persona a tu agenda."
        )

        zona = tk.Frame(
            self.contenido, bg=E.FONDO
        )
        zona.pack(
            fill="both", expand=True,
            padx=34, pady=(0, 28)
        )

        zona.grid_columnconfigure(0, weight=3)
        zona.grid_columnconfigure(1, weight=1)

        formulario = self.panel(zona)
        formulario.grid(
            row=0, column=0,
            sticky="nsew", padx=(0, 16)
        )

        interior = tk.Frame(
            formulario, bg=E.SUPERFICIE
        )
        interior.pack(
            fill="both", padx=28, pady=25
        )

        tk.Label(
            interior,
            text="Información del contacto",
            bg=E.SUPERFICIE,
            fg=E.TEXTO,
            font=(E.FUENTE, 14, "bold")
        ).pack(anchor="w", pady=(0, 9))

        nombre = self.crear_campo(
            interior, "Nombre completo *"
        )
        telefono = self.crear_campo(
            interior, "Número de teléfono *"
        )
        correo = self.crear_campo(
            interior, "Correo electrónico"
        )

        acciones = tk.Frame(
            interior, bg=E.SUPERFICIE
        )
        acciones.pack(
            fill="x", pady=(28, 5)
        )

        def guardar():
            correcto, mensaje = self.gestor.agregar(
                nombre.get(),
                telefono.get(),
                correo.get()
            )

            if correcto:
                messagebox.showinfo(
                    "Registro completado", mensaje
                )
                self.mostrar_directorio()
            else:
                messagebox.showwarning(
                    "Revisa los datos", mensaje
                )

        self.boton(
            acciones, "Guardar contacto", guardar
        ).pack(side="left")

        self.boton(
            acciones, "Cancelar",
            self.mostrar_directorio,
            secundario=True
        ).pack(side="left", padx=12)

        ayuda = self.panel(zona)
        ayuda.grid(
            row=0, column=1, sticky="nsew"
        )

        tk.Label(
            ayuda,
            text="Antes de guardar",
            bg=E.SUPERFICIE,
            fg=E.TEXTO,
            font=(E.FUENTE, 12, "bold")
        ).pack(
            anchor="w", padx=20, pady=(24, 12)
        )

        tk.Label(
            ayuda,
            text=(
                "Los campos marcados con * "
                "son obligatorios.\n\n"
                "El teléfono debe contener "
                "solo números y no puede "
                "estar duplicado.\n\n"
                "Los contactos se guardan "
                "temporalmente durante "
                "esta sesión."
            ),
            bg=E.SUPERFICIE,
            fg=E.TEXTO_SECUNDARIO,
            font=E.NORMAL,
            justify="left",
            wraplength=190
        ).pack(
            anchor="w", padx=20, pady=5
        )

        nombre.focus_set()
