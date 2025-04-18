import requests
import json

# URL do seu servidor Flask
url = "http://localhost:5000/jobs"  # Altere se estiver em outro host/porta

# Payload de exemplo para busca de vagas
payload = {
    "search_term": "data scientist",
    "location": "São Paulo",
    "results_wanted": 10,
    "offset": 0,
    "is_remote": True,
    "job_type": "fulltime",
}

# Cabeçalhos HTTP
headers = {"Content-Type": "application/json"}

# Envia a requisição POST
response = requests.post(url, headers=headers, data=json.dumps(payload))

# Trata a resposta
if response.status_code == 200:
    data = response.json()
    print(f"\n✅ Vagas encontradas: {len(data.get('jobs', []))}\n")
    for idx, job in enumerate(data["jobs"], start=1):
        print(
            f"{idx}. {job.get('title')} - {job.get('company_name')} ({job.get('location')})"
        )
        print(f"   Publicado em: {job.get('date_posted')}")
        print(f"   Link: {job.get('job_url')}")
        print("-" * 60)
else:
    print(f"❌ Erro na requisição: {response.status_code}")
    print(response.text)
