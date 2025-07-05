# Autores: Sony, Angelo ,Victor, Franklin
# Descripción: Ventana gráfica para la gestión de doctores

import tkinter as tk
from tkinter import messagebox
from services import doctores_service

class DoctorVentana:
    def __init__(self):
        # Crear una nueva ventana
        self.ventana = tk.Toplevel()
        self.ventana.title("Gestión de Doctores")
        self.ventana.geometry("700x600")
        self.ventana.configure(bg="#f0f8ff")  # Fondo azul claro
        self.ventana.resizable(False, False)

        # Título de la ventana
        titulo = tk.Label(self.ventana, text="Gestión de Doctores", font=("Helvetica", 18, "bold"),
                          bg="#f0f8ff", fg="#003366")
        titulo.pack(pady=15)

        # Frame para la lista de doctores
        frame_lista = tk.LabelFrame(self.ventana, text="Doctores Registrados", font=("Arial", 11, "bold"),
                                    bg="#f0f8ff", fg="#003366")
        frame_lista.pack(padx=20, pady=10, fill="both", expand=True)

        # Listbox para mostrar doctores
        self.lista_doctores = tk.Listbox(frame_lista, font=("Arial", 10), width=70, height=10)
        self.lista_doctores.pack(side="left", fill="y", padx=(10, 0), pady=10)

        # Scrollbar vertical para la lista
        scrollbar = tk.Scrollbar(frame_lista, orient="vertical", command=self.lista_doctores.yview)
        scrollbar.pack(side="right", fill="y", pady=10)
        self.lista_doctores.config(yscrollcommand=scrollbar.set)

        self.lista_doctores.bind("<<ListboxSelect>>", self.seleccionar_doctor)

        # Frame para el formulario de ingreso
        frame_formulario = tk.LabelFrame(self.ventana, text="Datos del Doctor", font=("Arial", 11, "bold"),
                                         bg="#f0f8ff", fg="#003366")
        frame_formulario.pack(padx=20, pady=10, fill="x")

        # Validaciones: solo letras
        self.validar_letras = self.ventana.register(lambda c: c.isalpha() or c.isspace())

        # Campo: Nombre
        self.nombre_entry = self._crear_campo(frame_formulario, "Nombre:", validar=self.validar_letras)

        # Campo: Especialidad
        self.especialidad_entry = self._crear_campo(frame_formulario, "Especialidad:", validar=self.validar_letras)

        # Estilos para los botones
        estilo_btn = {
            "width": 20,
            "height": 1,
            "font": ("Arial", 10, "bold"),
            "bg": "#add8e6",
            "fg": "#003366",
            "bd": 0,
            "activebackground": "#87cefa"
        }

        estilo_btn_rojo = estilo_btn.copy()
        estilo_btn_rojo.update({"bg": "#ffcccc", "fg": "#660000", "activebackground": "#ff9999"})

        # Frame para los botones CRUD
        btn_frame = tk.Frame(self.ventana, bg="#f0f8ff")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Agregar", command=self.agregar_doctor, **estilo_btn).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Editar seleccionado", command=self.editar_doctor, **estilo_btn).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Eliminar seleccionado", command=self.eliminar_doctor, **estilo_btn_rojo).grid(row=0, column=2, padx=5)

        self.actualizar_lista()

    def _crear_campo(self, frame, texto, validar=None):
        """Crea un campo con etiqueta y entrada de texto"""
        label = tk.Label(frame, text=texto, bg="#f0f8ff", font=("Arial", 10, "bold"))
        label.pack(anchor="w", padx=10, pady=(5, 0))
        entry = tk.Entry(frame, width=50, validate="key", validatecommand=(validar, "%S")) if validar else tk.Entry(frame, width=50)
        entry.pack(padx=10, pady=5)
        return entry

    def actualizar_lista(self):
        """Actualiza el contenido de la lista de doctores"""
        self.lista_doctores.delete(0, tk.END)
        for doctor in doctores_service.obtener_doctores():
            self.lista_doctores.insert(tk.END, f"ID {doctor.id}: {doctor.nombre} - {doctor.especialidad}")

    def agregar_doctor(self):
        """Agrega un nuevo doctor si todos los campos están completos"""
        nombre = self.nombre_entry.get().strip()
        especialidad = self.especialidad_entry.get().strip()

        if not nombre or not especialidad:
            messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios.")
            return

        doctores_service.agregar_doctor(nombre, especialidad)
        self.actualizar_lista()
        self._limpiar_campos()

    def editar_doctor(self):
        """Edita los datos del doctor seleccionado"""
        seleccion = self.lista_doctores.curselection()
        if not seleccion:
            messagebox.showinfo("Editar", "Selecciona un doctor para editar.")
            return

        indice = seleccion[0]
        doctor = doctores_service.obtener_doctores()[indice]

        nuevo_nombre = self.nombre_entry.get().strip()
        nueva_especialidad = self.especialidad_entry.get().strip()

        if not nuevo_nombre or not nueva_especialidad:
            messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios.")
            return

        doctores_service.editar_doctor(doctor.id, nuevo_nombre, nueva_especialidad)
        self.actualizar_lista()
        self._limpiar_campos()

    def eliminar_doctor(self):
        """Elimina el doctor seleccionado con confirmación"""
        seleccion = self.lista_doctores.curselection()
        if not seleccion:
            messagebox.showinfo("Eliminar", "Selecciona un doctor para eliminar.")
            return

        indice = seleccion[0]
        doctor = doctores_service.obtener_doctores()[indice]

        confirmar = messagebox.askyesno("Confirmar eliminación", f"¿Eliminar al doctor {doctor.nombre}?")
        if confirmar:
            doctores_service.eliminar_doctor(doctor.id)
            self.actualizar_lista()
            self._limpiar_campos()

    def seleccionar_doctor(self, event):
        """Llena los campos con los datos del doctor seleccionado"""
        seleccion = self.lista_doctores.curselection()
        if seleccion:
            indice = seleccion[0]
            doctor = doctores_service.obtener_doctores()[indice]
            self.nombre_entry.delete(0, tk.END)
            self.nombre_entry.insert(0, doctor.nombre)
            self.especialidad_entry.delete(0, tk.END)
            self.especialidad_entry.insert(0, doctor.especialidad)

    def _limpiar_campos(self):
        """Limpia los campos del formulario"""
        self.nombre_entry.delete(0, tk.END)
        self.especialidad_entry.delete(0, tk.END)