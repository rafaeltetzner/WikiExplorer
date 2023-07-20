import csv
import os
import numpy as np
import logging
from scraper.log_level import LOG_LEVEL
from scraper.wiki_scraper import WikiScraper

class WikiCrawler():
    def __init__(self):
        self.url_idxs = {} # hash map of url to its idx in children list
        self.url_children = [] # list of tuples (url, children)
        self.scraper = WikiScraper()
        self.current_idx = 0 # current idx of url being processed (idx < current_idx = already visited)
        self.last_saved = -1

        self.logger = self._setup_logger()

    def crawl(self, url):
        self.logger.debug(f'Crawling url: {url}')
        html = self.scraper.fetch(url)
        result = self.scraper.parse(html, url)
        if result:
            return list(result['links'])
        self.logger.warning(f'url returned no children: {url}')
        return []
        
    def run(self, start_url, filename, save_every=10):
        self.push_url(start_url)

        while self.current_idx < len(self.url_children):
            url, _ = self.url_children[self.current_idx]
            children = self.crawl(url)

            for child in children:
                self.push_url(child)

            children_as_idxs = np.array([self.url_idxs[child] for child in children])
            self.url_children[self.current_idx] = (url, children_as_idxs)

            self.current_idx += 1
            if self.current_idx % save_every == 0:
                self.save_to_csv(filename)
                self.logger.debug(f"Updated CSV file at index {self.current_idx - 1}")

        self.save_to_csv(filename)

    def save_to_csv(self, filename):
        with open(filename, 'a+', newline='') as f:
            writer = csv.writer(f)
            if self.last_saved == -1:
                header = ['URL', 'CHILDREN']
                writer.writerow(header)
                self.last_saved += 1
            
            while self.last_saved < self.current_idx:
                url, children = self.url_children[self.last_saved]
                childrenStr = ','.join(map(str, children))
                writer.writerow([url, childrenStr])
                self.last_saved += 1

    def push_url(self, url):
        if url not in self.url_idxs:
            self.url_idxs[url] = len(self.url_children)
            self.url_children.append((url, []))
            self.logger.debug(f"Pushed URL to queue: {url}")

    def _setup_logger(self):
        logger = logging.getLogger('crawler')
        logger.setLevel(LOG_LEVEL)

        file_handler = logging.FileHandler('crawler.log')
        file_handler.setLevel(LOG_LEVEL)

        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

        return logger