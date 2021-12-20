from datetime import datetime
from pathlib import Path

import requests
from flask import Flask, render_template, send_from_directory
from bs4 import BeautifulSoup

app = Flask(__name__)


CMS_URL = "https://moov-cms.sudo.mg"
# CMS_URL = "http://localhost:2337"
AUTH = {"Authorization": "Bearer 1bc6439b946fd03c02a0b319924d49459a05c4763372d0ad5683a3fad3fdb8f17822dbcffc7507078dc337bd01cda5992c8197fe99b795f6374a1c85909bbdfbc4a6cb6fd652049c899034ae4a3410951721433910106ff9f6647cb137b70a3f91740dba3924a57b25a807adc68f28e4c58d3c0b3d06eda16dee9344685dd58c"}


@app.route("/")
def home():
    spotlighted = requests.get(
        url=f"{CMS_URL}/api/actualites",
        params={'populate': 'images', 'sort': "id:desc", "filters[spotlight][$eq]": "true" },
        headers=AUTH)
    regular = requests.get(
        url=f"{CMS_URL}/api/actualites",
        params={'populate': 'images', 'sort': "id:desc", "pagination[limit]": 100},
        headers=AUTH)

    actualites = {"data": []}

    for data in regular.json()["data"]:
        if data["attributes"]["images"]["data"] is not None:
            actualites["data"].append(data)

    return render_template(
        "index.html",
        actualites=actualites,
        actu_spotlighted=spotlighted.json(),
        CMS_URL=CMS_URL)


@app.route("/actualite/<id>")
def actualite(id):
    response = requests.get(
        url=f"{CMS_URL}/api/actualites/{id}",
        params={'populate': 'images', 'sort': "id:desc", "pagination[limit]": 100},
        headers=AUTH)

    body = cut_body(response.json()["data"]["attributes"]["body"])

    regular = requests.get(
        url=f"{CMS_URL}/api/actualites",
        params={'populate': 'images', 'sort': "id:desc", "pagination[limit]": 100},
        headers=AUTH)

    actualites = {"data": []}

    for data in regular.json()["data"]:
        if data["attributes"]["images"]["data"] is not None:
            actualites["data"].append(data)

    return render_template(
        "actualites.html",
        actualites=actualites,
        news=response.json(),
        body=body,
        CMS_URL=CMS_URL)


@app.route('/assets/<path:filename>')
def serve_assets(filename):
    return send_from_directory(Path() / "assets/", filename)


@app.template_filter('date')
def _date(s):
    if isinstance(s, str):
        return datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%d/%m/%Y")
    return ""

@app.template_filter('time')
def _time(s):
    if isinstance(s, str):
        return datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%H:%M")
    return ""


def cut_body(text):
    FIRST_LIMIT_CHAR = 1750

    if not "<p>" in text:
        return [text]

    # TODO:use beautifulsoup to cut in FIRST_LIMIT_CHAR
    # Get length of traversed node
    first_part = []
    second_part = []
    for child in BeautifulSoup(text, "html.parser"):
        if len("".join([str(tag) for tag in first_part])) >= FIRST_LIMIT_CHAR:
            second_part.append(child)
        else:
            first_part.append(child)

    return (
        "".join([str(tag) for tag in first_part]),
        "".join([str(tag) for tag in second_part ]),
    )
