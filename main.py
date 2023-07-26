from scraper.wiki_crawler import WikiCrawler

if __name__ == '__main__':
    start_url = 'https://deadmountdeathplay.fandom.com/wiki/Dead_Mount_Death_Play_Wiki'

    output_childs = 'data/dmdp_children.bin'
    output_ids = 'data/dmdp_ids.bin'
    crawler = WikiCrawler()
    crawler.run(start_url, (output_childs, output_ids), save_every=1000, check=10)