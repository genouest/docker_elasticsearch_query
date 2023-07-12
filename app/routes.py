from flask import Blueprint, current_app, jsonify, make_response, request

app = Blueprint('app', __name__, url_prefix='/')


@app.route('/')
@app.route('/query')
def index():
    query = request.args.get('q')
    if not query:
        return make_response(jsonify({'error': "Missing 'q' parameter", 'data': []}), 400)
    search_index = current_app.config['ES_INDEX']
    query = _generate_query(current_app.config, query)

    try:
        results = current_app.config['ES_INSTANCE'].search(index=search_index, query=query)
    except Exception as e:
        make_response(jsonify({'error': str(e), 'data': []}), 400)

    return make_response(jsonify({'error': "", 'data': results['hits']['hits']}), 400)


def _generate_query(config, query):
    query = {
        "_source": ["gene_id", "organism", "organism_slug"]
    }

    search_field = config['ES_SEARCH_FIELDS']

    if config["RESTRICT_PUBLIC"]:
        query['query'] = {
            "bool": {
                "must": [
                    {
                        "multi_match": {
                            "query": query,
                            **({'fields': search_field} if search_field else {})
                        }
                    },
                    {
                        "term": {
                            "public": True
                        }
                    }
                ]
            }
        }
    else:
        query['query'] = {
            "multi_match": {
                "query": query,
                **({'fields': search_field} if search_field else {})
            }
        }
    return query
