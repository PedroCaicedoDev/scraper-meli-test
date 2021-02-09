
# Django Rest Framework
from rest_framework import serializers


class StringListField(serializers.ListField):
    child = serializers.CharField()


class ScraperSerializer(serializers.Serializer):

    provider = serializers.ChoiceField(choices=['mercadolibre'])
    provider_url = serializers.URLField()
    provider_category = serializers.CharField(min_length=2)
    provider_url_search = serializers.CharField(allow_blank=True, required=False)

    page_ini = serializers.IntegerField(min_value=1, max_value=20)
    page_end = serializers.IntegerField(min_value=1, max_value=20)

    clean_common_words = StringListField
    clean_sames_words = serializers.DictField(child=serializers.CharField())

    classifier_score_min = serializers.IntegerField(min_value=0, max_value=100)
