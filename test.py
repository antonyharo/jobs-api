import csv
from jobspy import scrape_jobs

jobs = scrape_jobs(
    site_name=[
        # "indeed",
        "linkedin",
        # "glassdoor",
        # "google",
    ],
    search_term="Analista de Redes",
    google_search_term="Analista de Redes",
    location="São Paulo",
    results_wanted=50,
    hours_old=72,
    country_indeed="USA",
    linkedin_fetch_description=False # gets more info such as description, direct job url (slower)
    # proxies=["208.195.175.46:65095", "208.195.175.45:65095", "localhost"],
)
print(f"Found {len(jobs)} jobs")
print(jobs.head())
jobs.to_csv(
    "jobs.csv", quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False
)  # to_excel
