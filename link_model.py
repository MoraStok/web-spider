class LinkModel:

    def __init__(self, title, url, links):
        self.title = title
        self.url = url
        self.links = links

    def __str__(self):
        return "\nTitle: " + self.title + "\nURL: " + self.url