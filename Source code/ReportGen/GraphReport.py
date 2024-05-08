import matplotlib.pyplot as plt
from Utiles.utiles import print_green  # Suppose importation d'une fonction utilitaire pour afficher des textes en vert.

def graph_exploit(exploit, shell, host):
    # Génère un graphique à barres pour les données relatives aux exploits et aux shells.
    categories = ['Exploit', 'Shell']  # Catégories pour les barres du graphique.
    values = [exploit, shell]  # Valeurs numériques pour chaque catégorie.
    colors = ['red' if value <= 4 else 'green' for value in values]  # Attribue une couleur en fonction de la valeur.
    plt.bar(categories, values, color=colors)  # Crée un graphique à barres avec les couleurs conditionnelles.
    plt.xlabel('Categories')  # Définit le label de l'axe des x.
    plt.ylabel('Values')  # Définit le label de l'axe des y.
    plt.title("Rapport Exploits/Shells     Source'ExploitDB'")  # Ajoute un titre au graphique.
    plt.savefig(f'./Doc/Report/PNG/Exploit/{host}.png')  # Sauvegarde le graphique en fichier PNG dans un répertoire spécifié.
    plt.close()  # Ferme l'objet de graphique pour libérer la mémoire.
    print_green(f'exploit graph report for {host} is created')  # Affiche un message de confirmation en vert.

def graph_cve(data, host):
    # Génère un graphique à barres pour les niveaux de risque des CVE (Common Vulnerabilities and Exposures).
    for item in data:
        HIGH = item["HIGH"]  # Extrait la valeur pour les vulnérabilités de niveau élevé.
        MEDIUM = item["MEDIUM"]  # Extrait la valeur pour les vulnérabilités de niveau moyen.
        LOW = item["LOW"]  # Extrait la valeur pour les vulnérabilités de niveau bas.
    plt.bar('HIGH', HIGH, color='red')  # Crée une barre pour les vulnérabilités élevées.
    plt.bar('MEDIUM', MEDIUM, color='orange')  # Crée une barre pour les vulnérabilités moyennes.
    plt.bar('LOW', LOW, color='green')  # Crée une barre pour les vulnérabilités basses.
    plt.xlabel('Categories')  # Définit le label de l'axe des x.
    plt.ylabel('Values')  # Définit le label de l'axe des y.
    plt.title("Rapport CVE     Source'NIST API'")  # Ajoute un titre au graphique.
    plt.savefig(f'./Doc/Report/PNG/Vulns/{host}.png')  # Sauvegarde le graphique en fichier PNG dans un répertoire spécifié.
    plt.close()  # Ferme l'objet de graphique pour libérer la mémoire.
    print_green(f'CVE graph report for {host} is created')  # Affiche un message de confirmation en vert.
