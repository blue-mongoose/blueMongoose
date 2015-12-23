import os
from flask import Flask, render_template, send_from_directory, jsonify, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
import uuid

from dungeon import dungeon

# Initilization
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

try:
    GITHUB_CLIENT_ID = os.environ['BM_GITHUB_CLIENT_ID']
except KeyError:
    GITHUB_CLIENT_ID = os.environ['GITHUB_CLIENT_ID']

def intersperse(iterable, delimiter):
    it = iter(iterable)
    yield next(it)
    for x in it:
        yield delimiter
        yield x

def build_url(base_url, params):
    url = base_url + '?' + ''.join(list(intersperse(params, '&')))
    if ' ' in url:
        return url.replace(' ', '+')
    else:
        return url


class players(db.Model):
    PID = db.Column(db.Integer, primary_key=True)
    NAME = db.Column(db.String(255))

    def __init__(self, PID, name):
        self.PID = PID
        self.NAME = name

    def __repr__(self):
        return str('Name ' + self.NAME)

# class characters(db.Model):
#     CharID = db.Column(db.Integer,

# Controllers
@app.route("/")
def index():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    return render_template('index.html')

@app.route("/api/test/", methods=['GET'])
def test():
    return jsonify({"msg":"hello world"})

@app.route("/api/dungeon/", methods=['GET'])
def make_dungeon():
    cur_events, cur_dungeon = dungeon.gen_dungeon()
    return_val = {"dungeon": cur_dungeon}
    for key, val in cur_events:
        return_val[key] = val
    return jsonify(return_val)

# @app.route("/api/players/<username>", methods=['POST'])
# def post_api_players(username):

@app.route("/api/players/", methods=['GET'])
def api_players():
    # print(players.query.all())
    return jsonify({"players": str(players.query.all())})

# @app.route("/api/equipment/", methods=['GET'])
# def equipment():
#     return jsonify({"current_equipment":

# INCOMPLETE -- Need to do second half of the handshake
@app.route('/api/login', methods=['GET'])
def api_login():
    BASE_URL = 'https://github.com/login/oauth/authorize'
    params = { 'client_id': GITHUB_CLIENT_ID
             , 'redirect_uri': 'https://blue-mongoose.herokuapp.com/dashboard'
             , 'state': str(uuid.uuid4())
             }
    param_pairs = zip(params.keys(), params.values())
    url = build_url(BASE_URL, [k + '=' + v for (k, v) in param_pairs])
    return redirect(url)


# Launch to Heroku
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
