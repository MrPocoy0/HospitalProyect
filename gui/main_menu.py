# Autores: Sony, Angelo ,Victor, Franklin
# Descripción: Ventana principal del sistema de citas médicas

import tkinter as tk
from gui.pacientes_gui import PacienteVentana
from gui.doctores_gui import DoctorVentana
from gui.citas_gui import CitaVentana

def mostrar_menu_principal():
    """Función que lanza la ventana principal del sistema"""
    ventana = tk.Tk()
    ventana.title("Sistema de Citas Médicas")
    ventana.geometry("450x350")
    ventana.resizable(False, False)
    ventana.configure(bg="#e6f2ff")  # fondo azul claro

    # Título principal
    titulo = tk.Label(ventana, text="Menú Principal", font=("Arial", 18, "bold"), bg="#e6f2ff", fg="#003366")
    titulo.pack(pady=20)

    # Frame para los botones
    frame_botones = tk.Frame(ventana, bg="#e6f2ff")
    frame_botones.pack(pady=10)

    # Estilo para los botones
    estilo_btn = {
        "width": 30,
        "height": 2,
        "bg": "#cce6ff",
        "fg": "#003366",
        "font": ("Arial", 11, "bold"),
        "bd": 0,
        "activebackground": "#99ccff"
    }

    # Botones del menú
    tk.Button(frame_botones, text="Gestión de Pacientes", command=abrir_pacientes, **estilo_btn).pack(pady=5)
    tk.Button(frame_botones, text="Gestión de Doctores", command=abrir_doctores, **estilo_btn).pack(pady=5)
    tk.Button(frame_botones, text="Gestión de Citas Médicas", command=abrir_citas, **estilo_btn).pack(pady=5)

    # Estilo específico para botón de salir
    estilo_salir = {
        "width": 30,
        "height": 2,
        "bg": "#ffcccc",
        "fg": "#660000",
        "font": ("Arial", 11, "bold"),
        "bd": 0,
        "activebackground": "#ff9999"
    }

    # Botón salir
    tk.Button(ventana, text="Salir", command=ventana.quit, **estilo_salir).pack(pady=15)

    ventana.mainloop()

def abrir_pacientes():
    """Abre la ventana de gestión de pacientes"""
    PacienteVentana()

def abrir_doctores():
    """Abre la ventana de gestión de doctores"""
    DoctorVentana()

def abrir_citas():
    """Abre la ventana de gestión de citas"""
    CitaVentana()
