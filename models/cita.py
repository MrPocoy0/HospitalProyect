# Autores: Sony, Angelo ,Victor, Franklin
# Descripción: Modelo de datos para representar una cita médica

class Cita:
    def __init__(self, id, paciente, doctor, fecha, hora):
        self.id = id
        self.paciente = paciente
        self.doctor = doctor
        self.fecha = fecha
        self.hora = hora
