from scraper.wiki_crawler import WikiCrawler

if __name__ == '__main__':
    start_url = 'https://jojo.fandom.com/wiki/Main_Page'

    output_childs = 'data/jojo.csv'
    output_ids = 'data/jojo_ids.csv'
    crawler = WikiCrawler()
    crawler.run(start_url, (output_childs, output_ids))