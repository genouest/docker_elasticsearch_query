from flask import Blueprint, current_app, jsonify, make_response, request

app = Blueprint('app', __name__, url_prefix='/')


@app.route('/')
@app.route('/query')
def index():
    query = request.args.get('q')
    if not query:
        return make_response(jsonify({'error': "Missing 'q' parameter", 'data': []}), 400)
    search_index = current_app.config['ES_INDEX']
    display_fields = current_app.config['ES_DISPLAY_FIELDS']
    es_query = _generate_query(current_app.config, query)
    highlight_pre = ["<{}>".format(current_app.config['ES_HIGHLIGHT_TAG'])]
    highligh_post = ["</{}>".format(current_app.config['ES_HIGHLIGHT_TAG'])]
    highlight = {"fields": {"*": {}}, "pre_tags": highlight_pre, "post_tags": highligh_post}
    max_results = current_app.config['ES_MAX_RESULTS']
    try:
        results = current_app.config['ES_INSTANCE'].search(index=search_index, query=es_query, source=display_fields, highlight=highlight, size=max_results)
    except Exception as e:
        return make_response(jsonify({'error': str(e), 'data': []}), 400)

    return make_response(jsonify({'error': "", 'data': results['hits']['hits']}), 200)


def _generate_query(config, user_query):
    query = {}
    search_field = config['ES_SEARCH_FIELDS']

    if config["RESTRICT_PUBLIC"]:
        query["bool"] = {
            "must": [
                {
                    "multi_match": {
                        "query": user_query,
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
    else:
        query['multi_match'] = {
            "query": user_query,
            **({'fields': search_field} if search_field else {})
        }
    return query
