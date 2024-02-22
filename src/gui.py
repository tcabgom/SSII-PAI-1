import tkinter as tk

def application_screen():
    # Pantalla de la aplicación
    window = tk.Tk()

    color_background =     "#28393b"
    color_text =           "#ffffff"
    color_button =         "#4caf50"
    color_button_pressed = "#388e3c"

    window.geometry("960x640")
    window.title("Sistema de Detección de Intrusos")
    window.configure(bg=color_background)

    test_text = tk.Label(window, text="Welcome", fg=color_text, bg=color_background)
    new_element_button = tk.Button(window, text="Add Element", bg=color_button, activebackground=color_button_pressed)
    log_file_button = tk.Button(window, text="Open Log File", bg=color_button, activebackground=color_button_pressed)
    start_button = tk.Button(window, text="Start Exam", bg=color_button, activebackground=color_button_pressed)
    exit_button = tk.Button(window, text="Close Program", bg=color_button, activebackground=color_button_pressed)

    test_text.pack(pady=10)
    new_element_button.pack(pady=5)
    log_file_button.pack(pady=5)
    start_button.pack(pady=5)
    exit_button.pack(pady=5)
    window.mainloop()
