from flask import (
    Blueprint,
    redirect,
    request,
    render_template,
    send_from_directory,
)
from .config import *
from .utils import cut_body, use_template

import requests


app = Blueprint("news", __name__, url_prefix="/actualites")

get_category = {
    "vaovao": {"content": "Vaovao", "display": "Vaovao"},
    "nationale": {"content": "Nationale", "display": "Nationale"},
    "internationale": {
        "content": "Internationale",
        "display": "Internationale",
    },
    "economie": {"content": "Economie", "display": "Economie"},
    "sport": {"content": "Sports", "display": "Sports"},
    "culture": {"content": "Culture", "display": "Culture"},
    "gasy-winner": {"content": "GasyWinner", "display": "Gasy Winner"},
    "sante-medecine": {"content": "sante", "display": "Medecine et santé"},
}


@app.route("/")
@use_template("actualites.html")
def news():
    result = requests.get(
        url=f"{STRAPI_API_URL}/actualites",
        params={
            "populate": "images",
            "sort": "id:desc",
            "pagination[pageSize]": 9,
            "pagination[page]": request.args.get("page", 1),
            "pagination[withCount]": 1,
        },
        headers=STRAPI_API_AUTH_TOKEN,
    )
    return {"result": result.json(), "page": request.args.get("page", 1)}


@app.route("/<category>")
@use_template("category.html")
def category_actuality(category):
    result = requests.get(
        url=f"{STRAPI_API_URL}/actualites",
        params={
            "populate": "images",
            "sort": "id:desc",
            "filters[category][$eq]": get_category[category]["content"],
            "pagination[pageSize]": 9,
            "pagination[page]": request.args.get("page", 1),
            "pagination[withCount]": 1,
        },
        headers=STRAPI_API_AUTH_TOKEN,
    )
    return {
        "category": get_category[category]["display"],
        "result": result.json(),
        "page": request.args.get("page", 1),
        "type": "Actualités",
    }
