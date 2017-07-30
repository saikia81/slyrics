from bs4 import BeautifulSoup

import requests

class Lyrics:
    def __init__(self, url, text):
        self._url = url
        self._text = text

    def get_url(self):
        return self._url

    def get_text(self):
        return self._text

class Scraper:
    def __init__(self, name):
        self.name = name

    def req(self, url, **kwargs):
        return requests.get(url, **kwargs)

    def find(self, track, artist):
        raise NotImplementedError("method not callable from base class")

class GeniusScraper(Scraper):
    def __init__(self):
        super().__init__("Genius")

    def find(self, track, artist):
        url = "https://genius.com/search?q={0} {1}".format(track, artist)
        res = self.req(url).text
        soup = BeautifulSoup(res, 'html.parser')
        url = soup.find("a", {"class": " song_link"}, href=True)
        if not url:
            raise Exception("couldn't find track")
        url = url["href"]

        res = self.req(url).text
        soup = BeautifulSoup(res, 'html.parser')
        lyrics = soup.find("div", {"class": "lyrics"})
        if not lyrics:
            raise Exception("error parsing lyrics")

        return Lyrics(url, lyrics.p.text)

scrapers = [
    GeniusScraper(),
]

def find(track, artist):
    for scraper in scrapers:
        try:
            return scraper.find(track, artist)
        except Exception as e:
            continue
    return None
