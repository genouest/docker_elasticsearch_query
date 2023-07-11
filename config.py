import os

from elasticsearch import Elasticsearch


class Config(object):
    ES_URL = os.environ.get('ELASTICSEARCH_CONTAINER', 'elasticsearch')
    ES_PORT = os.environ.get('ELASTICSEARCH_PORT', '9200')
    ES_INDEX = os.environ.get('ES_INDEX', 'genes')
    # Use restrict public if some datasets in Elasticsearch are private
    RESTRICT_PUBLIC = os.environ.get('RESTRICT_PUBLIC', False)
    ES_SEARCH_FIELDS = os.environ.get('ES_SEARCH_FIELDS', "").split(",")

    es_url = "http://{}:{}".format(ES_URL, ES_PORT)
    ES_INSTANCE = Elasticsearch(es_url)