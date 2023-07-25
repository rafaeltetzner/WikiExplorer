import requests
from bs4 import BeautifulSoup
from scraper.log_level import LOG_LEVEL
from urllib.parse import urljoin

class WikiScraper():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = self.headers

    def fetch(self, url):
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            return None
    
    def parse(self, html, url):
        if not html:
            return None
        
        soup = BeautifulSoup(html, 'lxml')
        #h1 = soup.select_one('h1')
        #title = None
        #if h1:
        #   title = h1.text.strip()

        links = set()
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and href.startswith('/wiki/'):
                full_link = urljoin(url, href)
                links.add(full_link)

        return {"links": links}