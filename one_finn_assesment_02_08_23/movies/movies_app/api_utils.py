import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import os
from dotenv import load_dotenv
import json
load_dotenv()

def get_movies_from_api():
    session = requests.Session()
    retries  = Retry(total=5, backoff_factor=2.0, status_forcelist=[500, 502, 503, 504])
    session.mount('http://', HTTPAdapter(max_retries=retries))
    
    url = "https://demo.credy.in/api/v1/maya/movies/"
    username = os.getenv("USERNAME1")
    password = os.getenv('PASSWORD')
    response = session.get(url, auth=(username, password))
    
    if response.status_code == 200:
        content = response.content.decode('utf-8')
        data = json.loads(content)
        movies = data
        return movies
    return []


if __name__ == "__main__":
    movies = get_movies_from_api()