from bs4 import BeautifulSoup

from .BaseExtractor import BaseExtractor


class MercadolibreExtractor(BaseExtractor):

    def get_pages(self, pages_range, quantity_items):
        result_pages = []

        for number_page in pages_range:
            url_path_extra = ''
            if number_page > 1:
                url_path_extra = '_Desde_{}'.format(str((number_page-1) * quantity_items+1))

            result_pages.append(self.get_page(url_path_extra))

        return result_pages

    def get_items_from_page(self, page):
        soup = BeautifulSoup(page.content, 'html.parser')
        # TODO se puede generalizar
        return soup.find_all('li', class_='ui-search-layout__item')

    def get_items_from_pages(self, pages):
        result_items = []
        for page in pages:
            items = self.get_items_from_page(page)

            result_items += items

        return result_items
