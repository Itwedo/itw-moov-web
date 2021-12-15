from os import path
from pathlib import Path

import requests
from flask import Flask, render_template, send_from_directory


app = Flask(__name__)


CMS_URL = "https://moov-cms.sudo.mg"
AUTH = {"Authorization": "Bearer 1bc6439b946fd03c02a0b319924d49459a05c4763372d0ad5683a3fad3fdb8f17822dbcffc7507078dc337bd01cda5992c8197fe99b795f6374a1c85909bbdfbc4a6cb6fd652049c899034ae4a3410951721433910106ff9f6647cb137b70a3f91740dba3924a57b25a807adc68f28e4c58d3c0b3d06eda16dee9344685dd58c"}


@app.route("/")
def hello_world():
    response = requests.get(f"{CMS_URL}/api/actualites", params={'populate': 'images'}, headers=AUTH)
    return render_template("index.html", actualites=response.json(), CMS_URL=CMS_URL)


@app.route('/assets/<path:filename>')
def serve_assets(filename):
    return send_from_directory(Path() / "assets/", filename)
