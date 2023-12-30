import nmap, socket, json, pyfiglet, paramiko, sys, time
from pycvesearch import CVESearch
from datetime import datetime
from threading import Thread
from ftplib import FTP
from docx import Document



class Network(object):
    def __init__(self):
        print(pyfiglet.figlet_format("Auto-Diag"))
        self.ip = input(f"Entrer une adresse IP (l'adresse IP de cette machine est par défaut :\n{socket.gethostbyname(socket.gethostname())}, pour la selectionner appuyez sur ENTRER).\n>")
        self.hosts = []
        self.nm = nmap.PortScanner()
        self.cve = CVESearch()
    
    def section_print(self, title):
        print("\n" + "=" * 50)
        print(title)
        print("=" * 50 + "\n")

    def network_scanner(self):
        if len(self.ip) == 0:
            network = f"{socket.gethostbyname(socket.gethostname())}/24"
        else:
            network = self.ip + '/24'
        
        print("\nScan réseau en cours ...")
        self.nm.scan(hosts = network, arguments = "-sn")
        hosts_list = [(x, self.nm[x]['status']['state']) for x in self.nm.all_hosts()]

        print("=" * 50)
        for host, status in hosts_list:
            print("Hôte\t{}\t{}".format(host, status))
            self.hosts.append(host)
        print("=" * 50)
        # print(hosts_list)
    
    def nmap_scan(self, host):
        print(f"\nDébut du scan Nmap pour :\t{host}")
        scan_result = self.nm.scan(hosts = host, arguments = '-sV -p 20-450 --script="vuln and safe"')
        
        with open(f"scan/{host}.csv", "w", encoding = "utf-8") as f:
            f.write(self.nm.csv())

        with open(f"scan/{host}.json", "w", encoding = "utf-8") as f:
            f.write(json.dumps(scan_result, indent = 4, sort_keys = True))
    
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
        print("\nAnalyse Nmap finie pour {}.".format(host))

    def cve_finder(self):
        try:
            cve_entry = str(input("\nSaisissez un code CVE pour votre recherche:\n>"))
            cve_result = self.cve.id(cve_entry)

            with open(f"cve/{cve_entry}.json", "w", encoding = "utf-8") as f:
                f.write(json.dumps(cve_result, indent = 4, sort_keys = True))
        except:
            pass
    
    def ssh_connect(ip, username, password, port = 22):
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
        self.network_scanner()
        for i in range(len(self.hosts)):
            self.nmap_scan(self.hosts[i])
            self.print_result(self.hosts[i])
            self.service_detection(self.hosts[i])
            self.save_results_to_word(self.hosts[i]) 
            time.sleep(1)
            #self.cve_finder()


if __name__ == "__main__":
    try:
        Nscan = Network()
        Nscan.Auto_Diag()
    except KeyboardInterrupt:  
        print("\n[x] Fermeture du programme !")
        sys.exit()
