from flask import (
    Blueprint,
    redirect,
    request,
    render_template,
    send_from_directory,
)
from .config import *
from .utils import cut_body, use_template, get_category_display

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
    "sport": {"content": "Sport", "display": "Sports"},
    "culture": {"content": "Culture", "display": "Culture"},
    "gasy-winner": {"content": "Gasy Winner", "display": "Gasy Winner"},
    "sante-medecine": {
        "content": "Médecine & Santé",
        "display": "Médecine & santé",
    },
    "people": {"content": "People", "display": "People"},
}


@app.route("/")
@use_template("actualites.html")
def news():
    result = requests.get(
        url=f"{STRAPI_API_URL}/actualites",
        params={
            "populate": ["images","rubrique"],
            "sort": "id:desc",
            "filters[rubrique][type][$eq]": "Actualite",
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
    if category == "médecine-et-santé":
        category = "sante-medecine"

    result = requests.get(
        url=f"{STRAPI_API_URL}/actualites",
        params={
            "populate": ["images","rubrique"],
            "sort": "id:desc",
            "filters[rubrique][slug][$eq]": category,
            "pagination[pageSize]": 9,
            "pagination[page]": request.args.get("page", 1),
            "pagination[withCount]": 1,
        },
        headers=STRAPI_API_AUTH_TOKEN,
    )
    return {
        "category": get_category_display(category),
        "result": result.json(),
        "page": request.args.get("page", 1),
        "type": "Actualités",
    }
