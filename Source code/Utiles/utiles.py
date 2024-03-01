import socket
import re

def check_ip_address(ip):
    # Vérifier si l'adresse IP correspond au format IPv4
    ip_regex = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    if re.match(ip_regex, ip):
        return True
    else:
        return False

def check_subnet_mask(mask):
    try:
        value = int(mask)
        if value < 1 or value > 32:
            return False
        else:
            return True
    except ValueError:
        return False

def print_red(text):
    print("\033[91m{}\033[00m".format(text))
