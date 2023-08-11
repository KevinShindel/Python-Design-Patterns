# Simple fabric pattern
from http.client import HTTPConnection
from ftplib import FTP as FTPConnection


class SimpleFactory:

    @staticmethod
    def build_connection(protocol):
        match protocol:
            case 'http':
                return HTTPConnection()
            case 'ftp':
                return FTPConnection()


if __name__ == '__main__':
    protocol = input('Select protocol (http, ftp): ')
    protocol = SimpleFactory.build_connection(protocol)
    protocol.connect()
    print(protocol.getresponse())
