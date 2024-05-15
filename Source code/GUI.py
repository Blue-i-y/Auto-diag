import tkinter as tk
from tkinter import ttk

# Fonction pour changer entre le mode clair et sombre
def toggle_theme():
    if style.theme_use() == 'default':
        style.theme_use('alt')
        root.configure(background=dark_background)
        for widget in root.winfo_children():
            if isinstance(widget, ttk.Frame):
                for child in widget.winfo_children():
                    child.configure(background=dark_background, foreground='white')
    else:
        style.theme_use('default')
        root.configure(background=light_background)
        for widget in root.winfo_children():
            if isinstance(widget, ttk.Frame):
                for child in widget.winfo_children():
                    child.configure(background=light_background, foreground='black')
                    
# Fonction d'action pour le bouton 'Hashage'
def hash_action():
    print("Hashage en cours...")

# Création de la fenêtre principale
root = tk.Tk()
root.title("Auto-Diag")

# Configuration du gestionnaire d'onglets (notebook)
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# Création des onglets
tab_target = ttk.Frame(notebook)
tab_hash = ttk.Frame(notebook)
tab_start = ttk.Frame(notebook)

notebook.add(tab_target, text='Target')
notebook.add(tab_hash, text='Hash')
notebook.add(tab_start, text='Start')

# Configuration de l'onglet 'Target' (premier onglet)
# Titre de l'onglet
title_label = ttk.Label(tab_target, text="Auto-Diag", font=("Arial", 20))
title_label.grid(row=0, column=0, columnspan=3, pady=10)

# Entrées pour IP et Masque
ip_label = ttk.Label(tab_target, text="Address IP")
ip_entry = ttk.Entry(tab_target)
mask_label = ttk.Label(tab_target, text="Masque")
mask_entry = ttk.Entry(tab_target)

ip_label.grid(row=1, column=0, sticky=tk.W)
ip_entry.grid(row=1, column=1, sticky=(tk.W, tk.E))
mask_label.grid(row=2, column=0, sticky=tk.W)
mask_entry.grid(row=2, column=1, sticky=(tk.W, tk.E))

# Options avec des cases à cocher
options_label = ttk.Label(tab_target, text="Options")
verbs_checkbox = ttk.Checkbutton(tab_target, text="Verbose",onvalue=1,offvalue=0,command=gui_on_check)
bruteforce_checkbox = ttk.Checkbutton(tab_target, text="BruteForce",onvalue=1,offvalue=0,command=gui_on_check)

options_label.grid(row=3, column=0, sticky=tk.W, pady=(10,0))
verbs_checkbox.grid(row=3, column=1, sticky=tk.W)
bruteforce_checkbox.grid(row=3, column=2, sticky=tk.W)

# Choix du type de rapport
report_label = ttk.Label(tab_target, text="Rapport")
excel_checkbox = ttk.Checkbutton(tab_target, text="Excel",onvalue=1,offvalue=0,command=gui_on_check)
docx_checkbox = ttk.Checkbutton(tab_target, text="docx",onvalue=1,offvalue=0,command=gui_on_check)
json_checkbox = ttk.Checkbutton(tab_target, text="JSON",onvalue=1,offvalue=0,command=gui_on_check)

report_label.grid(row=4, column=0, sticky=tk.W, pady=(10,0))
excel_checkbox.grid(row=4, column=1, sticky=tk.W)
docx_checkbox.grid(row=4, column=2, sticky=tk.W)
json_checkbox.grid(row=4, column=3, sticky=tk.W)

# Affichage de la console
console_label = ttk.Label(tab_target, text="Affichage")
console_checkbox = ttk.Checkbutton(tab_target, text="Console",onvalue=1,offvalue=0,command=gui_on_check)

console_label.grid(row=5, column=0, sticky=tk.W, pady=(10,0))
console_checkbox.grid(row=5, column=1, sticky=tk.W)

# Configuration pour le redimensionnement automatique des éléments
tab_target.grid_columnconfigure(1, weight=1)

# Code pour le deuxième onglet (Start)
# ...

# Onglet 'Hash'
hash_button = ttk.Button(tab_hash, text="Hashage", command=hash_action)
hash_button.pack(pady=20)

# Configuration du gestionnaire de mise en page pour l'onglet 'Start'
output_text = tk.Text(tab_start, height=20)
output_text.grid(row=0, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S))

start_button = ttk.Button(tab_start, text="Start")
stop_button = ttk.Button(tab_start, text="Stop")
save_button = ttk.Button(tab_start, text="Save Output")
clear_button = ttk.Button(tab_start, text="Clear Output")

start_button.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
stop_button.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
save_button.grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
clear_button.grid(row=1, column=3, sticky=tk.W, padx=5, pady=5)

# Configuration pour le redimensionnement automatique des boutons dans l'onglet 'Start'
tab_start.grid_columnconfigure(0, weight=1)
tab_start.grid_columnconfigure(1, weight=1)
tab_start.grid_columnconfigure(2, weight=1)
tab_start.grid_columnconfigure(3, weight=1)
tab_start.grid_rowconfigure(0, weight=1)


# Bouton pour changer le thème
theme_button = ttk.Button(root, text="Basculer Mode Clair/Sombre", command=toggle_theme)
theme_button.pack(side=tk.BOTTOM, pady=5)

# Lancement de l'interface graphique
root.mainloop()
