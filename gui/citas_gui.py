# Autores: Sony, Angelo, Victor, Franklin
# Descripción: Ventana gráfica para la gestión de citas médicas

import tkinter as tk
from tkinter import messagebox
from services import citas_service
import re

class CitaVentana:
    def __init__(self):
        self.ventana = tk.Toplevel()
        self.ventana.title("Gestión de Citas Médicas")
        self.ventana.geometry("700x620")
        self.ventana.configure(bg="#fffaf0")  # Fondo beige claro
        self.ventana.resizable(False, False)

        # Título
        titulo = tk.Label(self.ventana, text="Gestión de Citas Médicas", font=("Helvetica", 18, "bold"),
                          bg="#fffaf0", fg="#8b4513")
        titulo.pack(pady=15)

        # Frame de la lista
        frame_lista = tk.LabelFrame(self.ventana, text="Citas Programadas", font=("Arial", 11, "bold"),
                                    bg="#fffaf0", fg="#8b4513")
        frame_lista.pack(padx=20, pady=10, fill="both", expand=True)

        self.lista_citas = tk.Listbox(frame_lista, font=("Arial", 10), width=70, height=10)
        self.lista_citas.pack(side="left", fill="y", padx=(10, 0), pady=10)

        scrollbar = tk.Scrollbar(frame_lista, orient="vertical", command=self.lista_citas.yview)
        scrollbar.pack(side="right", fill="y", pady=10)
        self.lista_citas.config(yscrollcommand=scrollbar.set)

        self.lista_citas.bind("<<ListboxSelect>>", self.seleccionar_cita)

        # Frame formulario
        frame_formulario = tk.LabelFrame(self.ventana, text="Datos de la Cita", font=("Arial", 11, "bold"),
                                         bg="#fffaf0", fg="#8b4513")
        frame_formulario.pack(padx=20, pady=10, fill="x")

        # Validación solo para letras (nombres)
        self.validar_letras = self.ventana.register(lambda c: c.isalpha() or c.isspace())

        # Campos del formulario
        self.paciente_entry = self._crear_campo(frame_formulario, "Nombre del Paciente:", validar=self.validar_letras)
        self.doctor_entry = self._crear_campo(frame_formulario, "Nombre del Doctor:", validar=self.validar_letras)
        self.fecha_entry = self._crear_campo(frame_formulario, "Fecha (YYYY-MM-DD):")  # Solo se valida en agregar/editar
        self.hora_entry = self._crear_campo(frame_formulario, "Hora (HH:MM):")         # Solo se valida en agregar/editar

        # Estilos de botones
        estilo_btn = {
            "width": 20,
            "height": 1,
            "font": ("Arial", 10, "bold"),
            "bg": "#ffe4b5",
            "fg": "#8b4513",
            "bd": 0,
            "activebackground": "#ffdead"
        }

        estilo_btn_rojo = estilo_btn.copy()
        estilo_btn_rojo.update({"bg": "#ffcccc", "fg": "#660000", "activebackground": "#ff9999"})

        # Botones de acción
        btn_frame = tk.Frame(self.ventana, bg="#fffaf0")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Agregar", command=self.agregar_cita, **estilo_btn).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Editar seleccionado", command=self.editar_cita, **estilo_btn).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Eliminar seleccionado", command=self.eliminar_cita, **estilo_btn_rojo).grid(row=0, column=2, padx=5)

        # Cargar citas actuales
        self.actualizar_lista()

    def _crear_campo(self, frame, texto, validar=None):
        """Crea un campo de entrada con etiqueta y validación opcional"""
        label = tk.Label(frame, text=texto, bg="#fffaf0", font=("Arial", 10, "bold"))
        label.pack(anchor="w", padx=10, pady=(5, 0))
        if validar:
            entry = tk.Entry(frame, width=50, validate="key", validatecommand=(validar, "%S"))
        else:
            entry = tk.Entry(frame, width=50)
        entry.pack(padx=10, pady=5)
        return entry

    def actualizar_lista(self):
        """Muestra todas las citas programadas en la lista"""
        self.lista_citas.delete(0, tk.END)
        for cita in citas_service.obtener_citas():
            self.lista_citas.insert(tk.END, f"ID {cita.id}: {cita.fecha} {cita.hora} - {cita.paciente} con {cita.doctor}")

    def agregar_cita(self):
        """Agrega una nueva cita a la lista"""
        paciente = self.paciente_entry.get().strip()
        doctor = self.doctor_entry.get().strip()
        fecha = self.fecha_entry.get().strip()
        hora = self.hora_entry.get().strip()

        if not paciente or not doctor or not fecha or not hora:
            messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios.")
            return

        if not re.match(r"^\d{4}-\d{2}-\d{2}$", fecha):
            messagebox.showerror("Formato inválido", "La fecha debe estar en formato YYYY-MM-DD.")
            return

        if not re.match(r"^\d{2}:\d{2}$", hora):
            messagebox.showerror("Formato inválido", "La hora debe estar en formato HH:MM.")
            return

        citas_service.agregar_cita(paciente, doctor, fecha, hora)
        self.actualizar_lista()
        self._limpiar_campos()

    def editar_cita(self):
        """Edita la cita seleccionada con los nuevos datos ingresados"""
        seleccion = self.lista_citas.curselection()
        if not seleccion:
            messagebox.showinfo("Editar", "Selecciona una cita para editar.")
            return

        indice = seleccion[0]
        cita = citas_service.obtener_citas()[indice]

        nuevo_paciente = self.paciente_entry.get().strip()
        nuevo_doctor = self.doctor_entry.get().strip()
        nueva_fecha = self.fecha_entry.get().strip()
        nueva_hora = self.hora_entry.get().strip()

        if not nuevo_paciente or not nuevo_doctor or not nueva_fecha or not nueva_hora:
            messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios.")
            return

        if not re.match(r"^\d{4}-\d{2}-\d{2}$", nueva_fecha):
            messagebox.showerror("Formato inválido", "La fecha debe estar en formato YYYY-MM-DD.")
            return

        if not re.match(r"^\d{2}:\d{2}$", nueva_hora):
            messagebox.showerror("Formato inválido", "La hora debe estar en formato HH:MM.")
            return

        citas_service.editar_cita(cita.id, nuevo_paciente, nuevo_doctor, nueva_fecha, nueva_hora)
        self.actualizar_lista()
        self._limpiar_campos()

    def eliminar_cita(self):
        """Elimina la cita seleccionada después de confirmar"""
        seleccion = self.lista_citas.curselection()
        if not seleccion:
            messagebox.showinfo("Eliminar", "Selecciona una cita para eliminar.")
            return

        indice = seleccion[0]
        cita = citas_service.obtener_citas()[indice]

        confirmar = messagebox.askyesno("Confirmar eliminación", f"¿Eliminar la cita de {cita.paciente} con {cita.doctor} el {cita.fecha}?")
        if confirmar:
            citas_service.eliminar_cita(cita.id)
            self.actualizar_lista()
            self._limpiar_campos()

    def seleccionar_cita(self, event):
        """Carga los datos de la cita seleccionada en el formulario"""
        seleccion = self.lista_citas.curselection()
        if seleccion:
            indice = seleccion[0]
            cita = citas_service.obtener_citas()[indice]
            self.paciente_entry.delete(0, tk.END)
            self.paciente_entry.insert(0, cita.paciente)
            self.doctor_entry.delete(0, tk.END)
            self.doctor_entry.insert(0, cita.doctor)
            self.fecha_entry.delete(0, tk.END)
            self.fecha_entry.insert(0, cita.fecha)
            self.hora_entry.delete(0, tk.END)
            self.hora_entry.insert(0, cita.hora)

    def _limpiar_campos(self):
        """Limpia todos los campos de entrada del formulario"""
        self.paciente_entry.delete(0, tk.END)
        self.doctor_entry.delete(0, tk.END)
        self.fecha_entry.delete(0, tk.END)
        self.hora_entry.delete(0, tk.END)
