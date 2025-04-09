import requests
import json

url = "http://localhost:5000/jobs"

data = {
    "search_term": "Developer",
    "google_search_term": "Developer",
    "location": "New York",
    "site_name": ["linkedin", "google", "indeed"],
    "results_wanted": 40,
    "is_remote": False,
    "linkedin_fetch_description": True,
}

headers = {
    "Content-Type": "application/json",
}

response = requests.post(url, headers=headers, data=json.dumps(data))

if response.status_code == 200:
    print("Requisição bem-sucedida!")
    print(json.dumps(response.json(), indent=4))
else:
    print(f"Falha na requisição. Status code: {response.status_code}")
    print(response.text)
