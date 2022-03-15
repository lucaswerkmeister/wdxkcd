import flask
import mwapi
import requests

app = flask.Flask(__name__)

user_agent = 'wdxkcd (wdxkcd@lucaswerkmeister.de, https://github.com/lucaswerkmeister/wdxkcd)'

requests_session = requests.Session()
requests_session.headers.update({
    'Accept': 'application/json',
    'User-Agent': user_agent,
})

api_session = mwapi.Session('https://www.wikidata.org',
                            user_agent=user_agent)

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/comic/Q<int:id>')
def comic(id):
    item_id = f'Q{id}'
    item_response = api_session.get(action='wbgetentities',
                                    ids=[item_id],
                                    props=['claims'])
    item = item_response['entities'][item_id]
    issue = item['claims']['P433'][0]['mainsnak']['datavalue']['value']

    depicted_item_ids = []
    for statement in item['claims'].get('P180', []):
        depicted_item_id = statement['mainsnak']['datavalue']['value']['id']
        depicted_item_ids.append(depicted_item_id)

    labels_response = api_session.get(action='wbgetentities',
                                      ids=depicted_item_ids,  # TODO split if >50 depicted_item_ids
                                      props=['labels'],
                                      languages=['en'],
                                      languagefallback=1)
    labels = {}
    for entity_id, entity in labels_response['entities'].items():
        labels[entity_id] = entity['labels']['en']['value']

    info = requests_session.get(f'https://xkcd.com/{issue}/info.0.json').json()

    return flask.render_template('comic.html',
                                 info=info,
                                 depicted_item_ids=depicted_item_ids,
                                 labels=labels)
