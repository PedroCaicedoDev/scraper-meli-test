from ..classifiers.BaseClassifier import BaseClassifier


class BasePresenter:

    def basic(self, items, classify_items, refine_items):
        simple_count = {}
        full_data = []

        for classify_key in classify_items:

            item = items[classify_key]
            same_items = classify_items[classify_key]

            group_slug = BaseClassifier.get_heuristic_slug(item['clean']['slug'])

            json_item = {
                'count': 1,
                'group_slug': group_slug,
                'slug': item['clean']['slug'],
                'item': item,
                'same_items': []
            }

            # print('-------', classify_key, item['clean']['slug'])
            for same_item in (same_items):
                # print(same_item[0], items[same_item[0]]['clean']['slug'], same_item[1])
                json_item['same_items'].append(items[same_item[0]])

            json_item['count'] = 1 + len(json_item['same_items'])

            simple_count[group_slug] = json_item['count']

            full_data.append(json_item)

        return {
            'simple': simple_count,
            'refined_with_rom': self.refined_with_rom(refine_items),
            'data': {
                'refined': refine_items,
                'full': full_data
            }
        }

    def refined_with_rom(self, refine_items):
        result = {}

        for group_father_slug in refine_items:
            group_father_items = refine_items[group_father_slug]['rom']
            for rom_slug in group_father_items:
                path_slug = '{}-rom-{}'.format(group_father_slug, rom_slug)
                result[path_slug] = len(group_father_items[rom_slug])

        return result
