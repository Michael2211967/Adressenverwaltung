import tkinter as tk
from tkinter import ttk
from functions import center_window

class About:
    def __init__(self, window, title = "Programm XYZ", program = "Programm", version = 1.0):
        self.version = f"Version {version}"
        self.version_window = tk.Toplevel(window)
        self.version_window.title("Über")
        self.style = ttk.Style()
        self.style.configure("font.TButton", font=("Arial", 15))
        self.geometry = center_window(450, 300, self.version_window)
        self.version_window.geometry(self.geometry)
        self.version_window.transient(window)
        self.version_window.grab_set()

        self.version_title = ttk.Label(self.version_window, font=("Arial Black", 20), text = title)
        self.version_title.pack(padx=20, pady=10)

        self.version_program = ttk.Label(self.version_window, font=("Arial Black", 18), text=program)
        self.version_program.pack(padx=20, pady=10)

        self.version_label = ttk.Label(self.version_window, font=("Arial", 18), text=self.version)
        self.version_label.pack(padx=20, pady=10)  # Etwas weniger vertikaler Abstand

        self.ok_button = ttk.Button(self.version_window, text="OK", style="font.TButton", command=self.version_window.destroy)
        self.ok_button.pack(side="bottom", pady=10)

        window.wait_window(self.version_window)