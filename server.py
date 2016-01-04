import os
from flask import Flask, render_template, send_from_directory, jsonify, redirect, url_for, request, abort
from flask.ext.sqlalchemy import SQLAlchemy
import uuid

import random, string

from dungeon import dungeon
from cards import cards

# Initilization
APPLICATION_CONFIG = os.environ.get('BLUE_MONGOOSE_SETTINGS')

BASE_URL = "http://localhost:5000/"

app = Flask(__name__)
app.config['DEBUG'] = False
app.config['TESTING'] = False

if APPLICATION_CONFIG == 'production':
    app.config['DATABASE_URI'] = os.environ['DATABASE_URL']
    GITHUB_CLIENT_ID = os.environ['GITHUB_CLIENT_ID']
    GITHUB_CLIENT_SECRET = os.environ['GITHUB_CLIENT_SECRET']
elif APPLICATION_CONFIG == 'development':
    app.config['DEBUG'] = True
    app.config['DATABASE_URI'] = os.environ['BLUE_MONGOOSE_DATABASE_URL']
    GITHUB_CLIENT_ID = os.environ['BLUE_MONGOOSE_GITHUB_CLIENT_ID']
    GITHUB_CLIENT_SECRET = os.environ['BLUE_MONGOOSE_GITHUB_CLIENT_SECRET']
elif APPLICATION_CONFIG == 'testing':
    app.config['TESTING'] = True
    app.config['DATABASE_URI'] = os.environ['BLUE_MONGOOSE_DATABASE_URL']
    GITHUB_CLIENT_ID = os.environ['BLUE_MONGOOSE_GITHUB_CLIENT_ID']
    GITHUB_CLIENT_SECRET = os.environ['BLUE_MONGOOSE_GITHUB_CLIENT_SECRET']
else:
    app.config['DEBUG'] = True
    app.config['DATABASE_URI'] = os.environ['BLUE_MONGOOSE_DATABASE_URL']
    GITHUB_CLIENT_ID = os.environ['BLUE_MONGOOSE_GITHUB_CLIENT_ID']
    GITHUB_CLIENT_SECRET = os.environ['BLUE_MONGOOSE_GITHUB_CLIENT_SECRET']

db = SQLAlchemy(app)

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

##########
# Models #
##########

class players(db.Model):
    PID = db.Column(db.Integer, primary_key=True)
    NAME = db.Column(db.String(255))

    def __init__(self, PID, name):
        self.PID = PID
        self.NAME = name

    def __repr__(self):
        return str('Name ' + self.NAME)

@app.route("/api/test/", methods=['GET'])
def test():
    all_args = request.args.lists()
    return jsonify(all_args)

# Homepage

@app.route("/")
def index():
    return render_template('cover.html')

game_dict = {}

@app.route("/api/host/")
def new_game():
    cur_keys = game_dict.keys()
    new_game_id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(5))
    while(new_game_id in cur_keys):
        new_game_id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(5))
    game_dict[new_game_id] = []
    return redirect(BASE_URL + new_game_id)

@app.route("/<gameid>/")
def gamelogin(gameid):
    return render_template('gamelogin.html',
                            gameid=id)

@app.route("/<gameid>/<userid>/")
def userlogin(gameid, userid):
    game_dict[gameid].append(userid)
    return render_template('index.html',
                           gameid=gameid,
                           name=userid)

# Dungeon

@app.route("/api/dungeon/", methods=['GET'])
def make_dungeon():
    terrain = request.args.get("terrain")[0]
    difficulty = int(request.args.get("difficulty")[0])
    cur_events, cur_dungeon = dungeon.gen_dungeon(terrain, difficulty)
    return_val = {"dungeon": cur_dungeon}
    for key, val in cur_events:
        return_val[key] = val
    return jsonify(return_val)

@app.route("/api/cards/", methods=['GET'])
def card():
    name = request.args.get("name")
    if name == None:
        return jsonify(cards.all_cards())
    try:
        return jsonify(cards.all_cards()[name.lower()])
    except KeyError:
        abort(400)

@app.route("/api/cards/<card_type>/", methods=['GET'])
def card_types(card_type):
    name = request.args.get("name")
    if name == None:
        return jsonify(eval("cards." + card_type)())
    try:
        return jsonify(eval("cards." + card_type)()[name.lower()])
    except (KeyError, AttributeError):
        abort(400)

@app.route("/api/players/", methods=['GET'])
def api_players():
    # print(players.query.all())
    return jsonify({"players": str(players.query.all())})

# Launch to Heroku
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
