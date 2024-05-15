import requests
import json
import sys
sys.path.append('./Utiles')
from utiles import *

def api_rest(api_key, url, path, host):
    if not requests.get(url, headers = api_key):
        print(f"Échec de la requête. Code d'erreur : {requests.get(url, headers = api_key).status_code}")
        exit()

    response = requests.get(url, headers = api_key)  

    if response.status_code == 200:
        path = f"{path}/{host}.json"
        with open(path, "w") as f:
            f.write(response.text)

        with open(path, "r") as f:
            data = json.load(f)
        with open(path, "w") as f:
            json.dump(data, f, indent=4)

        return data

    else:
        print(f"Échec de la requête. Code d'erreur : {response.status_code}")
        exit()


def vuln_filter(data, service):
    vulnerabilities = []
    report = []
    remediation = []
    graph = []
    high = 0
    low = 0
    medium = 0
    print(f"searching for {service}")

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
                print(f"Erreur: Le champ 'value' n'existe pas dans {desc}")
            if desc["lang"] == "en":
                descriptions.append(desc["value"])
        i = 1
        if i :
            if "cvssMetricV31" in vulnerability["cve"]["metrics"] :
                cvssData = vulnerability["cve"]["metrics"]["cvssMetricV31"][0]["cvssData"]
                attack_vector = cvssData["attackVector"]
                base_score = cvssData["baseScore"]
                conf_impact = cvssData["confidentialityImpact"]
                int_impact = cvssData["integrityImpact"]
                av_impact = cvssData["availabilityImpact"]
                i = 0

            elif "cvssMetricV30" in vulnerability["cve"]["metrics"] :
                cvssData = vulnerability["cve"]["metrics"]["cvssMetricV30"][0]["cvssData"]
                attack_vector = cvssData["attackVector"]
                base_score = cvssData["baseScore"]
                conf_impact = cvssData["confidentialityImpact"]
                int_impact = cvssData["integrityImpact"]
                av_impact = cvssData["availabilityImpact"]
                i = 0

            elif "cvssMetricV2" in vulnerability["cve"]["metrics"] :
                cvssData = vulnerability["cve"]["metrics"]["cvssMetricV2"][0]["cvssData"]
                attack_vector = cvssData["accessVector"]
                base_score = cvssData["baseScore"]
                conf_impact = cvssData["confidentialityImpact"]
                int_impact = cvssData["integrityImpact"]
                av_impact = cvssData["availabilityImpact"]
                i = 0
            
            else:
                print("Erreur: cvssMetric not found")
                i = 0
            if "references" not in vulnerability["cve"]:
                print(f'pas de reference de remediations pour {cve_id}')
            else : 
                remed_url = []
                remed_tag = []
                for reference in vulnerability["cve"]["references"]:
                    if reference['url']:
                        remed_url.append(reference['url'])
                    if "tag" in reference:
                        for tag in vulnerability["cve"]["references"]["tag"]:
                            remed_tag.append(tag)
        
        if base_score >= 7:
            color = "\033[91m" 
            high += 1 
        elif base_score >= 4:
            color = "\033[93m" 
            medium += 1
        else:
            color = "\033[92m" 
            low += 1

        vulnerabilities.append({
            "cve_id": cve_id,
            "attack_vector": attack_vector,
            "base_score": base_score,
            "published": published,
            "color": color,
            "confidentiality": conf_impact,
            "integrity": int_impact,
            "availability": av_impact,
            "descriptions": descriptions
        })
        report.append({
            "cve_id": cve_id,
            "service": service,
            "attack_vector": attack_vector,
            "base_score": base_score,
            "confidentiality": conf_impact,
            "integrity": int_impact,
            "availability": av_impact,
            "descriptions": descriptions 
        })

        remediation.append({
            "cve_id": cve_id,
            "Remédiation URL": remed_url,
            "tag": remed_tag
        })

    graph.append({
        "HIGH":high,
        "MEDIUM":medium,
        "LOW":low
    })
    return vulnerabilities, report, remediation, graph

def vuln_display(vulnerabilities):
    for vuln in vulnerabilities:
        print(f"{vuln['color']}CVE ID: {vuln['cve_id']}\033[0m  C = {vuln['confidentiality']}  |  I = {vuln['integrity']}  |  A = {vuln['availability']}")
        print(f"Published: {vuln['published']}")
        print("Descriptions:")

        for desc in vuln["descriptions"]:
            print(f"- {desc}")

        print(f"Attack Vector: {vuln['attack_vector']}")
        print(f"Base Score: {vuln['color']}{vuln['base_score']}\033[0m")
        print("______________________________________________________________________________________________________________________________________________")


def Vuln_search(services, api_key, path, host):
    vulnerabilities = []
    report = []
    remediation = []
    for service in services:
        url = f'https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch={service}'
        data = api_rest(api_key, url, path, host)
        vulnerabilities, report, remediation, graph = vuln_filter(data, service)
    
    return vulnerabilities, report, remediation, graph