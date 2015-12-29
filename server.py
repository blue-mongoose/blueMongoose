import os
from flask import Flask, render_template, send_from_directory, jsonify, redirect, url_for, request
from flask.ext.sqlalchemy import SQLAlchemy
import uuid

from dungeon import dungeon

# Initilization
APPLICATION_CONFIG = os.environ.get('BLUE_MONGOOSE_SETTINGS')

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

class classes(db.Model):
    Name = db.Column(db.String(255), primary_key=True)
    Requirement = db.Column(db.String(255))
    AttkBonus = db.Column(db.Integer)
    SpeedBonus = db.Column(db.Integer)
    HealthBonus = db.Column(db.Integer)
    URLDescription = db.Column(db.String(255))
    URLImage = db.Column(db.String(255))

    def __init__(self, Name, Requirement, AttkBonus, SpeedBonus, HealthBonus, URLDescription, URLImage):
        self.Name = Name
        self.Requirement = Requirement
        self.AttkBonus = AttkBonus
        self.SpeedBonus = SpeedBonus
        self.HealthBonus = HealthBonus
        self.URLDescription = URLDescription
        self.URLImage = URLImage

class buildings(db.Model):
    Name = db.Column(db.String(255), primary_key=True)
    AttkBonus = db.Column(db.Integer)
    SpeedBonus = db.Column(db.Integer)
    HealthBonus = db.Column(db.Integer)
    URLDescription = db.Column(db.String(255))
    URLImage = db.Column(db.String(255))

    def __init__(self, Name, Requirement, AttkBonus, SpeedBonus, HealthBonus, URLDescription, URLImage):
        self.Name = Name
        self.Requirement = Requirement
        self.AttkBonus = AttkBonus
        self.SpeedBonus = SpeedBonus
        self.HealthBonus = HealthBonus
        self.URLDescription = URLDescription
        self.URLImage = URLImage

class items(db.Model):
    Name = db.Column(db.String(255), primary_key=True)
    Requirement = db.Column(db.String(255))
    AttkBonus = db.Column(db.Integer)
    SpeedBonus = db.Column(db.Integer)
    HealthBonus = db.Column(db.Integer)
    URLDescription = db.Column(db.String(255))
    URLImage = db.Column(db.String(255))

    def __init__(self, Name, Requirement, AttkBonus, SpeedBonus, HealthBonus, URLDescription, URLImage):
        self.Name = Name
        self.Requirement = Requirement
        self.AttkBonus = AttkBonus
        self.SpeedBonus = SpeedBonus
        self.HealthBonus = HealthBonus
        self.URLDescription = URLDescription
        self.URLImage = URLImage


class enemies(db.Model):
    Name = db.Column(db.String(255), primary_key=True)
    Attk = db.Column(db.Integer)
    Speed = db.Column(db.Integer)
    Health = db.Column(db.Integer)
    URLDescription = db.Column(db.String(255))
    URLImage = db.Column(db.String(255))

    def __init__(self, Name, Requirement, AttkBonus, SpeedBonus, HealthBonus, URLDescription, URLImage):
        self.Name = Name
        self.Attk = AttkBonus
        self.Speed = SpeedBonus
        self.Health = HealthBonus
        self.URLDescription = URLDescription
        self.URLImage = URLImage

class moves(db.Model):
    Name = db.Column(db.String(255), primary_key=True)
    Attk = db.Column(db.Integer)
    Speed = db.Column(db.Integer)
    Health = db.Column(db.Integer)
    URLDescription = db.Column(db.String(255))

    def __init__(self, Name, Requirement, AttkBonus, SpeedBonus, HealthBonus, URLDescription, URLImage):
        self.Name = Name
        self.Attk = AttkBonus
        self.Speed = SpeedBonus
        self.Health = HealthBonus
        self.URLDescription = URLDescription

class bosses(db.Model):
    Name = db.Column(db.String(255), primary_key=True)
    Attk = db.Column(db.Integer)
    Speed = db.Column(db.Integer)
    Health = db.Column(db.Integer)
    URLDescription = db.Column(db.String(255))
    URLImage = db.Column(db.String(255))

    def __init__(self, Name, Requirement, AttkBonus, SpeedBonus, HealthBonus, URLDescription, URLImage):
        self.Name = Name
        self.Attk = AttkBonus
        self.Speed = SpeedBonus
        self.Health = HealthBonus
        self.URLDescription = URLDescription
        self.URLImage = URLImage

class equipment(db.Model):
    Name = db.Column(db.String(255), primary_key=True)
    Attk = db.Column(db.Integer)
    Speed = db.Column(db.Integer)
    Health = db.Column(db.Integer)
    URLDescription = db.Column(db.String(255))
    URLImage = db.Column(db.String(255))

    def __init__(self, Name, Requirement, AttkBonus, SpeedBonus, HealthBonus, URLDescription, URLImage):
        self.Name = Name
        self.Attk = AttkBonus
        self.Speed = SpeedBonus
        self.Health = HealthBonus
        self.URLDescription = URLDescription
        self.URLImage = URLImage

class dungeon(db.Model):
    Name = db.Column(db.String(255), primary_key=True)
    Attk = db.Column(db.Integer)
    Speed = db.Column(db.Integer)
    Health = db.Column(db.Integer)
    URLDescription = db.Column(db.String(255))
    URLImage = db.Column(db.String(255))

    def __init__(self, Name, Requirement, AttkBonus, SpeedBonus, HealthBonus, URLDescription, URLImage):
        self.Name = Name
        self.Attk = AttkBonus
        self.Speed = SpeedBonus
        self.Health = HealthBonus
        self.URLDescription = URLDescription
        self.URLImage = URLImage

# mapping tables

class enemies_carry_items(db.Model):
    Enemy = db.Column(db.String(255), primary_key=True)
    Item = db.Column(db.String(255))

    def __init__(self, Enemy, Item):
        self.Enemy = Enemy
        self.Item = Item


# class dungeons_have_bosses(db.Model):
#     Enemy = db.Column(db.String(255), primary_key=True)
#     Item = db.Column(db.String(255))

#     def __init__(self, Enemy, Item):
#         self.Enemy = Enemy
#         self.Item = Item
# class characters(db.Model):
#     CharID = db.Column(db.Integer,



###############
# Controllers #
###############

@app.route("/api/test/", methods=['GET'])
def test():
    return jsonify({"msg":"hello world"})

# Homepage

@app.route("/")
def index():
    return render_template('index.html')


# Login

"""
Flow is as follows:

api/login -> Github -> api/authorize -> /

- Need to generate a state UUID in api/login
- Send to Github
- Github should send it back
- Need to verify in api/authorize that the state in the URL matches the state
generated in api/login
"""

# @app.route('/api/login', methods=['GET'])
# def api_login():
#     BASE_URL = 'https://github.com/login/oauth/authorize'
#     state = str(uuid.uuid4())
#     params = { 'client_id': GITHUB_CLIENT_ID
#              , 'redirect_uri': 'https://blue-mongoose.herokuapp.com/api/authorize'
#              , 'state': state
#              }
#     param_pairs = zip(params.keys(), params.values())
#     url = build_url(BASE_URL, [k + '=' + v for (k, v) in param_pairs])
#     return redirect(url)

# @app.route('/api/authorize', methods=['GET'])
# def authorize():
#     state = request.args.get('state', '')
#     code = request.args.get('code', '')
#     print(state)
#     print(code)
#     return redirect('/')


# Dungeon

@app.route("/api/dungeon/", methods=['GET'])
def make_dungeon():
    cur_events, cur_dungeon = dungeon.gen_dungeon()
    return_val = {"dungeon": cur_dungeon}
    for key, val in cur_events:
        return_val[key] = val
    return jsonify(return_val)


# Players

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
