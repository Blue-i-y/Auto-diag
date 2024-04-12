import json, paramiko,time
from threading import Thread
from ftplib import FTP
from network import Network

class Scanner(Network):
    def __init__(self):
        super().__init__()

    def nmap_scan(self, host):
        print(f"\nNmap scan in progress for: {host}")
        scan_result = self.nm.scan(hosts=host, arguments='-sV -T4 -sC -O')

        filename = f"{host.replace('.', '_')}.json"
        with open(filename, 'w') as file:
            json.dump(scan_result, file)

        
    def print_result(self, host):
        print("Hostname : {}".format(self.nm[host].hostname()))
        print("PORT\tSTATE\tSERVICE")
        for i in range(20, 450):
            try:
                if self.nm[host]["tcp"][i]:
                    print("{}/tcp\t{}\t{}".format(i, self.nm[host]["tcp"][i]["state"], self.nm[host]["tcp"][i]["name"]))
                    print(" | Product : {}".format(self.nm[host]["tcp"][i]["product"]))
                    if self.nm[host]["tcp"][i]["script"]:
                        print(" | Script :")
                        for script in self.nm[host]["tcp"][i]["script"]:
                            print(" | | {} : {}".format(script, self.nm[host]["tcp"][i]["script"][script]))
                    print(" |_Version : {}".format(self.nm[host]["tcp"][i]["version"]))
            except:
                pass
        print(f"\nAnalyse Nmap finie pour {host}")

    def service_detection(self, host):
        if self.nm[host].has_tcp(22):
            print(f"\n Hôte \t {host} \n Port ssh (22) ouvert. \n Tentative de bruteforce sur cet hôte.")
            self.bruteforce(host, "ssh")
        elif self.nm[host].has_tcp(21):
            print(f"\n Hôte \t {host} \n Port ftp (21) ouvert. \n Tentative de bruteforce sur cet hôte.")
            self.bruteforce(host, "ftp")

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
        username = str(input("Veuillez entrer un nom d'utilisateur : \n >"))
        wordl = str(input("Veuillez entrer un dictionnaire de mots de passe (uniquement le nom du fichier sans l'extension) : \n >"))

        with open(f"/usr/share/dirb/wordlists/{wordl}.txt", 'r', encoding = "utf8") as file:
            for line in file.readlines():
                if type == "ssh":
                    th = Thread(target = self.ssh_connect ,args = (ip, username, line.strip()))
                    th.start()
                elif type == "ftp":
                    th = Thread(target = self.ftp_connect ,args = (ip, username, line.strip()))
                    th.start()

    def Auto_Diag(self):
        try:
            self.discover_hosts()

            for i in range(len(self.hosts)):
                host = self.hosts[i]

                self.section_print(f"Port scan for {host}")
                
                try:
                    self.nmap_scan(host)
                    self.print_result(host)
                    self.service_detection(host)
                    # self.save_results_to_word(host)  

                except nmap.PortScannerError as e:
                    print(f"Erreur pendant le scan Nmap pour {host}: {e}")

                except Exception as e:
                    print(f"Erreur pendant le scan Nmap pour {host}: {e}")

                time.sleep(1)

        except KeyboardInterrupt:
            print("\n[x] Program closed!")

"""
    def cve_finder(self):
        try:
            cve_entry = str(input("\nSaisissez un code CVE pour votre recherche:\n>"))
            cve_result = self.cve.id(cve_entry)

            with open(f"cve/{cve_entry}.json", "w", encoding = "utf-8") as f:
                f.write(json.dumps(cve_result, indent = 4, sort_keys = True))
        except:
            pass
"""
