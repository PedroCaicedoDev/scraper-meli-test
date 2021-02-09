
class MercadolibreTransformer:

    def transform_item(self, raw_item):
        title = raw_item.find('h2', class_='ui-search-item__title')
        price = raw_item.find('span', class_='price-tag-fraction')
        image = raw_item.find('img', class_='ui-search-result-image__element')

        return {
            'title': title.text,
            'price': price.text,
            'image': image['data-src'],
        }

    def from_raw_to_json(self, raw_items):
        result_json_items = []
        for raw_item in raw_items:
            item = self.transform_item(raw_item)
            result_json_items.append(item)

        return result_json_items
