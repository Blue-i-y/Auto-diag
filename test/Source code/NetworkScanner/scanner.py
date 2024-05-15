import json
import paramiko
import time
from threading import Thread
from ftplib import FTP
from network import Network
from ReportGen.ExcelGen import *
from ReportGen.GraphReport import *
from ReportGen.DocGen import *
from Vuln_search.ExploitDB import *
from Vuln_search.NISTSearch import *
from Utiles.utiles import *
from WebPentest.DirEnum import *
from WebPentest.SubEnum import * 

class Scanner(Network):
    def __init__(self):
        super().__init__()

    def nmap_scan(self, host):
        print(f"\nNmap scan in progress for: {host}")
        scan_result = self.nm.scan(hosts=host, arguments='-sV -T4 -sC -O')
        path = f"./Doc/Report/JSON/Hosts/{host}.json"
        pathxlsx = f"./Doc/Report/Excel/Recon/{host}.xlsx"
        with open(path, 'w') as file:
            json.dump(scan_result, file, indent=4)
        recon_excel(scan_result, pathxlsx)

    def get_services(self, path):
        path_se = []
        unique_services = set()
        with open(path, 'r') as f:
            data = json.load(f)
        for host in data['scan']:
            for service_data in data['scan'][host]['tcp'].values():
                product = service_data['product']
                version = service_data['version']
                service = f"{product} {version}"
                search_exploit(service)
                unique_services.add(service)
                path_se.append(f"./Doc/Report/JSON/Exploits/{service}.json")
        return list(unique_services), path_se

    def get_shell_exploit(self, path):
        Exploit = []
        Shell = []
        with open(path, "r") as f:
            data = json.load(f)
        for exploit in data.get("RESULTS_EXPLOIT", []):
            if exploit.get('Title'):
                titre = exploit['Title']
                URL = exploit['URL']
                Exploit.append({
                    "Nom d'Exploit": titre,
                    "URL": URL
                })
        for shell in data.get("RESULTS_SHELLCODE", []):
            if shell.get('Title'):
                titre = shell['Title']
                URL = shell['URL']
                Shell.append({
                    "Nom d'Exploit": titre,
                    "URL": URL
                })
        return Exploit, Shell

    def get_shell_exploit_from_files(self, paths):
        all_exploits = []
        all_shells = []
        for path in paths:
            (exploits, shells) = self.get_shell_exploit(path)
            all_exploits.extend(exploits)
            all_shells.extend(shells)
        return all_exploits, all_shells

    def print_nmap(self, host):
        print(f"Hostname : {self.nm[host].hostname()}")
        print("PORT\tSTATE\tSERVICE")
        
        # Parcours de tous les ports dans nm['host']['tcp']
        for port in self.nm[host]["tcp"]:
            state = self.nm[host]["tcp"][port]["state"]
            service = self.nm[host]["tcp"][port]["name"]
            product = self.nm[host]["tcp"][port].get("product", "")
            version = self.nm[host]["tcp"][port].get("version", "")
            scripts = self.nm[host]["tcp"][port].get("script", {})

            print(f"{port}/tcp\t{state}\t{service}")
            print(f" | Product : {product}")
            
            if scripts:
                print(" | Script :")
                for script, result in scripts.items():
                    print(f" | | {script} : {result}")
                    
            print(f" |_Version : {version}")

        print_green(f"\nAnalyse Nmap finie pour {host}")

    def attack_service(service, port, host): #Toute fonction doit generer un rapport a rajouté si c'est possible dans le rapport final 
        if service == 'ftp':
            confirm = input(f'le service {service} est ouvert dans le port {port} \n voulez vous faire une attack par dictionnaire ? (press y to accept) ')
            if confirm == 'y':
                ftp_bruteforce(host, port)  #Fonction a faire
            else: print_orange(f'attack bruteforce ignoré ...')
        if service == 'ssh':
            confirm = input(f'le service {service} est ouvert dans le port {port} \n voulez vous faire une attack par dictionnaire ? (press y to accept) ')
            if confirm == 'y':
                ssh_bruteforce(host, port)  #regler affichage + generation de rapport 
            else: print_orange('attack bruteforce ignoré ...')
        if service == 'ms-wbt-server':
            confirm = input(f'le service {service} est ouvert dans le port {port} \n voulez vous faire une attack par dictionnaire ? (press y to accept) ')
            if confirm == 'y':
                rdp_bruteforce(host, port)
            else: print_orange('attack bruteforce ignoré ...')
        if service == 'http':
            print(f'Le service http est ouvert dans le port {port}')
            while 1 :
                confirm = input(f'Choisis le numero de test souhaité : \n 1 - Sub enumeration \n 2 - dir enumeration \n Press any other key to exit ')
                if confirm == '1':
                    SubEnum()#fonction a regler 
                elif confirm == '2':
                    DirEnum()#fonction a regler
                else : break
            print_orange("L'attack sur le service http est términé  ...")


    def service_detection(self, host):
        attack = ['ftp', 'rdp', 'ssh', 'http', 'ms-wbt-server']
        detected_services = []

        for port in self.nm[host]["tcp"]:
            service = self.nm[host]["tcp"][port]["name"]
            
            if service.lower() in attack:
                detected_services.append((port, service))
        
        if detected_services:
            print(f"Detected services on {host}: ")
            for port, service in detected_services:
                print(f"Port {port}: {service}")
        else:
            print(f"No attack services detected on {host}")


        if self.nm[host].has_tcp(22):
            print(f"\n Hôte \t {host} \n Port ssh (22) ouvert. \n Lancement d'un bruteforce sur cet hôte.")
            self.bruteforce(host, "ssh")
        elif self.nm[host].has_tcp(21):
            print(f"\n Hôte \t {host} \n Port ftp (21) ouvert. \n Lancement d'un bruteforce sur cet hôte.")
            self.bruteforce(host, "ftp")


    def auto_diag(self):
        services = []
        Exploits = []
        Shells = []
        api_key = {'apiKey': '97410594-f2e3-4e00-a63e-1e6eb5dcef38'}
        try:
            self.discover_hosts()
            for i in range(len(self.hosts)):
                host = self.hosts[i]
                self.section_print(f"Port scan for {host}")
                path_host = f"./Doc/Report/JSON/Hosts/{host}.json"
                try:
                    self.nmap_scan(host)
                    confirm = input("Voulez vous afficher le resultat de nmap (press y to accept)  : \n >")
                    if confirm == "y":
                        self.print_nmap(host)
                    else:
                        print_orange("Affichage resultas nmap ignoré !\n")
                    print("Recherche des service ouvert ... \n")
                    services, path_se = self.get_services(path_host)
                    print("Rechreche des CVE dans NIST API ...\n")
                    display, report, remediation, graph = Vuln_search(services, api_key, "./Doc/Report/JSON/Vulns", host)
                    print("Rechreche d'exploits dans ExploitDB ...\n")
                    (Exploits, Shells) = self.get_shell_exploit_from_files(path_se)
                    confirm = input("Voulez vous afficher le resultat des CVE (press y to accept) : \n >")
                    if confirm == "y":
                        vuln_display(display)
                    else:
                        print_orange("Affichage CVE ignoré !\n")
                    vuln_Excel(report, "./Doc/Report/Excel/Vulns", host)
                    remed_Excel(remediation, "./Doc/Report/Excel/Remed", host)
                    exploit_Excel(Exploits, Shells, "./Doc/Report/Excel/ExploitDB", host)
                    graph_cve(graph, host)
                    graph_exploit(len(Exploits), len(Shells), host)
                    create_report(host)
                    break
                    self.service_detection(host)
                except nmap.PortScannerError as e:
                    print_orange(f"Error during Nmap scan for {host}: {e}")
                except Exception as e:
                    print_orange(f"Error during nmap scan for {host}: {e}")
                time.sleep(1)
        except KeyboardInterrupt:
            print_red("\n[x] Program closed!")

# Utilisation de la classe Scanner pour exécuter le diagnostic automatique
if __name__ == "__main__":
    scanner = Scanner()
    scanner.Auto_Diag()



'''
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
        username = str(input("Entrer un nom d'utilisateur : \n >"))
        wordl = str(input("Entrer un dictionnaire de mots de passe (juste le nom du fichier, sans l'extension) : \n >"))

        with open(f"/usr/share/wordlists/{wordl}.txt", 'r', encoding = "utf8") as file:
            for line in file.readlines():
                if type == "ssh":
                    th = Thread(target = self.ssh_connect ,args = (ip, username, line.strip()))
                    th.start()
                elif type == "ftp":
                    th = Thread(target = self.ftp_connect ,args = (ip, username, line.strip()))
                    th.start()
'''