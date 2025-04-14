from flask import Flask, jsonify, request
from flask_cors import CORS
from jobspy import scrape_jobs
import logging
import requests
import math
from datetime import date

app = Flask(__name__)
CORS(app)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


@app.route("/")
def home():
    return jsonify({"message": "Hello World!"})


def renew_tor_ip_with_socks():
    """Configura e retorna uma sessão do requests via Tor."""
    session = requests.Session()
    session.proxies = {
        "http": "socks5://127.0.0.1:9050",
        "https": "socks5://127.0.0.1:9050",
    }
    try:
        ip = session.get("https://api.ipify.org?format=json", timeout=5).json()["ip"]
        logging.info(f"Tor IP renewed successfully: {ip}")
        return session
    except requests.RequestException as e:
        logging.error(f"Error renewing Tor IP: {e}")
        return None


def get_real_ip(session):
    """Obtém o IP real da sessão fornecida."""
    try:
        return session.get("https://api.ipify.org?format=json", timeout=5).json()["ip"]
    except requests.RequestException as e:
        logging.error(f"Error getting IP: {e}")
        return None


def format_proxies(proxies):
    """Formata proxies para o formato correto."""
    return [
        f"http://{proxy}" if not proxy.startswith(("http://", "https://")) else proxy
        for proxy in (proxies or [])
    ]


def configure_proxy(use_tor, proxies):
    """Configura e retorna proxies formatados ou sessão Tor."""
    formatted_proxies = format_proxies(proxies) if proxies else None
    tor_session = renew_tor_ip_with_socks() if use_tor else None

    if use_tor and tor_session:
        return {
            "http": "socks5://127.0.0.1:9050",
            "https": "socks5://127.0.0.1:9050",
        }, tor_session

    if formatted_proxies:
        return {
            proto: proxy for proxy in formatted_proxies for proto in ["http", "https"]
        }, None

    return None, None


def format_jobs(jobs):
    """
    Limpa e formata uma lista de dicionários de jobs:
    - Converte NaN para None.
    - Transforma datetime.date em strings no formato DD/MM/AAAA para a chave 'date_posted'.
    """

    def clean_data(data):
        if isinstance(data, dict):
            return {key: clean_data(value) for key, value in data.items()}
        if isinstance(data, list):
            return [clean_data(item) for item in data]
        if isinstance(data, float) and math.isnan(data):
            return None
        return data

    jobs = clean_data(jobs)

    for job in jobs:
        dp = job.get("date_posted")
        if isinstance(dp, date):
            job["date_posted"] = dp.strftime("%d/%m/%Y")

    return jobs


@app.route("/jobs", methods=["POST"])
def search_jobs():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        required_params = ["search_term", "location"]
        if not all(param in data for param in required_params):
            return (
                jsonify(
                    {"error": "Missing required parameters: search_term and location"}
                ),
                400,
            )

        search_term, location = data["search_term"], data["location"]
        site_name = ["linkedin", "indeed", "glassdoor"]
        proxies = data.get("proxies")
        use_tor = data.get("use_tor", False)

        proxy_dict, tor_session = configure_proxy(use_tor, proxies)
        session = tor_session or requests.Session()
        ip_address = get_real_ip(session)
        logging.info(f"IP used for the search: {ip_address}")

        jobs = scrape_jobs(
            site_name=site_name if isinstance(site_name, list) else [site_name],
            search_term=search_term,
            google_search_term=data.get(
                "google_search_term",
                f"{search_term} jobs near {location} since yesterday",
            ),
            location=location,
            job_type=data.get("job_type"),
            is_remote=data.get("is_remote", False),
            results_wanted=data.get("results_wanted", 20),
            offset=data.get("offset", 0),
            hours_old=data.get("hours_old", 72),
            verbose=2,
            linkedin_fetch_description=True,
            proxies=proxy_dict,
            ca_cert=data.get("ca_cert"),
            session=tor_session,
        )

        formated_jobs = format_jobs(jobs.to_dict(orient="records"))
        response_data = {"jobs": formated_jobs}

        logging.info(f"Found {len(jobs)} jobs")

        if ip_address:
            response_data["ip_address"] = ip_address

        return jsonify(response_data), 200
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
