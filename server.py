import os
from flask import Flask, render_template, send_from_directory

# Initilization
app = Flask(__name__)


# Controllers
@app.route("/")
def index():
    return render_template('index.html')

# Launch to Heroku
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)