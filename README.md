# Auto-Diag

Bienvenue dans **Auto-Diag**, un outil de diagnostic automatique de réseau. Cet outil utilise diverses techniques pour scanner et analyser les hôtes sur un réseau, détecter les services actifs, effectuer des scans de vulnérabilité et lancer des attaques de bruteforce sur les services identifiés.

---

## Prérequis

Assurez-vous d'avoir les bibliothèques Python suivantes installées :

```bash
pip install nmap pyfiglet paramiko pycvesearch docx 
```

```bash
pip install --user python-netdiscover pymetasploit3
```

---

## Utilisation

1. **Cloner le projet**
   ```bash
   git clone https://github.com/votre-utilisateur/Auto-Diag.git
   cd Auto-Diag
   ```

2. **Exécution**
   ```bash
   python auto_diag.py
   ```

---

## Fonctionnalités

### Scan de réseau

- L'outil commence par effectuer un scan de réseau pour découvrir les hôtes actifs.
- Vous pouvez spécifier une adresse IP pour le scan ou appuyer sur Entrée pour utiliser l'adresse IP par défaut de la machine.

### Scan Nmap

- Un scan Nmap détaillé est effectué sur chaque hôte découvert, en recherchant les services actifs et les vulnérabilités.
- Les résultats du scan sont enregistrés au format CSV et JSON.

### Recherche CVE

- Vous pouvez effectuer une recherche CVE en fournissant un code CVE spécifique.

### Brute-force

- L'outil propose une fonction de bruteforce pour les services SSH et FTP.
- Vous devez spécifier un nom d'utilisateur et un fichier de mots de passe.

### Rapports

- Les résultats de chaque analyse sont affichés en temps réel.
- Un rapport Word est généré à la fin, récapitulant les résultats du scan pour chaque hôte.

---

## Exemple d'utilisation

1. **Scan de réseau**
   - Appuyez sur Entrée pour utiliser l'adresse IP par défaut.
   - Les hôtes actifs seront répertoriés.

2. **Scan Nmap**
   - Un scan détaillé sera effectué sur chaque hôte.
   - Les services ouverts, les versions et les scripts associés seront affichés.

3. **Brute-force**
   - Choisissez un type de service à attaquer (SSH ou FTP).
   - Fournissez un nom d'utilisateur et le chemin d'un fichier de mots de passe.

4. **Rapport**
   - Un rapport Word sera généré à la fin de l'exécution, résumant les résultats du scan.

---

## Contributions

Les contributions sont les bienvenues ! Si vous avez des idées d'amélioration ou des correctifs, n'hésitez pas à ouvrir une issue ou à créer une pull request.

---

## Avertissement

L'utilisation de cet outil est destinée uniquement à des fins éducatives et de test sur des réseaux dont vous avez l'autorisation d'accéder. L'auteur n'est pas responsable de toute utilisation abusive ou illégale de cet outil.

--- 

*Auto-Diag* est développé par [Yassir / victor / guigui].
