import pandas as pd
import os

def resize_table(writer, df):
    # Redimensionne les colonnes d'une feuille Excel en fonction de la longueur du contenu.
    worksheet = writer.sheets['Sheet1']  # Accède à la feuille 'Sheet1' dans le fichier Excel.
    for i, col in enumerate(df.columns):  # Itère sur chaque colonne du dataframe.
        column_len = max(df[col].astype(str).map(len).max(), len(col))  # Détermine la longueur maximale du contenu ou du titre de la colonne.
        worksheet.set_column(i, i, column_len)  # Ajuste la largeur de la colonne.
    writer.close()  # Ferme le writer après redimensionnement.

def hosts_excel(data, output_file):
    # Crée un fichier Excel pour stocker des données, généralement des informations sur des hôtes.
    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame(data)  # Convertit les données en DataFrame si ce n'est pas déjà un DataFrame.
    
    writer = pd.ExcelWriter(output_file, engine='xlsxwriter')  # Initialise un ExcelWriter pour écrire dans le fichier spécifié.
    data.to_excel(writer, index=False, header=False)  # Écrit les données dans le fichier sans index et sans en-tête.
    resize_table(writer, data)  # Appelle resize_table pour ajuster les largeurs de colonne.

def recon_excel(data, path):
    # Crée un fichier Excel à partir de données de reconnaissance structurées.
    donnees = []
    for host in data['scan']:
        # Extrait des informations de base et des détails des services pour chaque hôte scanné.
        ipv4 = data['scan'][host]['addresses']['ipv4']
        mac = data['scan'][host]['addresses']['mac']
        vendor = data['scan'][host]['vendor'][mac]
        ports = list(data['scan'][host]['tcp'].keys())
        cpe_list = [service['cpe'] for service in data['scan'][host]['tcp'].values()]
        products = [service['product'] for service in data['scan'][host]['tcp'].values()]
        versions = [service['version'] for service in data['scan'][host]['tcp'].values()]
        names = [service['name'] for service in data['scan'][host]['tcp'].values()]

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

    df = pd.DataFrame(donnees)  # Crée un DataFrame avec les données collectées.
    writer = pd.ExcelWriter(path, engine='xlsxwriter')
    df.to_excel(writer, index=False)  # Écrit le DataFrame dans un fichier Excel.
    resize_table(writer, df)  # Redimensionne les colonnes.

def exploit_Excel(Exploits, Shells, path, host):
    # Crée des fichiers Excel pour les exploits et les shells disponibles pour un hôte donné.
    if not os.path.exists(path + f"/{host}"):
        os.makedirs(path + f"/{host}")  # Crée un dossier pour l'hôte si ce n'est pas déjà fait.

    if Exploits:
        pathexploit = path + f"/{host}/exploit.xlsx"
        df_exploit = pd.DataFrame(Exploits)
        writer_exploit = pd.ExcelWriter(pathexploit, engine='xlsxwriter')
        df_exploit.to_excel(writer_exploit, index=False)
        resize_table(writer_exploit, df_exploit)  # Crée et redimensionne le fichier pour les exploits.

    if Shells:
        pathshell = path + f"/{host}/shell.xlsx"
        df_shell = pd.DataFrame(Shells)
        writer_shell = pd.ExcelWriter(pathshell, engine='xlsxwriter')
        df_shell.to_excel(writer_shell, index=False)
        resize_table(writer_shell, df_shell)  # Crée et redimensionne le fichier pour les shells.

def vuln_Excel(report, path, host):
    # Crée un fichier Excel pour les vulnérabilités rapportées d'un hôte.
    df = pd.DataFrame(report)
    path = f"{path}/{host}.xlsx"
    writer = pd.ExcelWriter(path, engine='xlsxwriter')
    df.to_excel(writer, index=False)
    resize_table(writer, df)  # Crée et redimensionne le fichier pour les rapports de vulnérabilité.

def remed_Excel(remediation, path, host):
    # Crée un fichier Excel pour les mesures de remédiation pour un hôte.
    df = pd.DataFrame(remediation)
    path = f"{path}/{host}.xlsx"
    writer = pd.ExcelWriter(path, engine='xlsxwriter')
    df.to_excel(writer, index=False)
    resize_table(writer, df)  # Crée et redimensionne le fichier pour les mesures de remédiation.
