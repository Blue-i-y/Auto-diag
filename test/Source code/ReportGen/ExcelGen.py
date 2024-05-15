import pandas as pd
import json
import os
import sys 


def resize_table(writer, df):
    worksheet = writer.sheets['Sheet1']

    for i, col in enumerate(df.columns):
        column_len = max(df[col].astype(str).map(len).max(), len(col))
        worksheet.set_column(i, i, column_len)

    writer.close()

def hosts_excel(data, output_file):
    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame(data)
    
    writer = pd.ExcelWriter(output_file, engine='xlsxwriter')
    data.to_excel(writer, index=False, header=False)
    resize_table(writer, data)



def recon_excel(data, path):
    for host in data['scan']:
        ipv4 = data['scan'][host]['addresses']['ipv4']
        mac = data['scan'][host]['addresses']['mac']
        vendor = data['scan'][host]['vendor'][mac]
        ports = list(data['scan'][host]['tcp'].keys())
        cpe_list = [service['cpe'] for service in data['scan'][host]['tcp'].values()]
        products = [service['product'] for service in data['scan'][host]['tcp'].values()]
        versions = [service['version'] for service in data['scan'][host]['tcp'].values()]
        names = [service['name'] for service in data['scan'][host]['tcp'].values()]
        donnees = []

        for port, cpe, product, version, name in zip(ports, cpe_list, products, versions, names):
            donnees.append({
                'IPv4': ipv4,
                'Vendor': vendor,
                'Ports': port,
                'Nom': name,
                'Produit': product,
                'Version': version,
                'CPE': cpe
            })

    df = pd.DataFrame(donnees)

    writer = pd.ExcelWriter(path, engine='xlsxwriter')
    df.to_excel(writer, index=False)

    resize_table(writer, df)


def exploit_Excel(Exploits, Shells, path, host):

    if not os.path.exists(path + f"/{host}"):
        os.makedirs(path + f"/{host}")

    if Exploits:
        pathexploit = path + f"/{host}/exploit.xlsx"
        df_exploit = pd.DataFrame(Exploits)
        writer_exploit = pd.ExcelWriter(pathexploit, engine='xlsxwriter')
        df_exploit.to_excel(writer_exploit, index=False)
        resize_table(writer_exploit, df_exploit)

    if Shells:
        pathshell = path + f"/{host}/shell.xlsx"
        df_shell = pd.DataFrame(Shells)
        writer_shell = pd.ExcelWriter(pathshell, engine='xlsxwriter')
        df_shell.to_excel(writer_shell, index=False)
        resize_table(writer_shell, df_shell)


def vuln_Excel(report, path, host):
    df = pd.DataFrame(report)
    path = f"{path}/{host}.xlsx"
    writer = pd.ExcelWriter(path, engine='xlsxwriter')
    df.to_excel(writer, index=False)

    resize_table(writer, df)


def remed_Excel(remediation, path, host):
    df = pd.DataFrame(remediation)
    path = f"{path}/{host}.xlsx"
    writer = pd.ExcelWriter(path, engine='xlsxwriter')
    df.to_excel(writer, index=False)

    resize_table(writer, df)