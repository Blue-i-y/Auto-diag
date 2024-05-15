import hashlib

def detect_algorithm(hash_input):
    algorithms = hashlib.algorithms_available
    for algorithm in algorithms:
        hash_ob = hashlib.new(algorithm)
        hash_ob.update(b'test') 
        test_hash = hash_ob.hexdigest()
        if test_hash == hash_input:
            return algorithm
    return None

# Exemple d'utilisation de la fonction
hash_input = input('Enter hash to be cracked: ')
detected_algorithm = detect_algorithm(hash_input)
if detected_algorithm:
    print('Detected algorithm:', detected_algorithm)
else:
    print('Unable to detect algorithm.')
