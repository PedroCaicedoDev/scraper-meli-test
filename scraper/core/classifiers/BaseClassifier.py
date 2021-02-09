
import math
import re
from collections import Counter, OrderedDict


class BaseClassifier:
    WORD = re.compile(r'\w+')

    def get_cosine(self, vec1, vec2):
        # print vec1, vec2
        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = sum([vec1[x] * vec2[x] for x in intersection])

        sum1 = sum([vec1[x] ** 2 for x in vec1.keys()])
        sum2 = sum([vec2[x] ** 2 for x in vec2.keys()])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)

        if not denominator:
            return 0.0
        else:
            return float(numerator) / denominator

    def text_to_vector(self, text):
        return Counter(self.WORD.findall(text))

    def get_similarity(self, a, b):
        a = self.text_to_vector(a.strip().lower())
        b = self.text_to_vector(b.strip().lower())

        return int((self.get_cosine(a, b) + 0.001) * 100)

        return self.get_cosine(a, b)

    # Calificador y clasificador
    def classify_items_slug(self, items, score_min):

        classify_items = {}

        for key, item in enumerate(items):

            scores = {}
            for nex_key, next_item in enumerate(items):

                if key == nex_key:
                    continue

                slug_item = self.get_heuristic_slug(item['clean']['slug'])
                slug_next_item = self.get_heuristic_slug(next_item['clean']['slug'])
                score = self.get_similarity(slug_item, slug_next_item)

                # Classify
                if score >= score_min:
                    scores[nex_key] = score

            # Sort by value
            scores_sorted = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)

            classify_items[key] = scores_sorted

        return self.order_and_clean(classify_items)

    def order_and_clean(self, classify_items):

        count_items = {}
        for key, item in classify_items.items():
            count_items[key] = len(item)

        # Order asc
        sort_count_items = {k: v for k, v in sorted(count_items.items(), key=lambda item: item[1])}

        # Clean repeated
        clean_items = {}
        items_ids = []

        for key, item in sort_count_items.items():
            if key not in items_ids:
                items_ids.append(key)
                clean_items[key] = []

                for classify_item in classify_items[key]:
                    id = classify_item[0]

                    if id not in items_ids:
                        clean_items[key].append(classify_item)
                        items_ids.append(id)

        return clean_items

    # Euristica no se repiten dos nros seguidos
    @staticmethod
    def get_heuristic_slug(slug):
        names = slug.split('-')
        count_numbers = 0
        result_names = []
        for name in names:
            if BaseClassifier.has_number(name):
                count_numbers += 1

            if count_numbers > 1:
                break

            result_names.append(name)

        return '-'.join(result_names)

    @staticmethod
    def has_number(str):
        for char in str:
            if char in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                return True
        return False
