from scraper.wiki_crawler import WikiCrawler

if __name__ == '__main__':
    start_url = 'https://jojo.fandom.com/wiki/Main_Page'
    output_file = 'data/jojo.csv'
    crawler = WikiCrawler()
    crawler.run(start_url)