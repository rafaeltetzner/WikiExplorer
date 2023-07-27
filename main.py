from scraper.wiki_crawler import WikiCrawler

if __name__ == '__main__':
    start_url = 'https://jojo.fandom.com/wiki/Stand'

    output_childs = 'jojo_children.bin'
    output_ids = 'jojo_ids.bin'
    crawler = WikiCrawler()
    crawler.run(start_url, (output_childs, output_ids), save_every=100, check=10)