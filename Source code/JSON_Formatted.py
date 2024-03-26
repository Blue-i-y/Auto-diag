import json


chemin_fichier_json = "10_0_2_15.json"

with open(chemin_fichier_json, "r") as f:
    contenu_json = f.read()

donnees_json = json.loads(contenu_json)
nouveau_chemin_fichier_json = "test.json"

with open(nouveau_chemin_fichier_json, "w") as f:
    json.dump(donnees_json, f, indent=4)

print("Le fichier JSON a été reformaté avec succès.")
