class LinkModel:

    def __init__(self, title, text, url, links):
        self.title = title
        self.text = text
        self.url = url
        self.links = links

    def __str__(self):
        return "\nTitle: " + self.title + "\nURL: " + self.url + "\nText: " + self.text