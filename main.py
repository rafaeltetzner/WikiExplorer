from scraper.wiki_crawler import WikiCrawler

if __name__ == '__main__':
    start_url = 'https://www.princesofdarknessmod.com/wiki/index.php/Main_Page'
    output_file = 'data/pod_child.csv'
    crawler = WikiCrawler()
    crawler.run(start_url, output_file)