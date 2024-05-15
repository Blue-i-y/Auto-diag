import nmap
import socket
import pyfiglet
from netdiscover import Discover
import os
from Utiles.utiles import check_ip_address, check_subnet_mask, print_red
from ReportGen.ExcelGen import hosts_excel


class Network:
    def __init__(self):
        try:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(pyfiglet.figlet_format("Auto-Diag"))
            self.ip = self.get_valid_ip()
            
            self.hosts = []
            self.nm = nmap.PortScanner()
        except KeyboardInterrupt:
            print_red("\n[x] Program closed!")
            sys.exit()
    
    def get_valid_ip(self):
        while True:
            ip = input("Enter an IP address:\n > ")
            if check_ip_address(ip):
                return ip
            else:
                print_red(f"The IP address {ip} is not in the correct IPv4 format.")

    def section_print(self, title):
        print("\n" + "=" * 50)
        print(title)
        print("=" * 50 + "\n")


    def discover_hosts(self):
        while True:
            mask = input(f"Enter your mask : ")
            if check_subnet_mask(mask):
                break
            else : 
                print_red("le maque n'est pas dans le bon format. Entrer un nombre entre 1 et 32")

        if len(self.ip) == 0:
            network = f"{socket.gethostbyname(socket.gethostname())}/{mask}"
        else:
            network = self.ip + f'/{mask}'

        print(f"\nyour IP address is {network}")
        print("host enumeration en cours ...")

        disc = Discover()
        hosts = disc.scan(ip_range=network)
        if (not disc):
            print("there is no alive hosts")
        enum = []
        for i in hosts:
            ip = i["ip"]
            mac = i["mac"]
            enum.append({
                'Host': ip,
                'Adresse mac': mac
            })
            if ip != self.ip:
                print(f"\n{ip} --> {mac} : \033[92m Host is UP !\033[00m")
                if ip == "10.0.2.15":
                    self.hosts.append(ip)

        hosts_excel(enum, './Doc/Report/Excel/Hosts.xlsx')

    def Auto_Diag(self):
        try:
            self.discover_hosts()

            scanner = Scanner()
            scanner.Auto_Diag()

        except KeyboardInterrupt:
            print_red("\n[x] Program closed!")