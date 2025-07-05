# Autores: Sony, Angelo ,Victor, Franklin
# Descripción: Servicio CRUD para pacientes.

from models.paciente import Paciente
import services.datos_globales as db

def obtener_pacientes():
    """Devuelve la lista de pacientes."""
    return db.pacientes

def agregar_paciente(nombre, apellido, dni):
    """Agrega un nuevo paciente a la lista."""
    nuevo = Paciente(db.contador_pacientes, nombre, apellido, dni)
    db.pacientes.append(nuevo)
    db.contador_pacientes += 1

def editar_paciente(id, nuevo_nombre, nuevo_apellido, nuevo_dni):
    """Modifica un paciente existente por su ID."""
    for paciente in db.pacientes:
        if paciente.id == id:
            paciente.nombre = nuevo_nombre
            paciente.apellido = nuevo_apellido
            paciente.dni = nuevo_dni
            break

def eliminar_paciente(id):
    """Elimina un paciente por su ID."""
    db.pacientes = [p for p in db.pacientes if p.id != id]
