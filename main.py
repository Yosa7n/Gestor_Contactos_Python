
# Gestor de Contactos en Python
# Proyecto para el Laboratorio N.º 05-A

contactos = []


def agregar_contacto():
    nombre = input("Nombre: ").strip()
    telefono = input("Telefono: ").strip()

    if not nombre or not telefono:
        print("El nombre y el telefono son obligatorios.")
        return

    contactos.append({"nombre": nombre, "telefono": telefono})
    print("Contacto registrado correctamente.")


def listar_contactos():
    if not contactos:
        print("No hay contactos registrados.")
        return

    print("\n--- LISTA DE CONTACTOS ---")
    for numero, contacto in enumerate(contactos, start=1):
        print(f"{numero}. {contacto['nombre']} - {contacto['telefono']}")


def main():
    while True:
        print("\n===== GESTOR DE CONTACTOS =====")
        print("1. Agregar contacto")
        print("2. Listar contactos")
        print("3. Salir")

        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1":
            agregar_contacto()
        elif opcion == "2":
            listar_contactos()
        elif opcion == "3":
            print("Programa finalizado.")
            break
        else:
            print("Opcion no valida. Intente nuevamente.")


if __name__ == "__main__":
    main()
