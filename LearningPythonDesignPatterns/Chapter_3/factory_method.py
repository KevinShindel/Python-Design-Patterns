import abc
from urllib.error import URLError
from urllib.request import urlopen

from bs4 import BeautifulSoup as Bs


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


class Connector:
    """ Abstract class to connect to remote resource """
    __metaclass__ = abc.ABCMeta

    def __init__(self, is_secure):
        self.is_secure = is_secure
        self.port = self.port_factory_method()
        self.protocol = self.protocol_factory_method()

    @abc.abstractmethod
    def parse(self, content):
        """ parses web content """
        pass

    def read(self, host, path):
        """ A generic method for all subclasses, read web content """
        url = self.protocol + '://' + host + ':' + str(self.port) + path
        print('connecting to: ', url)
        return urlopen(url).read().decode('utf-8')

    @abc.abstractmethod
    def protocol_factory_method(self):
        """ A factory method that must be redefined in subclass. """
        pass

    @abc.abstractmethod
    def port_factory_method(self):
        pass


class HTTPConnector(Connector):
    """ A concrete creator that creates a HTTP connector and sets in runtime all its attributes. """

    def protocol_factory_method(self):
        if self.is_secure:
            return 'https'
        else:
            return 'http'

    def port_factory_method(self):
        """ Here HTTPPort and HTTPSecure port are concrete objects """

        if self.is_secure:
            return HTTPSecurePort()
        else:
            return HTTPPort()

    def parse(self, content):
        """ Parses web content """

        soup = Bs(content)
        filenames = [link['href'] for link in soup.find_all('a') if hasattr(link, 'href')]
        return '\n'.join(filenames)


class FTPConnector(Connector):
    """ A concrete creator that creates a FTP connector and sets in runtime all its attributes. """

    def protocol_factory_method(self):
        if self.is_secure:
            return 'ftps'
        else:
            return 'ftp'

    def port_factory_method(self):
        return FTPPort()

    def parse(self, content):
        filenames = []
        lines = content.split('\n')
        for line in lines:
            splitted_line = line.split(None, 8)
            if len(splitted_line) == 9:
                filenames.append(splitted_line[-1])
        return '\n'.join(filenames)


if __name__ == '__main__':
    domain = 'ftp.freebsd.org'
    path = '/pub/FreeBSD'

    protocol = int(input(f'Connecting to {domain}. Which protocol to use? (0-http, 1-ftp)'))

    match protocol:
        case 0:
            is_secure = bool(int(input('Use secure connection? (1-yes, 0-no)')))
            connector = HTTPConnector(is_secure)
            pass
        case 1:
            is_secure = bool(int(input('Use secure connection? (1-yes, 0-no)')))
            connector = FTPConnector(is_secure)
        case _:
            raise Exception('Connector is not defined!')

    try:
        content = connector.read(domain, path)
    except URLError as Err:
        print(str(Err))
    else:
        result = connector.parse(content)
        print(result)

    exit(0)
