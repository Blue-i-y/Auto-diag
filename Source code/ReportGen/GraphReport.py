import matplotlib.pyplot as plt
from Utiles.utiles import *


def graph_exploit(exploit, shell, host):
    categories = ['Exploit', 'Shell']
    values = [exploit, shell]
    colors = ['red' if value <= 4 else 'green' for value in values]
    plt.bar(categories, values, color=colors)
    plt.xlabel('Categories')
    plt.ylabel('Values')
    plt.title("Rapport Exploits/Shells     Source'ExploitDB'")
    plt.savefig(f'./Doc/Report/PNG/Exploit/{host}.png')
    plt.close()
    print_green(f'exploit graph report for {host} is created')


def graph_cve(data, host):
    for item in data:
        HIGH = item["HIGH"]
        MEDIUM = item["MEDIUM"]
        LOW = item["LOW"]
    plt.bar('HIGH', HIGH, color='red')
    plt.bar('MEDIUM', MEDIUM, color='orange')
    plt.bar('LOW', LOW, color='green')
    plt.xlabel('Categories')
    plt.ylabel('Values')
    plt.title("Rapport CVE     Source'NIST API'")
    plt.savefig(f'./Doc/Report/PNG/Vulns/{host}.png')
    plt.close()
    print_green(f'CVE graph report for {host} is created')
