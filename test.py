import csv
from jobspy import scrape_jobs

jobs = scrape_jobs(
    site_name=["linkedin", "indeed", "glassdoor", "google"],
    search_term="Analista de Redes",
    google_search_term="Vagas de Analista de Redes próximas à São Paulo desde ontem",
    location="São Paulo",
    results_wanted=20,
    hours_old=72,
    linkedin_fetch_description=False,
)

print(f"Found {len(jobs)} jobs")
print(jobs.head())

jobs_dict = jobs.to_dict(orient="records")

for i, job in enumerate(jobs_dict):
    print(i)