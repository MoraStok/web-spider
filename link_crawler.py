from lxml import html
import requests
import time
from link_model import LinkModel
from concurrent.futures import ThreadPoolExecutor


class LinkCrawler:

    def __init__(self, starting_url, depth = 10, breadth = 10):
        self.starting_url = starting_url
        self.pool = ThreadPoolExecutor(max_workers=3,thread_name_prefix='0-')
        self.depth = depth
        self.breadth = breadth
        self.currentDepth = 0
        self.depthLinks = []
        self.linkList = []

    def startCrawl(self):
        link = self.pool.submit(self.get_content_from_link, self.starting_url)
        print(link.result())
        self.linkList.append(link.result())
        self.depthLinks.append(link.result().links)
        while self.currentDepth < self.depth:
            currentLinks = []
            for relatedLink in self.depthLinks[self.currentDepth]:
                new_link = self.pool.submit(self.get_content_from_link, relatedLink)
                print(new_link.result())
                currentLinks.extend(new_link.result().links)
                self.linkList.append(new_link.result())
                time.sleep(2)
            self.currentDepth += 1
            self.depthLinks.append(currentLinks)
        return

    def get_content_from_link(self, link):
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
    crawler = LinkCrawler("http://localhost:8000/spiders/web_page.html", 2, 3)
    crawler.startCrawl()


if __name__ == '__main__':
    main()
