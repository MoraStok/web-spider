from lxml import html
import requests
import time
from link_model import LinkModel
# from concurrent.futures import ThreadPoolExecutor
import threading


class LinkCrawler:

    def __init__(self, starting_url, depth = 10, breadth = 10):
        self.starting_url = starting_url
        self.depth = depth
        self.breadth = breadth
        self.currentDepth = 0
        self.depthLinks = []
        self.linkList = []

    def startCrawl(self):
        print("Starting thread: {}".format(threading.current_thread().name)) 
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
        print("Ending thread: {}".format(threading.current_thread().name))
        return

    def get_content_from_link(self, link):
        print("Thread {}: scraping {}".format(threading.current_thread().name, link)) 
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
    t1 = threading.Thread(target=crawler.startCrawl, name='1') 
    t2 = threading.Thread(target=crawler.startCrawl, name='2')   
  
    t1.start() 
    t2.start() 
  
    t1.join() 
    t2.join()

    for link in crawler.linkList:
        print(link)


if __name__ == '__main__':
    main()
