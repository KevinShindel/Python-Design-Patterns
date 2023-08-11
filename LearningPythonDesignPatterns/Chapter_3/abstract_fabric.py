import abc
from urllib.error import URLError
from urllib.request import urlopen

from bs4 import BeautifulSoup as Bs


class AbstractFactory:
    """ interface  provides 3 methods to implement in sub-classes: create-protocol, create-port, create-parser """

    __metaclass__ = abc.ABCMeta

    def __init__(self, is_secure):
        self.is_secure = is_secure

    @abc.abstractmethod
    def create_protocol(self):
        pass

    @abc.abstractmethod
    def create_port(self):
        pass

    @abc.abstractmethod
    def create_parser(self):
        pass


class HTTPFactory(AbstractFactory):

    def create_protocol(self):
        return 'https' if self.is_secure else 'http'

    def create_parser(self):
        return HTTPParser()

    def create_port(self):
        return HTTPSecurePort() if self.is_secure else HTTPPort()


class FTPFactory(AbstractFactory):

    def create_protocol(self):
        return 'ftp'

    def create_parser(self):
        return FTPParser()

    def create_port(self):
        return FTPSecurePort() if self.is_secure else FTPPort()


class Port:
    __metaclass__ = abc.ABCMeta
    """ Abstract product. One of its subclasses will created in factory methods"""

    @abc.abstractmethod
    def __str__(self):
        pass


class HTTPPort(Port):
    """ A concrete product which represents http port """

    def __str__(self):
        return '80'


class HTTPSecurePort(Port):
    """ A concrete product which represents https port """

    def __str__(self):
        return '443'


class FTPPort(Port):
    """ A concrete product which represents ftp port """

    def __str__(self):
        return '21'


class FTPSecurePort(Port):

    def __str__(self):
        return '22'


class Parser:
    """ abstract product to represent parser to parse web content """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __call__(self, content, *args, **kwargs):
        pass


class FTPParser(Parser):

    def __call__(self, content, *args, **kwargs):
        filenames = []
        lines = content.split('\n')
        for line in lines:
            splitted_line = line.split(None, 8)
            if len(splitted_line) == 9:
                filenames.append(splitted_line[-1])
        return '\n'.join(filenames)


class HTTPParser(Parser):

    def __call__(self, content, *args, **kwargs):
        soup = Bs(content)
        filenames = [link['href'] for link in soup.find_all('a') if hasattr(link, 'href')]
        return '\n'.join(filenames)


class Connector:

    def __init__(self, factory: AbstractFactory):
        self.port = factory.create_port()
        self.protocol = factory.create_protocol()
        self.parse = factory.create_parser()

    @abc.abstractmethod
    def parse(self, content):
        """ parses web content """
        pass

    def read(self, host, path):
        """ A generic method for all subclasses, read web content """
        url = self.protocol + '://' + host + ':' + str(self.port) + path
        print('connecting to: ', url)
        return urlopen(url).read().decode('utf-8')


if __name__ == '__main__':
    domain = 'ftp.freebsd.org'
    path = '/pub/FreeBSD'

    protocol = int(input(f'Connecting to {domain}. Which protocol to use? (0-http, 1-ftp)'))

    match protocol:
        case 0:
            is_secure = bool(int(input('Use secure connection? (1-yes, 0-no)')))
            factory = HTTPFactory(is_secure)
            pass
        case 1:
            is_secure = bool(int(input('Use secure connection? (1-yes, 0-no)')))
            factory = FTPFactory(is_secure)
        case _:
            raise Exception('Connector is not defined!')

    connector = Connector(factory)
    try:
        content = connector.read(domain, path)
    except URLError as Err:
        print(str(Err))
    else:
        result = connector.parse(content)
        print(result)

    exit(0)
