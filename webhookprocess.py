from flask import Flask, jsonify
import os
from flask import send_from_directory

app = Flask(__name__)

"""
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/favicon.png')
"""
@app.route('/')
@app.route('/homepage')
def home():
    return "Hello World Success changed"

if __name__ == "__main__":
    app.secret_key = 'ItIsASecret'
    app.debug = True
    app.run()