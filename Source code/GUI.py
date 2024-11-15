import tkinter as tk
from tkinter import ttk
import ipaddress

# Couleurs pour le thème sombre et clair
dark_background = "#2e2e2e"
light_background = "#f5f5f5"

# Fonction pour changer entre le mode clair et sombre
def toggle_theme():
    if style.theme_use() == 'default':
        style.theme_use('clam')
        style.configure("TFrame", background=dark_background)
        style.configure("TLabel", background=dark_background, foreground="white")
        style.configure("TButton", background=dark_background, foreground="white")
        root.configure(background=dark_background)
    else:
        style.theme_use('default')
        root.configure(background=light_background)

def gui_on_check():
    print("Fonction en cours de préparation")

# Fonction d'action pour le bouton 'Hashage'
def hash_action():
    print("Hashage en cours...")

def clear_output():
    output_text.delete(1.0, tk.END)

def validate_ip():
    try:
        ipaddress.ip_address(ip_entry.get())
        print("Adresse IP valide")
    except ValueError:
        print("Adresse IP invalide")

class AutoDiagApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto-Diag")
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)
        self.create_tabs()
        self.create_theme_button()

    def create_tabs(self):
        # Création des onglets
        self.tab_target = ttk.Frame(self.notebook)
        self.tab_hash = ttk.Frame(self.notebook)
        self.tab_start = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_target, text='Target')
        self.notebook.add(self.tab_hash, text='Hash')
        self.notebook.add(self.tab_start, text='Start')

        # Configuration de chaque onglet
        self.configure_target_tab()
        self.configure_hash_tab()
        self.configure_start_tab()

    def configure_target_tab(self):
        # Titre
        title_label = ttk.Label(self.tab_target, text="Auto-Diag", font=("Arial", 20))
        title_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Entrées pour IP et Masque
        ip_label = ttk.Label(self.tab_target, text="Address IP")
        ip_label.grid(row=1, column=0, sticky=tk.W)
        self.ip_entry = ttk.Entry(self.tab_target)
        self.ip_entry.grid(row=1, column=1, sticky=(tk.W, tk.E))

        mask_label = ttk.Label(self.tab_target, text="Masque")
        mask_label.grid(row=2, column=0, sticky=tk.W)
        self.mask_entry = ttk.Entry(self.tab_target)
        self.mask_entry.grid(row=2, column=1, sticky=(tk.W, tk.E))

        # Options avec des cases à cocher
        options_label = ttk.Label(self.tab_target, text="Options")
        options_label.grid(row=3, column=0, sticky=tk.W, pady=(10,0))

        verbs_checkbox = ttk.Checkbutton(self.tab_target, text="Verbose", onvalue=1, offvalue=0, command=gui_on_check)
        verbs_checkbox.grid(row=3, column=1, sticky=tk.W)
        bruteforce_checkbox = ttk.Checkbutton(self.tab_target, text="BruteForce", onvalue=1, offvalue=0, command=gui_on_check)
        bruteforce_checkbox.grid(row=3, column=2, sticky=tk.W)

        # Choix du type de rapport
        report_label = ttk.Label(self.tab_target, text="Rapport")
        report_label.grid(row=4, column=0, sticky=tk.W, pady=(10,0))
        excel_checkbox = ttk.Checkbutton(self.tab_target, text="Excel", onvalue=1, offvalue=0, command=gui_on_check)
        excel_checkbox.grid(row=4, column=1, sticky=tk.W)
        docx_checkbox = ttk.Checkbutton(self.tab_target, text="docx", onvalue=1, offvalue=0, command=gui_on_check)
        docx_checkbox.grid(row=4, column=2, sticky=tk.W)
        json_checkbox = ttk.Checkbutton(self.tab_target, text="JSON", onvalue=1, offvalue=0, command=gui_on_check)
        json_checkbox.grid(row=4, column=3, sticky=tk.W)

        # Affichage de la console
        console_label = ttk.Label(self.tab_target, text="Affichage")
        console_label.grid(row=5, column=0, sticky=tk.W, pady=(10,0))
        console_checkbox = ttk.Checkbutton(self.tab_target, text="Console", onvalue=1, offvalue=0, command=gui_on_check)
        console_checkbox.grid(row=5, column=1, sticky=tk.W)

        # Redimensionnement
        self.tab_target.grid_columnconfigure(1, weight=1)

    def configure_hash_tab(self):
        # Onglet 'Hash'
        hash_button = ttk.Button(self.tab_hash, text="Hashage", command=hash_action)
        hash_button.pack(pady=20)

    def configure_start_tab(self):
        # Onglet 'Start'
        self.output_text = tk.Text(self.tab_start, height=20)
        self.output_text.grid(row=0, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S))

        start_button = ttk.Button(self.tab_start, text="Start")
        start_button.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        stop_button = ttk.Button(self.tab_start, text="Stop")
        stop_button.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        save_button = ttk.Button(self.tab_start, text="Save Output")
        save_button.grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        clear_button = ttk.Button(self.tab_start, text="Clear Output", command=clear_output)
        clear_button.grid(row=1, column=3, sticky=tk.W, padx=5, pady=5)

        # Redimensionnement
        self.tab_start.grid_columnconfigure(0, weight=1)
        self.tab_start.grid_columnconfigure(1, weight=1)
        self.tab_start.grid_columnconfigure(2, weight=1)
        self.tab_start.grid_columnconfigure(3, weight=1)
        self.tab_start.grid_rowconfigure(0, weight=1)

    def create_theme_button(self):
        theme_button = ttk.Button(self.root, text="Basculer Mode Clair/Sombre", command=toggle_theme)
        theme_button.pack(side=tk.BOTTOM, pady=5)

# Création de la fenêtre principale et de l'application
root = tk.Tk()
style = ttk.Style(root)
app = AutoDiagApp(root)

# Lancement de l'interface graphique
root.mainloop()
