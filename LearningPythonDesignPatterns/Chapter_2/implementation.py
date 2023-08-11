""""
Simple implementation for web crawler.
download images from page in two threads.
this threads should not interfer with each other , do not scan page if it already scanned,
do not download image if it already exist.
"""
import os.path
import threading
from urllib.parse import urlparse, urljoin, ParseResult
from urllib.request import urlretrieve, urlopen
from logging import getLogger

from bs4 import BeautifulSoup as Bs

from classic import Singleton

class WebThreadSingleton(Singleton):
    __queue_to_parse: list = []
    __parsed_root: ParseResult  = None
    __to_visit: set = set()
    __downloaded: set = set()

    @property # getter
    def parsed_root(self):
        return self.__parsed_root

    @parsed_root.setter # setter
    def parsed_root(self, value):
        self.__parsed_root = value

    @property
    def queue_exist(self):
        return bool(self.__queue_to_parse)

    @property
    def queue_to_parse(self):
        return self.__queue_to_parse

    @property
    def max_visit_links(self):
        return len(self.__to_visit)

    def get_next_link(self):
        link = self.__queue_to_parse.pop()
        return link

    def add_link(self, value):
        self.__to_visit.add(value)

    def is_link_exist(self, value):
        return value in self.__to_visit

    def is_downloaded(self, value):
        return value in self.__downloaded

    @property
    def downloaded(self):
        return self.__downloaded

    @downloaded.setter
    def downloaded(self, value):
        self.__downloaded.add(value)

    def add_to_queue(self, value):
        if isinstance(value, str):
            self.__queue_to_parse.append(value)
        if isinstance(value, list):
            self.__queue_to_parse.extend(value)


logger = getLogger(__name__)

def uri_validator(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception as Err:
        logger.error(str(Err))
        return False

class ImageDownloaderThread(threading.Thread):

    def __init__(self, threat_id, name, counter):
        threading.Thread.__init__(self)
        self.name = name

    def run(self) -> None:
        logger.info('starting thread ', self.name)
        download_images(self.name)
        logger.info('finished thread ', self.name)


def traverse_site(max_links=10):
    link_parser_singleton = WebThreadSingleton()
    while link_parser_singleton.queue_exist:

        if link_parser_singleton.max_visit_links == max_links:
            break

        url = link_parser_singleton.get_next_link()

        try:
            response = urlopen(url)
        except Exception as Err:
            logger.error(msg=str(Err))
            continue

        if response.headers.get_content_type() != 'text/html':
            continue

        link_parser_singleton.add_link(url)
        logger.info('added ', url, ' to queue')

        soup = Bs(response, 'html.parser')

        for link in soup.find_all('a'):
            link_url = link.get('href')

            if not uri_validator(link_url):
                continue

            parsed = urlparse(link_url)

            if parsed.netloc and parsed.netloc != singleton.parsed_root.netloc:
                continue

            link_url = (parsed.scheme or singleton.parsed_root.scheme) + '://' + (parsed.netloc or singleton.parsed_root.netloc) + parsed.path or ''

            if link_parser_singleton.is_link_exist(link_url):
                continue

            link_parser_singleton.add_to_queue(link_url)
            link_parser_singleton.add_to_queue(link_parser_singleton.queue_to_parse)




def download_images(thread_name):
    web_singleton = WebThreadSingleton()
    while web_singleton.max_visit_links:
        url = web_singleton.get_next_link()

        logger.info('Starting download images from ', url)

        try:
            response = urlopen(url)
        except Exception as Err:
            logger.error(str(Err))
            continue

        soup = Bs(response, 'html.parser')

        for image in  soup.find_all('img'):

            src = image.get('src')
            src = urljoin(url, src)
            basename = os.path.basename(src)

            if web_singleton.is_downloaded(src):
                web_singleton.downloaded = src
                logger.info('Downloading ', src)
                urlretrieve(src, os.path.join('images', basename))

        logger.info(thread_name, ' finished downloading images from ', url)


if __name__ == '__main__':
    root = 'https://www.python.org/'

    singleton = WebThreadSingleton()
    singleton.add_to_queue(root)

    singleton.parsed_root = urlparse(root)

    traverse_site()

    if not os.path.exists('images'):
        os.mkdir('images')

    thread1 = ImageDownloaderThread(1, 'Thread-1', 1)
    thread2 = ImageDownloaderThread(2, 'Thread-2', 2)

    thread1.start()
    thread2.start()

    exit(0)
