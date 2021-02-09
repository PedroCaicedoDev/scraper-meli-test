
from slugify import slugify


class MercadolibreCleaner:

    def clean_items(self, items, clean_words, clean_similar_words):

        clean_items = []
        for item in items:
            slug = self.get_slug(item)

            slug_without_words = self.clean_words_slug(slug, clean_words)
            slug_clean = self.clean_slimilars_words(slug_without_words, clean_similar_words)

            clean_item = self.clean_item(slug_clean, item)
            clean_items.append(clean_item)

        return clean_items

    def get_slug(self, item):
        title = '' + item['title']
        title = title.strip().lower()

        return slugify(title)

    def clean_words_slug(self, slug, clean_words):
        for word in clean_words:
            slug = slugify(''.join(slug.split(word)))

        return slug

    def clean_slimilars_words(self, slug, clean_similar_words):

        for word in clean_similar_words:
            word_clean = clean_similar_words[word]

            slug = slug.replace(word, word_clean, 1)

        return slug

    def clean_item(self, slug_clean, item):
        title = '' + item['title']
        title = title.strip().lower()

        return {
            'original': item,
            'clean': {
                'title': title,
                'slug': slug_clean,
                'price': item['price'],
                'image': item['image']
            }
        }
