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

@app.route('/comic/<int:id>')
def comic(id):
    info = requests_session.get(f'https://xkcd.com/{id}/info.0.json').json()
    return flask.render_template('comic.html',
                                 info=info)
