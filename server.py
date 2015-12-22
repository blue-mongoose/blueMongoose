import os
from flask import Flask, render_template, send_from_directory, jsonify
from flask.ext.sqlalchemy import SQLAlchemy

# Initilization
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

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
    return render_template('index.html')

@app.route("/api/test/", methods=['GET'])
def test():
    return jsonify({"msg":"hello world"})

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
