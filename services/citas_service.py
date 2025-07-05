# Autores: Sony, Angelo ,Victor, Franklin
# Descripción: Servicio CRUD para la gestión de citas médicas

from models.cita import Cita

# Lista que simula la base de datos de citas
citas = []
contador_id = 1

def obtener_citas():
    """Retorna la lista de citas registradas"""
    return citas

def agregar_cita(paciente, doctor, fecha, hora):
    """Agrega una nueva cita médica"""
    global contador_id
    cita = Cita(contador_id, paciente, doctor, fecha, hora)
    citas.append(cita)
    contador_id += 1

def editar_cita(id_cita, nuevo_paciente, nuevo_doctor, nueva_fecha, nueva_hora):
    """Edita una cita médica existente"""
    for cita in citas:
        if cita.id == id_cita:
            cita.paciente = nuevo_paciente
            cita.doctor = nuevo_doctor
            cita.fecha = nueva_fecha
            cita.hora = nueva_hora
            break

def eliminar_cita(id_cita):
    """Elimina una cita por ID"""
    global citas
    citas = [c for c in citas if c.id != id_cita]
