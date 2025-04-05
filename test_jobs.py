import requests
import json

# URL do endpoint da sua aplicação Flask
url = "http://localhost:5000/jobs"

# Dados para enviar no corpo da requisição POST
data = {
    "search_term": "Developer",
    "google_search_term": "Developer",
    "location": "New York",
    "site_name": ["linkedin", "google", "indeed"],
    "results_wanted": 40,
    "is_remote": False,
    # "hours_old": 72,
    "linkedin_fetch_description": False,  # arrumar dps
}

# Cabeçalhos da requisição
headers = {
    "Content-Type": "application/json",
}

# Envia a requisição POST para o endpoint
response = requests.post(url, headers=headers, data=json.dumps(data))

# Verifica se a resposta foi bem-sucedida (status code 200)
if response.status_code == 200:
    print("Requisição bem-sucedida!")
    # Imprime o JSON de resposta
    print(json.dumps(response.json(), indent=4))
else:
    print(f"Falha na requisição. Status code: {response.status_code}")
    print(response.text)
