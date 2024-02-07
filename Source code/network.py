import nmap, socket, pyfiglet
from netdiscover import *

class Network:
    def __init__(self):
        print(pyfiglet.figlet_format("Auto-Diag"))
        self.ip = input("Enter an IP address (press ENTER to use the default IP address):\n"
                        f"{socket.gethostbyname(socket.gethostname())}\n>")
        self.hosts = []
        self.nm = nmap.PortScanner()

    def section_print(self, title):
        print("\n" + "=" * 50)
        print(title)
        print("=" * 50 + "\n")
    
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

    def discover_hosts(self):
        mask = input(f"Enter your mask : ")

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

        print("Alive hosts_list :")
        for i in hosts:
            ip = i["ip"]
            mac = i["mac"]
            print(f"\n{ip} --> {mac}")
        return hosts

    """def network_scanner(self):
        mask = input(f"Enter your mask : ")
        if len(self.ip) == 0:
            network = f"{socket.gethostbyname(socket.gethostname())}/{mask}"
        else:
            network = self.ip + f'/{mask}'
        print(f"\nyour IP address is {network}")
        print("\nScan réseau en cours ...")
        self.nm.scan(hosts = network, arguments = "-Pn -F")
        print("\n nm scan finished")
        hosts_list = [(x, self.nm[x]['status']['state']) for x in self.nm.all_hosts()]

        print("=" * 50)
        for host, status in hosts_list:
            print("Hôte\t{}\t{}".format(host, status))
            self.hosts.append(host)
        print("=" * 50)
        print(hosts_list)"""



    def Auto_Diag(self):
        try:
            self.network_scanner()

            # Create an instance of the Scanner class
            scanner = Scanner()
            scanner.Auto_Diag()

        except KeyboardInterrupt:
            print("\n[x] Program closed!")

