# docker_elasticsearch_exec

Small flask frontend to be deploy with an ES container.
Will forward queries to it without exposing it to the public.

Environment variables:

```
ES_URL = Url for the ES container (or container name, if using docker-compose). Default to 'elasticsearch'
ES_PORT = Port for ES. Default to '9200'
ES_INDEX = Index name. Default to 'genes'

RESTRICT_PUBLIC = Whether to restrict queries to documents with 'public=True'. Default to False
ES_SEARCH_FIELDS = List of comma-separated fields to search. Default to None, which will search on all fields
ES_DISPLAY_FIELDS = List of comma-separated fields to return. Default to all
ES_MAX_RESULTS = Number of results returned by the query. Default to 10
ES_HIGHLIGHT_TAG = Html tag (without <>) wrapping the highlights (matched terms). Default to 'em'
ES_ALLOWED_FILTERS = List of comma-separated fields that can be used as direct filters. Default to none
```

Simple send your query to the '/' or '/query' endpoint, with the query itself as the 'q' get parameter.
You may pass additional get parameters depending on what you need

```
'highlighting': Boolean value, default to true. Whether the highlights will be returned by the query.
'max_results': Integer value, default to the 'ES_MAX_RESULTS' env variable. How many results are returned by the query.
'display_fields': Coma-separated list of fields. Default to the 'ES_DISPLAY_FIELDS' env variable. Which fields will be returned by the query
```

You can pass additional exact filters on some fields as get parameters (using field=value), as long as the field is set in the 'ES_ALLOWED_FILTERS' env variable.
