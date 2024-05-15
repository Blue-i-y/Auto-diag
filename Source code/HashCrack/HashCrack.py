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
    hash_input = input('Enter hash to be cracked: ')
    algorithm = input('Enter hash algorithm  (press Enter for default - md5): ')

    if not algorithm:
        algorithm = 'md5'  # Utiliser md5 par défaut si aucun algorithme n'est spécifié

    wordlist_location = input('Enter wordlist file location (press Enter for default - rockyou.txt): ')

    if not wordlist_location:
        wordlist_location = '/usr/share/wordlists/rockyou.txt'

    if not os.path.isfile(wordlist_location):
        print('Wordlist file not found.')
        return

    algorithms = hashlib.algorithms_available
    print(algorithms)
    #found = crack_hash(wordlist_location, hash_input, algorithm)

    if not found:
        print('Password not found in the wordlist.')

if __name__ == "__main__":
    main()
