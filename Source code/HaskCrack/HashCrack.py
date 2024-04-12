import os
import hashlib

def crack_hash(wordlist_location, hash_input, algorithm):
    with open(wordlist_location, 'r', encoding='latin-1') as file:
        for line in file.readlines():
            hash_ob = hashlib.new(algorithm)
            hash_ob.update(line.strip().encode())
            hashed_pass = hash_ob.hexdigest()
            if hashed_pass == hash_input:
                print('Found cleartext password for algorithm', algorithm + ':', line.strip())
                return True
    return False

def main():
    hash_input = input('Saisir le hash à décrypter : ')
    algorithm = input('Entrer l'algorithme de hachage (Appuyer sur ENTRER par défaut - md5): ')

    if not algorithm:
        algorithm = 'md5'  # Utiliser md5 par défaut si aucun algorithme n'est spécifié

    wordlist_location = input('Veuillez entrer le chemin de la wordlist (Appuyer sur ENTRER par défaut - rockyou.txt): ')

    if not wordlist_location:
        wordlist_location = '/usr/share/wordlists/rockyou.txt'

    if not os.path.isfile(wordlist_location):
        print('Fichier wordlist non trouvé.')
        return

    algorithms = hashlib.algorithms_available
    print(algorithms)
    #found = crack_hash(wordlist_location, hash_input, algorithm)

    if not found:
        print('Mots de passe non trouvé dans la wordlist.')

if __name__ == "__main__":
    main()
