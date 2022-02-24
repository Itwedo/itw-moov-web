from pathlib import Path
from datetime import datetime, date

from flask import (
    Flask,
    request,
    render_template,
    send_from_directory
)

import os
import requests
import markdown2
from bs4 import BeautifulSoup


app = Flask(__name__)


STRAPI_API_URL = os.environ.get('STRAPI_API_URL', 'http://localhost:2337/api')
STRAPI_API_AUTH_TOKEN = {'Authorization': f'Bearer {os.environ.get("STRAPI_API_AUTH_TOKEN", "")}'}
CMS_URL = STRAPI_API_URL.replace(f'/{STRAPI_API_URL.split("/")[-1]}', '')


@app.route("/")
def home():
    spotlighted = requests.get(
        url=f"{STRAPI_API_URL}/actualites",
        params={'populate': 'images', 'sort': "id:desc", "filters[spotlight][$eq]": "true" },
        headers=STRAPI_API_AUTH_TOKEN)
    flashed = requests.get(
        url=f"{STRAPI_API_URL}/actualites",
        params={'populate': 'images', 'sort': "id:desc", "filters[flash][$eq]": "true" },
        headers=STRAPI_API_AUTH_TOKEN)
    regular = requests.get(
        url=f"{STRAPI_API_URL}/actualites",
        params={'populate': 'images', 'sort': "id:desc", "pagination[limit]": 100},
        headers=STRAPI_API_AUTH_TOKEN)

    actualites = {"data": []}

    for data in regular.json()["data"]:
        if data["attributes"]["images"]["data"] is not None:
            actualites["data"].append(data)

    return render_template(
        "index.html",
        actualites=actualites,
        actu_spotlighted=spotlighted.json(),
        actu_flashed=flashed.json(),
        CMS_URL=CMS_URL)


@app.route("/actualite/<id>")
def actualite(id):
    response = requests.get(
        url=f"{STRAPI_API_URL}/actualites/{id}",
        params={'populate': 'images', 'sort': "id:desc", "pagination[limit]": 100},
        headers=STRAPI_API_AUTH_TOKEN)

    body = cut_body(response.json()["data"]["attributes"]["body"])

    regular = requests.get(
        url=f"{STRAPI_API_URL}/actualites",
        params={'populate': 'images', 'sort': "id:desc", "pagination[limit]": 100},
        headers=STRAPI_API_AUTH_TOKEN)

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


@app.route("/category")
def category():
    # 10/page
    result = requests.get(
        url=f"{STRAPI_API_URL}/actualites",
        params={
            'populate': 'images',
            'sort': "id:desc",
            "pagination[pageSize]": 10,
            "pagination[page]": request.args.get("page", 1),
            "pagination[withCount]": 1},
        headers=STRAPI_API_AUTH_TOKEN)

    return render_template(
        "category.html",
        result=result.json(),
        page=request.args.get("page", 1),
        CMS_URL=CMS_URL)


@app.route("/tendance")
def tendance():
    # 18/page
    result = requests.get(
        url=f"{STRAPI_API_URL}/actualites",
        params={
            'populate': 'images',
            'sort': "id:desc",
            "pagination[pageSize]": 18,
            "pagination[page]": request.args.get("page", 1),
            "pagination[withCount]": 1},
        headers=STRAPI_API_AUTH_TOKEN)

    return render_template(
        "tendance.html",
        result=result.json(),
        page=request.args.get("page", 1),
        CMS_URL=CMS_URL)


@app.route("/recherche")
def recherche():
    result = requests.get(
        url=f"{STRAPI_API_URL}/actualites",
        params={
            'populate': 'images',
            'sort': "id:desc",
            'filters[title][$containsi]': request.args.get("query", ""),
            "pagination[pageSize]": 8,
            "pagination[page]": request.args.get("page", 1),
            "pagination[withCount]": 1},
        headers=STRAPI_API_AUTH_TOKEN)

    regular = requests.get(
        url=f"{STRAPI_API_URL}/actualites",
        params={'populate': 'images', 'sort': "id:desc", "pagination[limit]": 100},
        headers=STRAPI_API_AUTH_TOKEN)

    actualites = {"data": []}

    for data in regular.json()["data"]:
        if data["attributes"]["images"]["data"] is not None:
            actualites["data"].append(data)

    return render_template(
        "recherche.html",
        result=result.json(),
        actualites=actualites,
        query=request.args.get("query", ""),
        page=request.args.get("page", 1),
        CMS_URL=CMS_URL)


@app.route("/mention.html")
def mention():
    return render_template("mention.html")


@app.route("/contact.html")
def contact():
    return render_template("contact.html")


@app.route("/pharmacie.html")
def pharmacie():
    today = date.today().strftime('%Y-%m-%d')
    todays_month = today.split('-')[1]
    response = requests.get(
        url=f"{STRAPI_API_URL}/allnighters",
        headers=STRAPI_API_AUTH_TOKEN,
        params={
            "filters[$and][0][start][$lte]": today,
            "filters[$and][1][stop][$gte]": today,
            "sort": "start:desc",
            "populate": "drugstore"
        }
    )
    result = response.json()['data']
    start = datetime.strptime(result[0]['attributes']['start'], '%Y-%m-%d').strftime('%d/%m/%Y')
    stop = datetime.strptime(result[0]['attributes']['stop'], '%Y-%m-%d').strftime('%d/%m/%Y')
    return render_template("pharmacie.html", start=start, stop=stop, result=result)


@app.route("/coming_soon.html")
def coming_soon():
    return render_template("coming_soon.html")


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

@app.template_filter('markdown')
def _markdown(s):
    if isinstance(s, str):
        return markdown2.markdown(s, extras=[
            "break-on-newline",
            "cuddled-lists",
            "markdown-in-html",
            "header-ids",
            "strike",
            "target-blank-links",
            "task_list",
        ])
    return ""


def cut_body(text):
    FIRST_LIMIT_CHAR = 1750

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
