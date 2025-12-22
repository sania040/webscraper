# 1L Summer Law Job Scraper (Georgia)

## Overview
This project scrapes public listings for 1L Summer Associate/Law jobs in Georgia, USA, stores them in a SQLite database, and serves them via a REST API.

## Tech Stack
* **Language:** Python 3.10+
* **Scraping:** ScrapeGraphAI (Official SDK)
* **Database:** SQLite (via SQLAlchemy)
* **API:** FastAPI

## Setup & Usage

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Environment Setup:**
    Create a `.env` file and add your ScrapeGraphAI API key:
    ```env
    SCRAPEGRAPH_API_KEY=sgai-your-key-here
    ```

3.  **Run the Scraper:**
    ```bash
    python scraper.py
    ```
    *Note:* This fetches data from LinkedIn and populates `jobs.db`.

4.  **Run the API:**
    ```bash
    uvicorn main:app --reload
    ```
    Access the Swagger UI at: `http://127.0.0.1:8000/docs`

## Known Limitations
* **LinkedIn Anti-Scraping:** The scraper uses a public, login-free method. Occasionally, LinkedIn masks data (appearing as `****`) to prevent scraping.
* **Mitigation:** In a production environment, this would be solved by using residential proxies or a specialized scraping service (e.g., BrightData), but I adhered to the "no login/free" constraints for this assessment.

## API Endpoints
* `GET /jobs`: Fetch jobs with pagination support.
    * Query Params: `skip`, `limit`, `city` (e.g., "Atlanta"), `is_1l`.