import os
from flask import Flask, render_template, send_from_directory, jsonify, request, abort
from flask.ext.sqlalchemy import SQLAlchemy

from dungeon import dungeon
from cards import cards

# Initilization
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

# tables
class players(db.Model):
    PID = db.Column(db.Integer, primary_key=True)
    NAME = db.Column(db.String(255))

    def __init__(self, PID, name):
        self.PID = PID
        self.NAME = name

    def __repr__(self):
        return str('Name ' + self.NAME)

# Controllers
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/api/test/", methods=['GET'])
def test():
    all_args = request.args.lists()
    return jsonify(all_args)

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
    print(name)
    try:
        return jsonify(cards.all_cards()[name.lower()])
    except KeyError:
        abort(400)

@app.route("/api/cards/<card_type>/", methods=['GET'])
def card_types(card_type):
    name = request.args.get("name")
    try:
        return jsonify(eval("cards." + card_type)()[name.lower()])
    except (KeyError, AttributeError):
        abort(400)

# @app.route("/api/cards/enemies/", methods=['GET'])
# def enemies_cards():
#     name = request.args.get("name")
#     print(name)
#     try:
#         return jsonify(cards.enemies()[name.lower()])
#     except KeyError:
#         abort(400)

# @app.route("/api/players/<username>", methods=['POST'])
# def post_api_players(username):

@app.route("/api/players/", methods=['GET'])
def api_players():
    # print(players.query.all())
    return jsonify({"players": str(players.query.all())})

# @app.route("/api/equipment/", methods=['GET'])
# def equipment():
#     return jsonify({"current_equipment":

# Launch to Heroku
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
