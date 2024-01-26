import json, requests
import filterJSON

url = f'https://services.nvd.nist.gov/rest/json/cves/2.0'
api_key = {'apiKey': '97410594-f2e3-4e00-a63e-1e6eb5dcef38'}
params = {
    'cpeName': ''
}

if not requests.get(url, headers = api_key):
    print(f"Échec de la requête. Code d'erreur : {requests.get(url, headers = api_key).status_code}")
    exit()

response = requests.get(url, headers = api_key)  

if response.status_code == 200:

    with open(r"C:\Users\y.kraouch\Desktop\Projects\CVE-ALERTS\test.json", "w") as f:
        f.write(response.text)

    with open(r"C:\Users\y.kraouch\Desktop\Projects\CVE-ALERTS\test.json", "r") as f:
        data = json.load(f)

else:
    print(f"Échec de la requête. Code d'erreur : {response.status_code}")
    exit()

vulnerabilities = []

if "vulnerabilities" not in data:
    print("Erreur: Le champ 'vulnerabilities' n'existe pas")
    exit()

for vulnerability in data["vulnerabilities"]:
    cve_id = vulnerability["cve"]["id"]
    published = vulnerability["cve"]["published"]
    descriptions = []

    if "cve" not in vulnerability or "descriptions" not in vulnerability["cve"]:
        print("Erreur: Le champ 'cve' ou 'descriptions' n'existe pas")
        exit()

    for desc in vulnerability["cve"]["descriptions"]:
        if "value" not in desc :
            print(f"Erreur: Le champ 'value' n'existe pas dans {vulnerability["cve"]["id"]}")
        if desc["lang"] == "en":
            descriptions.append(desc["value"])

    attack_vector = vulnerability["cve"]["metrics"]["cvssMetricV31"][0]["cvssData"]["attackVector"]
    base_score = vulnerability["cve"]["metrics"]["cvssMetricV31"][0]["cvssData"]["baseScore"]
    
    if base_score >= 7:
        color = "\033[91m" 
    elif base_score >= 4:
        color = "\033[93m" 
    else:
        color = "\033[92m" 
    
    vulnerabilities.append({
        "cve_id": cve_id,
        "descriptions": descriptions,
        "attack_vector": attack_vector,
        "base_score": base_score,
        "published": published,
        "color": color
    })


for vuln in vulnerabilities:
    print(f"{vuln['color']}CVE ID: {vuln['cve_id']}\033[0m")
    print(f"Published: {vuln['published']}")
    print("English Descriptions:")

    for desc in vuln["descriptions"]:
        print(f"- {desc}")

    print(f"Attack Vector: {vuln['attack_vector']}")
    print(f"Base Score: {vuln['color']}{vuln['base_score']}\033[0m")
    print("_________________________________________________________________________________________________________________________________________________________________________________________________________________________")
