import tkinter as tk
from tkinter import scrolledtext
from scanner import Scanner

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Auto-Diag GUI")
        self.geometry("800x600")

        self.result_text = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=80, height=30)
        self.result_text.pack(padx=10, pady=10)

        self.start_button = tk.Button(self, text="Start Auto-Diag", command=self.start_auto_diag)
        self.start_button.pack(pady=10)

    def start_auto_diag(self):
        scanner = Scanner()
        result = scanner.Auto_Diag()

        # Assuming you have a method in Scanner to get the results
        results_to_display = scanner.get_results()

        # Insert results into the text widget
        self.result_text.insert(tk.END, results_to_display)

