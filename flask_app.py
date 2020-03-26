from flask import Flask, abort, jsonify
from flask_caching import Cache
from flask_cors import CORS

import main

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/')
def display_available():
    content = ('<html>' +
               '<head>' +
               '<title>Restaurant Menu Parser</title>' +
               '</head>' +
               '<body>' +
               '<span style="font-weight: bold">' +
               '<p>This page is no longer updated. The current version can be found at ' +
               '<a href="https://menu.dckube.scilifelab.se/">' + 
               'https://menu.dckube.scilifelab.se/</a>.</p>' +
               '</span>' +
               '<p><a href="ki">Campus Solna (KI)</a></p>' +
               '<p><a href="uu">Campus Uppsala (BMC)</a></p>' +
               '</body>' +
               '</html>')
    return content

@app.route('/api/restaurants')
@cache.cached(timeout=3600)
def api_list_restaurants():
    return jsonify(main.list_restaurants())


@app.route('/api/restaurant/dsw/<name>')
@cache.cached(timeout=3600)
def api_get_restaurant_dsw(name):
    data = main.get_restaurant(name)
    if not data:
        abort(404)
    data['menu'] = [{'dish': entry} for entry in data['menu']]
    return jsonify(data)


@app.route('/api/restaurant/<name>')
@cache.cached(timeout=3600)
def api_get_restaurant(name):
    data = main.get_restaurant(name)
    if not data:
        abort(404)
    return jsonify(data)


@app.route('/ki')
@cache.cached(timeout=3600)
def make_menu_ki():
    return main.gen_ki_menu()


@app.route('/uu')
@cache.cached(timeout=3600)
def make_menu_uu():
    return main.gen_uu_menu()


# API for "nbis task"
@app.route('/api/nbis/')
def nbis_list_entities():
    return jsonify({'entities': ['restaurant']})


@app.route('/api/nbis/restaurant/')
@cache.cached(timeout=3600)
def nbis_api_list_restaurants():
    return jsonify({'restaurants': main.list_restaurants()})


@app.route('/api/nbis/restaurant/<name>/')
@cache.cached(timeout=3600)
def nbis_api_get_restaurant(name):
    data = main.get_restaurant(name)
    if not data:
        abort(404)
    data['menu'] = [{'dish': entry} for entry in data['menu']]
    return jsonify({'restaurant': data})
