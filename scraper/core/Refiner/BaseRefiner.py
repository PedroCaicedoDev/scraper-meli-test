from slugify import slugify

from ..classifiers.BaseClassifier import BaseClassifier


class BaseRefiner:
    def basic(self, clean_items, classify_items):
        groups_with_feature = {}

        for item_first_id in classify_items:
            items_with_feature = {
                'rom': {},
                'ram': {},
                'battery': {},
                'camera': {},
            }

            group_slug = BaseClassifier.get_heuristic_slug(clean_items[item_first_id]['clean']['slug'])

            items_group = classify_items[item_first_id]

            # Add first item
            items_group.append((item_first_id, 100))

            for item in items_group:
                item_id = item[0]
                item_first_score = item[1]
                item_slug = clean_items[item_id]['clean']['slug']

                # Clean new slug
                item_description_slug = self.clean_group_slug(group_slug, item_slug)

                arr_despriction = self.sort_numeric(item_description_slug.split('-'))

                # ROM
                rom = self.get_description_rom(arr_despriction)

                try:
                    arr_despriction.remove(rom)
                except:
                    print('rom does not exit', rom)

                # RAM
                ram = self.get_description_ram(arr_despriction)

                try:
                    arr_despriction.remove(ram)
                except:
                    print('ram does not exit', ram)

                # BATTERY
                battery = self.get_description_battery(arr_despriction)

                try:
                    arr_despriction.remove(battery)
                except:
                    print('battery does not exit', battery)

                # CAMERA
                camera = self.get_description_camera(arr_despriction)

                try:
                    arr_despriction.remove(camera)
                except:
                    print('camera does not exit', camera)

                # Add roms ids
                if rom not in items_with_feature['rom']:
                    items_with_feature['rom'][rom] = [item_id]
                else:
                    items_with_feature['rom'][rom] += [item_id]

                # Add rams ids
                if ram not in items_with_feature['ram']:
                    items_with_feature['ram'][ram] = [item_id]
                else:
                    items_with_feature['ram'][ram] += [item_id]

                # Add batteries ids
                if battery not in items_with_feature['battery']:
                    items_with_feature['battery'][battery] = [item_id]
                else:
                    items_with_feature['battery'][battery] += [item_id]

                # Add cameras ids
                if camera not in items_with_feature['camera']:
                    items_with_feature['camera'][camera] = [item_id]
                else:
                    items_with_feature['camera'][camera] += [item_id]

                groups_with_feature[group_slug] = items_with_feature

        # print(groups_with_feature)
        return groups_with_feature

    def get_description_rom(self, arr_despriction):
        rom = 0

        for feature in arr_despriction:
            quantity_rom_duple = self.get_number(feature)
            if 1024 > quantity_rom_duple[1] > 16:
                rom = quantity_rom_duple[1]
                break
        return rom

    def get_description_ram(self, arr_despriction):
        ram = 0

        for feature in arr_despriction:
            quantity_ram_duple = self.get_number(feature)
            if 16 > quantity_ram_duple[1] > 1:
                ram = quantity_ram_duple[1]
                break
        return ram

    def get_description_battery(self, arr_despriction):
        battery = 0

        for feature in arr_despriction:
            quantity_battery_duple = self.get_number(feature)
            if quantity_battery_duple[1] > 1024:
                battery = quantity_battery_duple[1]
                break
        return battery

    def get_description_camera(self, arr_despriction):
        camera = 0

        for feature in arr_despriction:
            quantity_camera_duple = self.get_number(feature)
            if 100 > quantity_camera_duple[1] > 0:
                camera = quantity_camera_duple[1]
                break
        return camera

    def clean_group_slug(self, group_slug, slug_item):
        arr_group_slug = group_slug.split('-')

        for word_group_slug in arr_group_slug:
            slug_item = slug_item.replace(word_group_slug, '', 1)

        return slugify(slug_item)

    def sort_numeric(self, arr_words):
        arr_word_duples = []
        for word in arr_words:
            arr_word_duples.append(self.get_number(word))

        arr_word_duples_sorted = sorted(arr_word_duples, key=lambda word_duple: word_duple[1], reverse=True)

        result_words = []
        for arr_word_duples in arr_word_duples_sorted:
            result_words.append(arr_word_duples[0])

        return result_words

    @staticmethod
    def get_number(word):
        word_number = ''

        for char in word:
            if char in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                word_number += char
        number = 0

        if word_number != '':
            number = int(word_number)

        return word, number
