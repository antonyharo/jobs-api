from jobspy import scrape_jobs
from datetime import date

jobs = scrape_jobs(
    site_name=["linkedin", "indeed", "glassdoor"],
    search_term="Analista de Redes",
    google_search_term="Vagas de Analista de Redes próximas à São Paulo desde ontem",
    location="São Paulo",
    country_indeed="Brazil",
    results_wanted=20,
    hours_old=72,
    linkedin_fetch_description=False,
    verbose=2,
)

jobs_dict = jobs.to_dict(orient="records")
print(f"\n✅ Vagas encontradas: {len(jobs_dict)}\n")

for idx, job in enumerate(jobs_dict, start=1):
    title = job.get("title")
    company = job.get("company")
    location = job.get("location")
    link = job.get("job_url")
    posted = job.get("date_posted")

    if isinstance(posted, date):
        posted = posted.strftime("%d/%m/%Y")

    print(f"{idx}. {title} - {company} ({location})")
    print(f"   Publicado em: {posted}")
    print(f"   Link: {link}")
    print("-" * 60)
