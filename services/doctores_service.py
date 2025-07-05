# Autores: Sony, Angelo ,Victor, Franklin
# Descripción: Servicio CRUD para doctores.

from models.doctor import Doctor
import services.datos_globales as db

def obtener_doctores():
    """Devuelve la lista de doctores."""
    return db.doctores

def agregar_doctor(nombre, especialidad):
    """Agrega un nuevo doctor a la lista."""
    nuevo = Doctor(db.contador_doctores, nombre, especialidad)
    db.doctores.append(nuevo)
    db.contador_doctores += 1

def editar_doctor(id, nuevo_nombre, nueva_especialidad):
    """Modifica un doctor existente por su ID."""
    for doctor in db.doctores:
        if doctor.id == id:
            doctor.nombre = nuevo_nombre
            doctor.especialidad = nueva_especialidad
            break

def eliminar_doctor(id):
    """Elimina un doctor por su ID."""
    db.doctores = [d for d in db.doctores if d.id != id]
