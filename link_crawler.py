from lxml import html
import requests
import time
from link_model import LinkModel
from concurrent.futures import ThreadPoolExecutor


class LinkCrawler:

    def __init__(self, starting_url, depth = 10, breadth = 10):
        self.starting_url = starting_url
        self.depth = depth
        self.breadth = breadth
        self.currentDepth = 0
        self.depthLinks = []
        self.linkList = []

    def startCrawl(self, n):
        print(f'Starting thread {n}')
        link = self.get_content_from_link(self.starting_url, n)
        self.linkList.append(link)
        self.depthLinks.append(link.links)
        
        while self.currentDepth < self.depth:
            currentLinks = []
            for relatedLink in self.depthLinks[self.currentDepth]:
                new_link = self.get_content_from_link(relatedLink, n)
                currentLinks.extend(new_link.links)
                self.linkList.append(new_link)
                time.sleep(5)
            self.currentDepth += 1
            self.depthLinks.append(currentLinks)
        print(f'Ending thread {n}')
        return

    def get_content_from_link(self, link, n):
        print(f'Thread {n}: scraping {link}')
        start_page = requests.get(link)
        document = html.fromstring(start_page.text)
        title = document.xpath('//title/text()')[0]
        links = document.xpath('//a/@href')[:self.breadth]
        new_links = []
        for l in links:
            new_links.append("http://localhost:8000/spiders/" + l)
        link_model = LinkModel(title, link, new_links)
        return link_model


def main():
    with ThreadPoolExecutor(max_workers=3) as executor:
        crawler = LinkCrawler("http://localhost:8000/spiders/web_page.html", 2, 3)
        executor.submit(crawler.startCrawl(1))
        executor.submit(crawler.startCrawl(2))

    for link in crawler.linkList:
        print(link)


if __name__ == '__main__':
    main()
