from lxml import html
import requests
import time
from link_model import LinkModel


class LinkCrawler:

    def __init__(self, starting_url, depth = 10, breadth = 10):
        self.starting_url = starting_url
        self.depth = depth
        self.breadth = breadth
        self.currentDepth = 0
        self.depthLinks = []
        self.linkList = []

    def startCrawl(self):
        link = self.get_content_from_link(self.starting_url)
        self.linkList.append(link)
        self.depthLinks.append(link.links)
        while self.currentDepth < self.depth:
            currentLinks = []
            for relatedLink in self.depthLinks[self.currentDepth]:
                new_link = self.get_content_from_link(relatedLink)
                currentLinks.extend(new_link.links)
                self.linkList.append(new_link)
                time.sleep(5)
            self.currentDepth += 1
            self.depthLinks.append(currentLinks)
        return

    def get_content_from_link(self, link):
        start_page = requests.get(link)
        document = html.fromstring(start_page.text)
        title = document.xpath('//title/text()')[0]
        text = document.xpath('//div[@id = "leftmenuinnerinner"]//a/text()')[0]
        links = document.xpath('//div[@id = "leftmenuinnerinner"]//a/@href')[:self.breadth]
        new_links = []
        for l in links:
            new_links.append("https://www.w3schools.com/html/" + l)
        link_model = LinkModel(title, text, link, new_links)
        return link_model


crawler = LinkCrawler("https://www.w3schools.com/html/default.asp", 2, 2)
crawler.startCrawl()

for link in crawler.linkList:
    print(link)
