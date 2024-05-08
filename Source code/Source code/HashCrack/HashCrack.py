import os
import hashlib

def crack_hash(wordlist_location, hash_input, algorithm):
    # Ouvre le fichier de mots de passe à partir de l'emplacement spécifié.
    with open(wordlist_location, 'r', encoding='latin-1') as file:
        # Itère sur chaque ligne du fichier.
        for line in file.readlines():
            hash_ob = hashlib.new(algorithm)  # Crée un objet de hash pour l'algorithme spécifié.
            hash_ob.update(line.strip().encode())  # Met à jour l'objet hash avec le mot de passe nettoyé (sans espaces).
            hashed_pass = hash_ob.hexdigest()  # Calcule le hash hexadécimal.
            if hashed_pass == hash_input:  # Compare le hash calculé avec le hash en entrée.
                print('Found cleartext password for algorithm', algorithm + ':', line.strip())
                return True  # Retourne True si le mot de passe correspondant est trouvé.
    return False  # Retourne False si aucun mot de passe correspondant n'est trouvé dans le fichier.

def main():
    hash_input = input('Enter hash to be cracked: ')  # Demande à l'utilisateur d'entrer le hash à craquer.
    algorithm = input('Enter hash algorithm (press Enter for default - md5): ')  # Demande l'algorithme de hashage, avec md5 comme défaut.

    if not algorithm:
        algorithm = 'md5'  # Utilise md5 par défaut si aucun algorithme n'est spécifié.

    wordlist_location = input('Enter wordlist file location (press Enter for default - rockyou.txt): ')  # Demande l'emplacement du fichier de mots de passe.

    if not wordlist_location:
        wordlist_location = '/usr/share/wordlists/rockyou.txt'  # Utilise rockyou.txt par défaut si aucun emplacement n'est spécifié.

    if not os.path.isfile(wordlist_location):
        print('Wordlist file not found.')  # Vérifie si le fichier existe à l'emplacement spécifié.
        return

    algorithms = hashlib.algorithms_available  # Affiche les algorithmes de hashage disponibles.
    print(algorithms)
    found = crack_hash(wordlist_location, hash_input, algorithm)  # Appelle la fonction de craquage de hash.

    if not found:
        print('Password not found in the wordlist.')  # Informe l'utilisateur si le mot de passe n'est pas trouvé.

if __name__ == "__main__":
    main()  # Exécute la fonction principale si le script est exécuté en tant que programme principal.
