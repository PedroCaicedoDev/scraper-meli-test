
import requests
from bs4 import BeautifulSoup


class BaseExtractor:
    URL_BASE = ''
    URL_PATH_NAME = ''
    URL_SEARCH = ''

    def __init__(self, url_base, url_path_name, url_search):
        self.URL_BASE = url_base
        self.URL_PATH_NAME = url_path_name
        self.URL_SEARCH = url_search

    def get_url(self, extra):
        return self.URL_BASE + self.URL_PATH_NAME + self.URL_SEARCH + extra

    def get_page(self, extra=''):
        print('url_extra', self.get_url(extra))
        return requests.get(self.get_url(extra))

    #page 1-5
    def get_pages(self, extra=''):
        pass

    def get_items_from_page(self, page):
        soup = BeautifulSoup(page.content, 'html.parser')
        return soup.find_all('li', class_='ui-search-layout__item')
