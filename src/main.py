import tkinter as tk
from tkinter import ttk
import add_element, exam, schedule

def application_screen():
    # Pantalla de la aplicación
    window = tk.Tk()

    color_background = "#28393b"
    color_text = "#000000"
    color_button = "#4caf50"
    color_button_pressed = "#388e3c"

    window.geometry("960x640")
    window.title("Sistema de Detección de Intrusos")
    window.configure(bg=color_background)

    # Utiliza ttk para estilos mejorados de botones
    style = ttk.Style()
    style.configure("TButton", padding=6, relief="flat", background=color_button, foreground=color_text)
    style.map("TButton", background=[('pressed', color_button_pressed)])

    # Etiqueta de bienvenida
    test_text = tk.Label(window, text="Sistema de Detección de Intrusos", fg=color_text, bg=color_background, font=('Helvetica', 18, 'bold'))
    test_text.pack(pady=10)

    # Botones con estilo mejorado
    new_dir_button = ttk.Button(window, text="Add Directory", command=add_element.add_new_dir)
    new_file_button = ttk.Button(window, text="Add File", command=add_element.add_new_file)
    start_button = ttk.Button(window, text="Start Exam", command=exam.check_integrity)
    check_every_hour = ttk.Button(window, text="Begin Scheduled Exams", command=schedule.schedule_integrity_check)
    exit_button = ttk.Button(window, text="Close Program", command=window.destroy)

    # Empaque de botones
    buttons = [new_dir_button, new_file_button, start_button, check_every_hour, exit_button]
    for button in buttons:
        button.pack(pady=10, padx=20, ipadx=10, ipady=5, fill=tk.X)

    window.mainloop()

if __name__ == '__main__':
    application_screen()
