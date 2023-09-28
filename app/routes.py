from flask import Blueprint, current_app, jsonify, make_response, request

app = Blueprint('app', __name__, url_prefix='/')


@app.route('/')
@app.route('/query')
def index():
    query = request.args.get('q')
    if not query:
        return make_response(jsonify({'error': "Missing 'q' parameter", 'data': []}), 400)

    show_highlight = True
    if request.args.get('highlighting', "1").lower() in ['0', 'false']:
        show_highlight = False

    max_results = current_app.config['ES_MAX_RESULTS']
    try:
        max_results = int(request.args.get('max_results'))
    except (ValueError, TypeError):
        return make_response(jsonify({'error': "'max_results' parameter is not an integer", 'data': []}), 400)

    display_fields = current_app.config['ES_DISPLAY_FIELDS']
    if 'display_fields' in request.args:
        display_fields = request.args.get('display_fields').split(',')

    search_index = current_app.config['ES_INDEX']
    display_fields = current_app.config['ES_DISPLAY_FIELDS']
    es_query = _generate_query(current_app.config, query)
    highlight = {}
    if show_highlight:
        highlight_pre = ["<{}>".format(current_app.config['ES_HIGHLIGHT_TAG'])]
        highligh_post = ["</{}>".format(current_app.config['ES_HIGHLIGHT_TAG'])]
        highlight = {"fields": {"*": {}}, "pre_tags": highlight_pre, "post_tags": highligh_post}
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
