# Autores: Sony, Angelo ,Victor, Franklin
# Descripción: Ventana gráfica para la gestión de pacientes.

import tkinter as tk
from tkinter import messagebox
from services import pacientes_service
import re

class PacienteVentana:
    def __init__(self):
        self.ventana = tk.Toplevel()
        self.ventana.title("Gestión de Pacientes")
        self.ventana.geometry("700x600")
        self.ventana.configure(bg="#f0f8ff")
        self.ventana.resizable(False, False)

        titulo = tk.Label(self.ventana, text="Gestión de Pacientes", font=("Helvetica", 18, "bold"),
                          bg="#f0f8ff", fg="#003366")
        titulo.pack(pady=20)

        frame_lista = tk.LabelFrame(self.ventana, text="Lista de Pacientes", font=("Arial", 11, "bold"),
                                    bg="#f0f8ff", fg="#003366")
        frame_lista.pack(padx=20, pady=10, fill="both", expand=True)

        self.lista_pacientes = tk.Listbox(frame_lista, font=("Arial", 10), width=70, height=10)
        self.lista_pacientes.pack(side="left", fill="y", padx=(10, 0), pady=10)

        scrollbar = tk.Scrollbar(frame_lista, orient="vertical", command=self.lista_pacientes.yview)
        scrollbar.pack(side="right", fill="y", pady=10)
        self.lista_pacientes.config(yscrollcommand=scrollbar.set)

        self.lista_pacientes.bind("<<ListboxSelect>>", self.seleccionar_paciente)

        frame_formulario = tk.LabelFrame(self.ventana, text="Datos del Paciente", font=("Arial", 11, "bold"),
                                         bg="#f0f8ff", fg="#003366")
        frame_formulario.pack(padx=20, pady=10, fill="x")

        # Validaciones para entradas
        self.validar_letras = self.ventana.register(lambda c: c.isalpha() or c.isspace())
        self.validar_numeros = self.ventana.register(str.isdigit)

        self.nombre_entry = self._crear_campo(frame_formulario, "Nombre:", validar=self.validar_letras)
        self.apellido_entry = self._crear_campo(frame_formulario, "Apellido:", validar=self.validar_letras)
        self.dni_entry = self._crear_campo(frame_formulario, "DNI:", validar=self.validar_numeros)

        estilo_btn = {
            "width": 20,
            "height": 1,
            "font": ("Arial", 10, "bold"),
            "bg": "#cce5ff",
            "fg": "#003366",
            "bd": 0,
            "activebackground": "#99ccff"
        }

        estilo_btn_rojo = estilo_btn.copy()
        estilo_btn_rojo.update({"bg": "#ffcccc", "fg": "#660000", "activebackground": "#ff9999"})

        btn_frame = tk.Frame(self.ventana, bg="#f0f8ff")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Agregar", command=self.agregar_paciente, **estilo_btn).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Editar seleccionado", command=self.editar_paciente, **estilo_btn).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Eliminar seleccionado", command=self.eliminar_paciente, **estilo_btn_rojo).grid(row=0, column=2, padx=5)

        self.actualizar_lista()

    def _crear_campo(self, frame, texto, validar=None):
        label = tk.Label(frame, text=texto, bg="#f0f8ff", font=("Arial", 10, "bold"))
        label.pack(anchor="w", padx=10, pady=(5, 0))
        entry = tk.Entry(frame, width=50, validate="key", validatecommand=(validar, "%S")) if validar else tk.Entry(frame, width=50)
        entry.pack(padx=10, pady=5)
        return entry

    def actualizar_lista(self):
        self.lista_pacientes.delete(0, tk.END)
        for paciente in pacientes_service.obtener_pacientes():
            self.lista_pacientes.insert(tk.END, f"ID {paciente.id}: {paciente.nombre} {paciente.apellido} - DNI: {paciente.dni}")

    def agregar_paciente(self):
        nombre = self.nombre_entry.get().strip()
        apellido = self.apellido_entry.get().strip()
        dni = self.dni_entry.get().strip()

        if not nombre or not apellido or not dni:
            messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios.")
            return

        if len(dni) != 8 or not dni.isdigit():
            messagebox.showerror("DNI inválido", "El DNI debe contener exactamente 8 dígitos numéricos.")
            return

        pacientes_service.agregar_paciente(nombre, apellido, dni)
        self.actualizar_lista()
        self._limpiar_campos()

    def editar_paciente(self):
        seleccion = self.lista_pacientes.curselection()
        if not seleccion:
            messagebox.showinfo("Editar", "Selecciona un paciente para editar.")
            return

        indice = seleccion[0]
        paciente = pacientes_service.obtener_pacientes()[indice]

        nuevo_nombre = self.nombre_entry.get().strip()
        nuevo_apellido = self.apellido_entry.get().strip()
        nuevo_dni = self.dni_entry.get().strip()

        if not nuevo_nombre or not nuevo_apellido or not nuevo_dni:
            messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios.")
            return

        if len(nuevo_dni) != 8 or not nuevo_dni.isdigit():
            messagebox.showerror("DNI inválido", "El DNI debe contener exactamente 8 dígitos numéricos.")
            return

        pacientes_service.editar_paciente(paciente.id, nuevo_nombre, nuevo_apellido, nuevo_dni)
        self.actualizar_lista()
        self._limpiar_campos()

    def eliminar_paciente(self):
        seleccion = self.lista_pacientes.curselection()
        if not seleccion:
            messagebox.showinfo("Eliminar", "Selecciona un paciente para eliminar.")
            return

        indice = seleccion[0]
        paciente = pacientes_service.obtener_pacientes()[indice]

        confirmar = messagebox.askyesno("Confirmar eliminación", f"¿Eliminar al paciente {paciente.nombre} {paciente.apellido}?")
        if confirmar:
            pacientes_service.eliminar_paciente(paciente.id)
            self.actualizar_lista()
            self._limpiar_campos()

    def seleccionar_paciente(self, event):
        seleccion = self.lista_pacientes.curselection()
        if seleccion:
            indice = seleccion[0]
            paciente = pacientes_service.obtener_pacientes()[indice]
            self.nombre_entry.delete(0, tk.END)
            self.nombre_entry.insert(0, paciente.nombre)
            self.apellido_entry.delete(0, tk.END)
            self.apellido_entry.insert(0, paciente.apellido)
            self.dni_entry.delete(0, tk.END)
            self.dni_entry.insert(0, paciente.dni)

    def _limpiar_campos(self):
        self.nombre_entry.delete(0, tk.END)
        self.apellido_entry.delete(0, tk.END)
        self.dni_entry.delete(0, tk.END)