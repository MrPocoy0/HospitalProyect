# Autores: Sony, Angelo ,Victor, Franklin
# Descripción: Modelo de datos para representar a un doctor del sistema

class Doctor:
    def __init__(self, id, nombre, especialidad):
        """
        Constructor de la clase Doctor.
        :para id: Identificador único del doctor
        :para nombre: Nombre completo del doctor
        :para especialidad: Especialidad médica del doctor
        """
        self.id = id
        self.nombre = nombre
        self.especialidad = especialidad
