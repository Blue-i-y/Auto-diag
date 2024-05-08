import socket
import re
import time

def check_ip_address(ip):
    # Vérifie si une chaîne correspond au format d'une adresse IP valide.
    ip_regex = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    if re.match(ip_regex, ip):
        return True  # Retourne True si l'adresse IP est valide.
    else:
        return False  # Retourne False si l'adresse IP n'est pas valide.

def check_subnet_mask(mask):
    # Vérifie si la valeur d'un masque de sous-réseau est valide (entre 1 et 32).
    try:
        value = int(mask)
        if value < 1 or value > 32:
            return False  # Retourne False si la valeur n'est pas entre 1 et 32.
        else:
            return True  # Retourne True si la valeur est valide.
    except ValueError:
        return False  # Retourne False si la valeur n'est pas un entier.

def print_red(text):
    # Affiche du texte en rouge dans la console.
    print("\033[91m{}\033[00m".format(text))

def print_orange(text):
    # Affiche du texte en orange dans la console.
    print("\033[33m{}\033[00m".format(text))

def print_green(text):
    # Affiche du texte en vert dans la console.
    print("\033[92m {}\033[00m".format(text))

def clear_line(second):
    # Efface la ligne actuelle dans la console après un délai.
    time.sleep(second)  # Attend pendant un nombre spécifié de secondes.
    print("\033[A\x1b[0K\r")  # Efface la ligne actuelle dans le terminal.
    print("\033[2A ")  # Déplace le curseur deux lignes plus haut.
    time.sleep(second)  # Attend encore pour un effet de délai.
