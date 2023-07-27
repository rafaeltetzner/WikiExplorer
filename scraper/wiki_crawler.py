from scraper.wiki_scraper import WikiScraper
from collections import defaultdict
from urllib.parse import urljoin
from urllib.parse import urlparse
from urllib.parse import quote
from queue import Queue
import time


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
        id = self.get_id(url)
        children_as_ids = [self.get_id(child) for child in children]
        self.id_children[id] = children_as_ids

    def save(self, childrenfile, idfile):
        if self.lastsave >= len(self.id_children):
            return
        with open(childrenfile, 'ab+') as f:
            for id, children in list(self.id_children.items())[self.lastsave:]:
                num_children = len(children)
                row = id.to_bytes(4, byteorder='little') + num_children.to_bytes(4, byteorder='little')
                for child in children:
                    row += child.to_bytes(4, byteorder='little')
                f.write(row)
        with open(idfile, 'ab+') as f:
            for url, id in list(self.url_id.items())[self.lastsave:]:
                url_bytes = quote(url).encode('ascii')
                id_bytes = id.to_bytes(4, byteorder='little')
                row = id_bytes + url_bytes + b'\x00'
                f.write(row)
        self.lastsave = len(self.id_children)

class WikiCrawler:
    def __init__(self):
        self.scraper = WikiScraper()
        self.url_manager = URLManager()
        self.queue = Queue()
        self.starting_url = ""
    
    def crawl(self, url):
        html = self.scraper.fetch(urljoin(self.starting_url, url))
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

    def run(self, start_url, filenames, save_every=10, check=10):
        self.starting_url = start_url
        processed_count = 0
        last_discovered_count = 0
        last_time = time.time()
        max_children_len = 0
        max_children_father = None

        childrenfile, idfile = filenames
        self.queue.put(urlparse(start_url).path)
        while not self.queue.empty():
            url = self.queue.get()
            self.process_url(url)
            processed_count += 1

            if processed_count % save_every == 0:
                self.url_manager.save(childrenfile, idfile)

            children = self.url_manager.id_children.get(self.url_manager.get_id(url), [])
            num_children = len(children)
            if num_children > max_children_len:
                max_children_len = num_children
                max_children_father = urlparse(url).path
            if processed_count % check == 0:
                current_time = time.time()
                elapsed_time = current_time - last_time
                discovered_count = len(self.url_manager.url_id)
                process_rate = check / elapsed_time
                discover_rate = (discovered_count - last_discovered_count) / elapsed_time
                last_time = current_time
                last_discovered_count = discovered_count

                print(f"Processed {processed_count} URLs | Discovered: {discovered_count} "
                      f"| Process Rate: {process_rate:.2f}/s | Discover Rate: {discover_rate:.2f}/s "
                      f"| Len: {max_children_len} | Father: {max_children_father}")
        self.url_manager.save(childrenfile, idfile)