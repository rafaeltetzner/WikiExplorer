from scraper.wiki_scraper import WikiScraper
from collections import defaultdict
from queue import Queue

class URLManager:
    def __init__(self):
        self.url_id = defaultdict(lambda: len(self.url_id))
        self.id_children = {}

    def get_id(self, url):
        return self.url_id[url]

    def set_children(self, url, children):
        children_as_ids = [self.get_id(child) for child in children]
        self.id_children[self.get_id(url)] = children_as_ids

class WikiCrawler:
    def __init__(self):
        self.scraper = WikiScraper()
        self.url_manager = URLManager()
        self.queue = Queue()
        self.visited = set()
        self.counter = 0
    
    def crawl(self, url):
        html = self.scraper.fetch(url)
        data = self.scraper.parse(html, url)
        return data["links"] if data else []

    def process_url(self, url):
        children = self.crawl(url)
        self.url_manager.set_children(url, children)
        self.visited.add(url)
        for new in children - self.visited:
            self.queue.put(new)

    def run(self, start_url):
        self.queue.put(start_url)
        while not self.queue.empty():
            url = self.queue.get()
            self.process_url(url)