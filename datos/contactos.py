
class GestorContactos:
    """Administra los contactos de la aplicación."""

    def __init__(self):
        self.contactos = []

    def agregar(self, nombre, telefono, correo=""):
        nombre = nombre.strip()
        telefono = telefono.strip()
        correo = correo.strip()

        if not nombre or not telefono:
            return False, "El nombre y el teléfono son obligatorios."

        if not telefono.isdigit():
            return False, "El teléfono solo debe contener números."

        if any(c["telefono"] == telefono for c in self.contactos):
            return False, "Ya existe un contacto con ese teléfono."

        contacto = {
            "id": len(self.contactos) + 1,
            "nombre": nombre,
            "telefono": telefono,
            "correo": correo
        }

        self.contactos.append(contacto)
        return True, "Contacto registrado correctamente."

    def listar(self):
        return self.contactos.copy()

    def buscar(self, texto):
        texto = texto.strip().lower()

        return [
            contacto for contacto in self.contactos
            if texto in contacto["nombre"].lower()
            or texto in contacto["telefono"]
            or texto in contacto["correo"].lower()
        ]

    def eliminar(self, contacto_id):
        for contacto in self.contactos:
            if contacto["id"] == contacto_id:
                self.contactos.remove(contacto)
                return True
        return False

    def total_contactos(self):
        return len(self.contactos)
