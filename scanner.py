import json, paramiko,time,
from threading import Thread
from ftplib import FTP

class Scanner(Network):
    def __init__(self):
        super().__init__()

    def cve_finder(self):
        try:
            cve_entry = str(input("\nSaisissez un code CVE pour votre recherche:\n>"))
            cve_result = self.cve.id(cve_entry)

            with open(f"cve/{cve_entry}.json", "w", encoding = "utf-8") as f:
                f.write(json.dumps(cve_result, indent = 4, sort_keys = True))
        except:
            pass

    def ssh_connect(self, ip, username, password, port=22):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, port, username, password)
            print("Mot de passe trouvé : " + password)
            return True
        except:
            return False

    def ftp_connect(self, ip, user, password):
        try:
            FTP(ip, user = user, passwd = password)
            print("Mot de passe trouvé : " + password)
            return True
        except:
            return False
            
    def bruteforce(self, ip, type):
        username = str(input("Entrer un nom d'utilisateur :\n>"))
        wordl = str(input("Entrer un dictionnaire de mots de passe (juste le nom du fichier, sans l'extension) :\n>"))

        with open(f"wordlists\{wordl}.txt", 'r', encoding = "utf8") as file:
            for line in file.readlines():
                if type == "ssh":
                    th = Thread(target = self.ssh_connect ,args = (ip, username, line.strip()))
                    th.start()
                elif type == "ftp":
                    th = Thread(target = self.ftp_connect ,args = (ip, username, line.strip()))
                    th.start()

    def service_detection(self, host):
        if self.nm[host].has_tcp(22):
            print("\nHôte\t{}\nPort ssh (22) ouvert.\nLancement d'un bruteforce sur cet hôte.".format(host))
            self.bruteforce(host, "ssh")
        elif self.nm[host].has_tcp(21):
            print("\nHôte\t{}\nPort ftp (21) ouvert.\nLancement d'un bruteforce sur cet hôte.".format(host))
            self.bruteforce(host, "ftp")

    def Auto_Diag(self):
        for i in range(len(self.hosts)):
            self.nmap_scan(self.hosts[i])
            self.print_result(self.hosts[i])
            self.service_detection(self.hosts[i])
            self.save_results_to_word(self.hosts[i]) 
            time.sleep(1)
            #self.cve_finder()
