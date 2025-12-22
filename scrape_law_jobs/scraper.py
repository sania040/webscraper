import os
import json
from dotenv import load_dotenv
from scrapegraph_py import Client
from database import SessionLocal, Job, init_db

# Load the key from .env
load_dotenv()
API_KEY = os.getenv("SCRAPEGRAPH_API_KEY")

# Target URL (Georgia 1L Summer Associate Search)
TARGET_URL = "https://www.linkedin.com/jobs/search?keywords=1L+Summer+Associate&location=Georgia%2C+United+States"

def run_scraper():
    print(f"--- Starting Official ScrapeGraphAI Job on {TARGET_URL} ---")

    # Initialize the official client
    try:
        client = Client(api_key=API_KEY)
    except Exception as e:
        print(f"Error initializing client. Check your API Key format. Error: {e}")
        return

    # The Prompt
    prompt = """
    Extract all job listings from this page.
    Return a JSON object with a key 'jobs' containing a list of jobs.
    Each job must have:
    - title (text)
    - organization (text)
    - location (text)
    - description (summary)
    - url (link)
    - is_1l (boolean, true if '1L' is mentioned)
    """

    try:
        # Use the 'smartscraper' endpoint
        response = client.smartscraper(
            website_url=TARGET_URL,
            user_prompt=prompt
        )

        # Debug: Print raw response to see what we got
        print("Raw Response:", json.dumps(response, indent=2))
        
        # Save to DB
        save_to_db(response)
        
    except Exception as e:
        print(f"Error during scraping: {e}")

def save_to_db(data):
    session = SessionLocal()
    init_db() 
    
    # The official API usually returns the pure JSON result directly
    # We look for the list inside the 'result' or the direct dictionary
    jobs_list = []
    
    # Adjust parsing based on the response structure
    if isinstance(data, dict):
        if "jobs" in data:
            jobs_list = data["jobs"]
        elif "result" in data and isinstance(data["result"], dict) and "jobs" in data["result"]:
             jobs_list = data["result"]["jobs"]
        elif "result" in data:
             jobs_list = data["result"] # sometimes it just returns the list
    
    count = 0
    for item in jobs_list:
        if not isinstance(item, dict): continue
        
        existing = session.query(Job).filter(Job.url == item.get('url')).first()
        if not existing:
            job = Job(
                title=item.get('title', 'N/A'),
                organization=item.get('organization', 'N/A'),
                location=item.get('location', 'Georgia'),
                description=item.get('description', ''),
                url=item.get('url', ''),
                is_1l=item.get('is_1l', False)
            )
            session.add(job)
            count += 1
    
    session.commit()
    session.close()
    print(f"Successfully added {count} new jobs to the database.")

if __name__ == "__main__":
    run_scraper()