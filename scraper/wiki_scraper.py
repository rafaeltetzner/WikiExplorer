import requests
from bs4 import BeautifulSoup
import logging
from scraper.log_level import LOG_LEVEL
from urllib.parse import urljoin

class WikiScraper():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = self.headers
        self.logger = self._setup_logger()

    def fetch(self, url):
        try:
            self.logger.info(f'Fetching url: {url}')
            response = self.session.get(url)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            self.logger.error(f'Error fetching wiki page: {e}')
            return None
    
    def parse(self, html, base_url):
        if not html:
            self.logger.warning(f'Null HTML provided to parser')
            return None
        
        soup = BeautifulSoup(html, 'lxml')
        h1 = soup.select_one('h1')
        title = None
        if not h1:
            self.logger.error(f'Error parsing title from html with base {base_url}, probably no title')
        else:
            title = h1.text.strip()

        links = set()
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and href.startswith('/wiki/'):
                full_link = urljoin(base_url, href)
                links.add(full_link)

        self.logger.info(f'Parsed {len(links)} links from the page')

        return {"title": title, "links": links}

    def _setup_logger(self):
        file_handler = logging.FileHandler('scraper.log')
        file_handler.setLevel(LOG_LEVEL)

        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)

        logger = logging.getLogger('scraper')
        logger.setLevel(LOG_LEVEL)
        logger.addHandler(file_handler)

        return logger