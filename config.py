import os

from elasticsearch import Elasticsearch


class Config(object):
    ES_URL = os.environ.get('ES_URL', 'elasticsearch')
    ES_PORT = os.environ.get('ES_PORT', '9200')
    ES_INDEX = os.environ.get('ES_INDEX', 'genes')
    # Use restrict public if some datasets in Elasticsearch are private
    RESTRICT_PUBLIC = os.environ.get('RESTRICT_PUBLIC', False)
    ES_MAX_RESULTS = int(os.environ.get('ES_MAX_RESULTS', 10))
    search_fields = os.environ.get('ES_SEARCH_FIELDS', "")
    ES_SEARCH_FIELDS = search_fields.split(",") if search_fields else []
    display_fields = os.environ.get('ES_DISPLAY_FIELDS', "")
    ES_DISPLAY_FIELDS = display_fields.split(",") if display_fields else []
    es_url = "http://{}:{}".format(ES_URL, ES_PORT)
    allowed_filters = os.environ.get('ES_ALLOWED_FILTERS', "")
    ES_ALLOWED_FILTERS = allowed_filters.split(",") if allowed_filters else []
    ES_INSTANCE = Elasticsearch(es_url)
    ES_HIGHLIGHT_TAG = os.environ.get('ES_HIGHLIGHT_TAG', 'em')
