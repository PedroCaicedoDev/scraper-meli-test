from abc import abstractmethod


class BaseScraper:
    URL_BASE = 'https://celulares.mercadolibre.com.co'
    URL_PATH_NAME = '/xiaomi/'
    URL_SEARCH = ''

    QUANTITY_ITEMS = 50

    CLEAN_COMMON_WORDS = [
        # Product type
        'celular',
        # Brand
        'xiaomi',
        'xioami',
        # Adjectives
        'libre',
        'nuevo',
        # Articles
        'de',
        'y'
    ]

    # Words equivalences or same mean
    CLEAN_SAMES_WORDS = {
        'pocophone': 'poco',
        '6-ram': '6ram',
        '64mpx': '64mpx',
        '64-mpx': '64mpx',
        '128g': '128gb',
        '128gbb': '128gb',
        'mpx': 'mp'
    }

    CLASSIFIER_SCORE_MIN = 80


    def __init__(self, data_request):

        self.URL_BASE = data_request['provider_url']
        self.URL_PATH_NAME = '/' + data_request['provider_category'] + '/'
        self.URL_SEARCH = data_request.get('provider_url_search', '')

        self.CLEAN_COMMON_WORDS = data_request['clean_common_words']
        self.CLEAN_SAMES_WORDS = data_request['clean_sames_words']

        self.CLASSIFIER_SCORE_MIN = data_request['classifier_score_min']

    def get_products_of_pages(self, pages='1-5'):

        pages_range = self.get_pages_list(pages)

        page_ini = pages_range[0]
        page_end = pages_range[1]

        pages_range = range(page_ini, page_end + 1)

        # Extraction layer
        extractor = self._get_extractor(self.URL_BASE, self.URL_PATH_NAME, self.URL_SEARCH)
        raw_pages = extractor.get_pages(pages_range=pages_range, quantity_items=self.QUANTITY_ITEMS)
        raw_items = extractor.get_items_from_pages(raw_pages)

        # Transform layer
        transformer = self._get_transformer()
        items = transformer.from_raw_to_json(raw_items)

        # Cleaner layer
        cleaner = self._get_cleaner()
        clean_items = cleaner.clean_items(items, self.CLEAN_COMMON_WORDS, self.CLEAN_SAMES_WORDS)

        # Classifier layer
        classifier = self._get_classifier()
        classify_items = classifier.classify_items_slug(clean_items, score_min=self.CLASSIFIER_SCORE_MIN)

        # Refiner layer
        refiner = self._get_refiner()
        refine_items = refiner.basic(clean_items, classify_items)

        # Presenter layer
        presenter = self._get_presenter()
        json_response = presenter.basic(clean_items, classify_items, refine_items)

        return json_response

    def get_pages_list(self, pages):
        pages_range = list(map(int, pages.split('-')))

        if len(pages_range) < 2:
            pages_range.append(pages_range[1])

        return pages_range

    @abstractmethod
    def _get_extractor(self, url_base, url_path_name, url_search):
        pass

    @abstractmethod
    def _get_transformer(self):
        pass

    @abstractmethod
    def _get_cleaner(self):
        pass

    @abstractmethod
    def _get_classifier(self):
        pass

    @abstractmethod
    def _get_refiner(self):
        pass

    @abstractmethod
    def _get_presenter(self):
        pass
