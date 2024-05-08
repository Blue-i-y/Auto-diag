import hashlib

def detect_algorithm(hash_input):
    # Récupère une liste de tous les algorithmes de hashage disponibles dans la bibliothèque hashlib.
    algorithms = hashlib.algorithms_available
    # Itère sur chaque algorithme disponible.
    for algorithm in algorithms:
        hash_ob = hashlib.new(algorithm)  # Crée un nouvel objet de hash pour l'algorithme en cours.
        hash_ob.update(b'test')  # Met à jour l'objet de hash avec une valeur de test (ici, le mot 'test').
        test_hash = hash_ob.hexdigest()  # Calcule le hash de la valeur de test.
        if test_hash == hash_input:  # Compare le hash calculé avec le hash en entrée.
            return algorithm  # Retourne le nom de l'algorithme si le hash correspond.
    return None  # Retourne None si aucun algorithme correspondant n'est trouvé.

# Exemple d'utilisation de la fonction
hash_input = input('Enter hash to be cracked: ')  # Demande à l'utilisateur d'entrer le hash à identifier.
detected_algorithm = detect_algorithm(hash_input)  # Appelle la fonction pour détecter l'algorithme.

if detected_algorithm:
    print('Detected algorithm:', detected_algorithm)  # Affiche l'algorithme détecté si trouvé.
else:
    print('Unable to detect algorithm.')  # Informe l'utilisateur si aucun algorithme n'est détecté.
