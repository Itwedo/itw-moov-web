from flask import (
    Blueprint,
    redirect,
    request,
    render_template,
    send_from_directory,
)

from .utils import use_template
from .config import *

import requests

get_category = {
    "gastronomie": {"content": ["Gastronomie"], "display": "Gastronomie"},
    "tourisme-voyage": {
        "content": ["Tourisme", "Voyage"],
        "display": "Tourisme & Voyage",
    },
    "education-emploi": {
        "content": ["Education", "Emploi"],
        "display": "Education & Emploi",
    },
    "sante-bien-etre": {"content": ["Sante"], "display": "Santé"},
    "famille": {"content": ["Famille"], "display": "Famille"},
    "maison-jardin": {
        "content": ["Maison", "Jardin"],
        "display": "Maison & Jardin",
    },
    "people": {"content": ["People"], "display": "People"},
    "connected-life": {"content": ["HighTech"], "display": "HighTech"},
}

app = Blueprint("magazine", __name__, url_prefix="/magazine")


@app.route("/")
@use_template("tendance.html")
def magazine():
    # 18/page
    result = requests.get(
        url=f"{STRAPI_API_URL}/actualites",
        params={
            "populate": "images",
            "sort": "id:desc",
            "pagination[pageSize]": 18,
            "pagination[page]": request.args.get("page", 1),
            "pagination[withCount]": 1,
        },
        headers=STRAPI_API_AUTH_TOKEN,
    )
    return {'result': result.json(), 'page': request.args.get("page", 1)}


@app.route("/<category>")
@use_template("category.html")
def category_magazines(category):
    result = requests.get(
        url=f"{STRAPI_API_URL}/actualites",
        params={
            "populate": "images",
            "sort": "id:desc",
            "filters[Type][$eq]": "Tendance",
            "filters[category][$in]": get_category[category]["content"],
            "pagination[pageSize]": 10,
            "pagination[page]": request.args.get("page", 1),
            "pagination[withCount]": 1,
        },
        headers=STRAPI_API_AUTH_TOKEN,
    )
    return {
        'category': get_category[category]["display"],
        'result': result.json(),
        'page': request.args.get("page", 1),
    }
