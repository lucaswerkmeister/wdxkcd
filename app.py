import flask
import requests

app = flask.Flask(__name__)

requests_session = requests.Session()
requests_session.headers.update({
    'Accept': 'application/json',
    'User-Agent': 'wdxkcd (wdxkcd@lucaswerkmeister.de, https://github.com/lucaswerkmeister/wdxkcd)',
})

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/comic/Q<int:id>')
def comic(id):
    item_id = f'Q{id}'
    item_response = requests_session.get(f'https://www.wikidata.org/entity/{item_id}').json()
    item = item_response['entities'][item_id]
    issue = item['claims']['P433'][0]['mainsnak']['datavalue']['value']
    info = requests_session.get(f'https://xkcd.com/{issue}/info.0.json').json()
    return flask.render_template('comic.html',
                                 info=info)
