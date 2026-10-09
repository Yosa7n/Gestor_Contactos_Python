
"""Punto de entrada del Gestor de Contactos.

Laboratorio N.º 05-A - Construcción de Software.
"""

from interfaz.ventana_principal import VentanaPrincipal


def main():
    """Inicia la aplicación con interfaz gráfica."""
    aplicacion = VentanaPrincipal()
    aplicacion.mainloop()


if __name__ == "__main__":
    main()
