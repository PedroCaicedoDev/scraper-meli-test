
from django.http import JsonResponse

from rest_framework.decorators import api_view

from .serializers import ScraperSerializer

from .core.scrapers.MercadolibreScraper import MercadolibreScraper

@api_view(['POST'])
def scraper(request):

    serializer = ScraperSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)

    page_ini = request.data['page_ini']
    page_end = request.data['page_end']

    if page_ini > page_end:
        raise Exception('page_ini is not greater what page_end')

    provider = request.data['provider']

    if provider == 'mercadolibre':
        scraper = MercadolibreScraper(request.data)

    if provider == 'olx':
        raise Exception("Don't support")

    pages = str(page_ini) + '-' + str(page_end)
    response = scraper.get_products_of_pages(pages)

    return JsonResponse(response)
