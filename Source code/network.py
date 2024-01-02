import nmap, socket, pyfiglet

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

    def network_scanner(self):
        if len(self.ip) == 0:
            network = f"{socket.gethostbyname(socket.gethostname())}/24"
        else:
            network = self.ip + '/24'
        
        print("\nScan réseau en cours ...")
        self.nm.scan(hosts = network, arguments = "-Pn")
        hosts_list = [(x, self.nm[x]['status']['state']) for x in self.nm.all_hosts()]

        print("=" * 50)
        for host, status in hosts_list:
            print("Hôte\t{}\t{}".format(host, status))
            self.hosts.append(host)
        print("=" * 50)
        # print(hosts_list)

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

    def Auto_Diag(self):
        try:
            self.network_scanner()

            # Create an instance of the Scanner class
            scanner = Scanner()
            scanner.Auto_Diag()

        except KeyboardInterrupt:
            print("\n[x] Program closed!")

