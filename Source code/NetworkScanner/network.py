import nmap
import socket
import pyfiglet
from netdiscover import Discover
import os
from Utiles.utiles import check_ip_address, check_subnet_mask, print_red
from ReportGen.ExcelGen import hosts_excel

class Network:
    def __init__(self):
        # Efface l'écran du terminal, compatible avec Windows et les autres OS
        try:
            os.system('cls' if os.name == 'nt' else 'clear')
            # Affiche le titre "Auto-Diag" en ASCII art
            print(pyfiglet.figlet_format("Auto-Diag"))
            # Initialise l'adresse IP avec une validation
            self.ip = self.get_valid_ip()
            self.hosts = []  # Liste pour stocker les hôtes découverts
            self.nm = nmap.PortScanner()  # Initialise le scanner de ports Nmap
        except KeyboardInterrupt:
            # Gère l'interruption par l'utilisateur et ferme le programme proprement
            print_red("\n[x] Fermeture du programme!")
            sys.exit()
    
    def get_valid_ip(self):
        # Boucle jusqu'à obtenir une adresse IP valide de l'utilisateur
        while True:
            ip = input("Entrer une adresse IP:\n > ")
            if check_ip_address(ip):
                return ip
            else:
                print_red(f"L'adresse IP {ip} n'est pas au format IPv4.")

    def section_print(self, title):
        # Affiche un titre de section avec des bordures
        print("\n" + "=" * 50)
        print(title)
        print("=" * 50 + "\n")

    def discover_hosts(self):
        # Demande le masque de sous-réseau et valide l'entrée
        while True:
            mask = input(f"Entrer le masque : ")
            if check_subnet_mask(mask):
                break
            else:
                print_red("Le masque n'est pas au bon format. Veuillez rentrer un masque en notation CIDR compris entre 1 et 32")
        
        # Définit le réseau en fonction de l'IP et du masque
        if len(self.ip) == 0:
            network = f"{socket.gethostbyname(socket.gethostname())}/{mask}"
        else:
            network = self.ip + f'/{mask}'
        
        print(f"\nL'adresse IP est : {network}")
        print("Enumération de l'hôte en cours ...")
        
        # Initialise la découverte de réseau et scanne les hôtes vivants
        disc = Discover()
        hosts = disc.scan(ip_range=network)
        if (not disc):
            print("Aucun hôte vivant")
        
        enum = []
        for i in hosts:
            ip = i["ip"]
            mac = i["mac"]
            enum.append({
                'Host': ip,
                'Mac Address': mac
            })
            if ip != self.ip:
                print(f"\n{ip} --> {mac} : \033[92m Hôte vivant !\033[00m")
                if ip == "10.0.2.15":
                    self.hosts.append(ip)
        
        # Génère un fichier Excel avec les informations des hôtes
        hosts_excel(enum, './Doc/Report/Excel/Hosts.xlsx')

    def Auto_Diag(self):
        # Lance la découverte des hôtes et une procédure de diagnostic automatique
        try:
            self.discover_hosts()

            scanner = Scanner()
            scanner.Auto_Diag()

        except KeyboardInterrupt:
            # Gère l'interruption par l'utilisateur pendant le diagnostic
            print_red("\n[x] Fermeture du programme!")
