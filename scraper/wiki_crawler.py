from scraper.wiki_scraper import WikiScraper
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Manager
from collections import defaultdict
from queue import Queue

class URLManager:
    def __init__(self):
        self.url_id = defaultdict(lambda: len(self.url_id))
        self.id_children = {}
        self.lastsave = 0

    def __contains__(self, url):
        return url in self.url_id
    
    def get_id(self, url):
        return self.url_id[url]

    def set_children(self, url, children):
        children_as_ids = [self.get_id(child) for child in children]
        self.id_children[self.get_id(url)] = children_as_ids
    
    def save(self, childrenfile, idfile):
        if self.lastsave >= len(self.id_children):
            return
        with open(childrenfile, 'w') as f:
            for id, children in list(self.id_children.items()):
                row = str(id) + ' ' + ' '.join(map(str, children)) + '\n'
                f.write(row)
        with open(idfile, 'w') as f:
            for url, id in list(self.url_id.items()):
                row = url + ' ' + str(id) + '\n'
                f.write(row) 
        
class WikiCrawler:
    def __init__(self):
        self.scraper = WikiScraper()
        self.url_manager = URLManager()
        self.queue = Queue()
        self.counter = 0
    
    def crawl(self, url):
        html = self.scraper.fetch(url)
        data = self.scraper.parse(html, url)
        return data["links"] if data else []
    
    def update_queue(self, children):
        for child in children:
            if child not in self.url_manager:
                self.queue.put(child)

    def process_url(self, url):
        children = self.crawl(url)
        self.update_queue(children)
        self.url_manager.set_children(url, children)

    def run(self, start_url, filenames, save_every=10):
        count = 0
        childrenfile, idfile = filenames
        self.queue.put(start_url)
        while not self.queue.empty():
            url = self.queue.get()
            self.process_url(url)
            count += 1
            if count % save_every == 0:
                self.url_manager.save(childrenfile, idfile)
            