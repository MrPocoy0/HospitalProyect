# Autores: Sony, Angelo ,Victor, Franklin
# Descripción: Modelo de datos que representa a un paciente del sistema.

class Paciente:
    def __init__(self, id, nombre, apellido, dni):
        """
        Constructor de la clase Paciente.
        :para id: Identificador único del paciente
        :para nombre: Nombre del paciente
        :para apellido: Apellido del paciente
        :para dni: Documento de identidad del paciente
        """
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni