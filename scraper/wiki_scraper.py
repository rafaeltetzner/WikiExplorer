import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, unquote

class WikiScraper():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}


    def __init__(self):
        self.session = requests.Session()
        self.session.headers = self.headers
        self.connection_pool = requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100)
        self.session.mount('http://', self.connection_pool)
        self.session.mount('https://', self.connection_pool)

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
        content_div = soup.find('div', class_='mw-parser-output')
        if not content_div:
            return None
        
        links = set()
        for link in soup.find_all('a'):
            href = link.get('href')
            if href:
                href = unquote(link.get('href'))
                if href.startswith('/wiki/') and not any(symbol in href for symbol in ['#', '?', '@', '&', '.']):
                    full_link = urljoin(url, href)
                    links.add(full_link)

        return {"links": links}