# Model-View-Controller pattern

import pickle

class URL:

    @classmethod
    def shorten(cls, full_url):
        instance = cls()
        instance.full_url = full_url
        instance.short_url = instance.__create_short_url()
        URL.__save_url_mapping(instance)
        return instance

    @classmethod
    def get_by_short_url(cls, short_url):
        url_mapping = URL.__load_url_mapping()
        return url_mapping.get(short_url)

    def __create_short_url(self):
        last_short_url = URL.__load_last_short_url()
        short_url = self.__increment_string(last_short_url)
        URL.__save_last_short_url(short_url)
        return short_url

    def __increment_string(self, string):
        if string == '':
            return 'a'

        last_chart = string[-1]

        if last_chart != 'z':
            return string[:-1] + chr(ord(last_chart) + 1)

        return self.__increment_string(string[:-1]) + 'a'

    @staticmethod
    def __load_last_short_url():
        try:
            data = pickle.load(open('last_short.p', 'rb'))
            return data
        except IOError:
            return ''

    @staticmethod
    def __save_last_short_url(url):
        pickle.dump(url , open('short_to_url.p', 'wb'))

    @staticmethod
    def __load_url_mapping():
        try:
            data = pickle.load(open('short_to_url.p', 'rb'))
            return data
        except IOError:
            return {}

    @staticmethod
    def __save_url_mapping(instance):
        short_to_url = URL.__load_url_mapping()
        short_to_url[instance.short_url] = instance
        pickle.dump(short_to_url, open('short_to_url.p', 'wb'))
