import nmap, socket, pyfiglet
from netdiscover import *
sys.path.append('./Utiles')
from utiles import *

class Network:
    def __init__(self):
        print(pyfiglet.figlet_format("Auto-Diag"))
        while True : 
            self.ip = input("Entrez une adresse IP (Appuyer sur ENTRER pour utiliser l'adresse IP par défaut):\n" f"{socket.gethostbyname(socket.gethostname())}\n>")
            if check_ip_address(self.ip):
                break
            else:
                print_red(f"L'adresse IP {self.ip} n'est pas au bon format IPv4.")
        
        self.hosts = []
        self.nm = nmap.PortScanner()

    def section_print(self, title):
        print("\n" + "=" * 50)
        print(title)
        print("=" * 50 + "\n")


    def discover_hosts(self):
        while True:
            mask = input(f"Veuillez entrer le masque de sous-réseaux : ")
            if check_subnet_mask(mask):
                break
            else : 
                print_red("Le masque de sous-réseaux n'est pas dans le bon format. Entrer un nombre entre 1 et 32 qui correspond à la notation CIDR")

        if len(self.ip) == 0:
            network = f"{socket.gethostbyname(socket.gethostname())}/{mask}"
        else:
            network = self.ip + f'/{mask}'

        print(f"\nVotre adresse IP est {network}")
        print("Enumération de l'hôte en cours ...")

        disc = Discover()
        hosts = disc.scan(ip_range=network)
        if (not disc):
            print("Aucun hôte découvert")

        for i in hosts:
            ip = i["ip"]
            mac = i["mac"]
            if ip != self.ip:
                print(f"\n{ip} --> {mac} : Host is UP")
                if ip == "10.0.2.15":
                    self.hosts.append(ip)

    def Auto_Diag(self):
        try:
            self.discover_hosts()

            # Create an instance of the Scanner class
            scanner = Scanner()
            scanner.Auto_Diag()

        except KeyboardInterrupt:
            print("\n[x] Fermeture du programme!")

