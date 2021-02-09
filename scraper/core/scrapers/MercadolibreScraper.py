
from ..extractors.MercadolibreExtractor import MercadolibreExtractor

from ..transfomers.MercadolibreTransformer import MercadolibreTransformer

from ..cleaner.MercadolibreCleaner import MercadolibreCleaner

from ..classifiers.BaseClassifier import BaseClassifier

from ..Refiner.BaseRefiner import BaseRefiner

from ..Presenters.BasePresenter import BasePresenter

from .BaseScraper import BaseScraper


class MercadolibreScraper(BaseScraper):

    def _get_extractor(self, url_base, url_path_name, url_search):
        return MercadolibreExtractor(url_base, url_path_name, url_search)

    def _get_transformer(self):
        return MercadolibreTransformer()

    def _get_cleaner(self):
        return MercadolibreCleaner()

    def _get_classifier(self):
        return BaseClassifier()

    def _get_refiner(self):
        return BaseRefiner()

    def _get_presenter(self):
        return BasePresenter()
