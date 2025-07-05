# Autores: Sony, Angelo ,Victor, Franklin
# Descripción: Datos simulados como una base de datos

from models.paciente import Paciente
from models.doctor import Doctor

# Listas que funcionan como base de datos
pacientes = [
    Paciente(1, "Juan", "Pérez", "12345678"),
    Paciente(2, "Ana", "García", "87654321"),
    Paciente(3, "Luis", "Martínez", "11223344"),
]

doctores = [
    Doctor(1, "Dr. Carlos López", "Cardiología"),
    Doctor(2, "Dra. María Ruiz", "Pediatría"),
    Doctor(3, "Dr. Pablo Torres", "Dermatología"),
]

citas = []

# Contadores para IDs únicos
contador_pacientes = 4
contador_doctores = 4
contador_citas = 1
