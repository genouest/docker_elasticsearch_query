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
```

Simple send your query to the '/' or '/query' endpoint, with the query itself as the 'q' get parameter.
