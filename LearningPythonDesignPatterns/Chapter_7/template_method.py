import urllib
from urllib.request import urlopen
from xml.dom import minidom


class AbstractNewsParser:

    def __int__(self):
        if self.__class__ is AbstractNewsParser:
            raise TypeError('abstract class cannot be instantinated')

    def print_top_news(self):
        url = self.get_url()
        raw_content = self.get_raw_content(url)
        content = self.parse_content(raw_content)
        cropped = self.crop_content(content)

        for item in cropped:
            print('title: ', item['title'])
            print('content', item['content'])
            print('link', item['link'])
            print('published', item['published'])
            print('id', item['id'])

    def get_url(self):
        raise NotImplementedError

    def parse_content(self, raw_content):
        raise NotImplementedError

    @staticmethod
    def crop_content(parsed_content, max_items=3):
        return parsed_content[:max_items]

    @staticmethod
    def get_raw_content(url):
        return urlopen(url).read()


class YahooParser(AbstractNewsParser):

    def get_url(self):
        return 'https://news.yahoo.com/rss'

    def parse_content(self, raw_content):
        parsed_content = []

        dom = minidom.parseString(raw_content)
        for node in dom.getElementByTagName('item'):
            parsed_item = {}

            try:
                parsed_item['title'] = node.getElementsByTagName('title')[0].childNodes[0].nodeValue
            except IndexError:
                parsed_item['title'] = None

            try:
                parsed_item['content'] = node.getElementsByTagName('description')[0].childNodes[0].nodeValue
            except IndexError:
                parsed_item['content'] = None

            try:
                parsed_item['link'] = node.getElementsByTagName('link')[0].childNodes[0].nodeValue
            except IndexError:
                parsed_item['link'] = None

            try:
                parsed_item['id'] = node.getElementsByTagName('guid')[0].childNodes[0].nodeValue
            except IndexError:
                parsed_item['id'] = None

            try:
                parsed_item['published'] = node.getElementsByTagName('pubDate')[0].childNodes[0].nodeValue
            except IndexError:
                parsed_item['title'] = None

            parsed_content.append(parsed_item)

        return parsed_content


class GoogleParser(AbstractNewsParser):

    def get_url(self):
        return 'https://news.google.com/news/feeds?output=atom'

    def parse_content(self, raw_content):
        parsed_content = []

        dom = minidom.parseString(raw_content)
        for node in dom.getElementsByTagName('entry'):
            parsed_item = {}

            try:
                parsed_item['title'] = node.getElementsByTagName('title')[0].childNodes[0].nodeValue
            except IndexError:
                parsed_item['title'] = None

            try:
                parsed_item['content'] = node.getElementsByTagName('description')[0].childNodes[0].nodeValue
            except IndexError:
                parsed_item['content'] = None

            try:
                parsed_item['link'] = node.getElementsByTagName('link')[0].childNodes[0].nodeValue
            except IndexError:
                parsed_item['link'] = None

            try:
                parsed_item['id'] = node.getElementsByTagName('guid')[0].childNodes[0].nodeValue
            except IndexError:
                parsed_item['id'] = None

            try:
                parsed_item['published'] = node.getElementsByTagName('updated')[0].childNodes[0].nodeValue
            except IndexError:
                parsed_item['title'] = None

            parsed_content.append(parsed_item)

        return parsed_content


if __name__ == '__main__':
    google = GoogleParser()
    yahoo = YahooParser()
    print('Google news: ', google.print_top_news())
    print('Yahoo news: ', google.print_top_news())