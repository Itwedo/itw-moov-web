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
    "gastronomie": {"cms": "Gastronomie", "display": "Gastronomie"},
    "tourisme-voyage": {
        "cms": "Tourisme & Voyage",
        "display": "Tourisme & Voyage",
    },
    "education-emploi": {
        "cms": "Education & Emploi",
        "display": "Education & Emploi",
    },
    "sante-bien-etre": {
        "cms": "Santé & Bien-être",
        "display": "Santé & Bien-être",
    },
    "famille": {"cms": "Famille", "display": "Famille"},
    "maison-jardin": {
        "cms": "Maison & Jardin",
        "display": "Maison & Jardin",
    },
    "people": {"cms": "People", "display": "People"},
    "connected-life": {"cms": "High Tech", "display": "HighTech"},
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
            "filters[Type][$eq]": "Tendance",
            "pagination[pageSize]": 18,
            "pagination[page]": request.args.get("page", 1),
            "pagination[withCount]": 1,
        },
        headers=STRAPI_API_AUTH_TOKEN,
    )

    people = requests.get(
        url=f"{STRAPI_API_URL}/actualites",
        params={
            "populate": "images",
            "sort": "id:desc",
            "filters[Type][$eq]": "Tendance",
            "filters[category][$eq]": "People",
            "pagination[pageSize]": 4,
            "pagination[page]": request.args.get("page", 1),
            "pagination[withCount]": 1,
        },
        headers=STRAPI_API_AUTH_TOKEN,
    )

    hightech = requests.get(
        url=f"{STRAPI_API_URL}/actualites",
        params={
            "populate": "images",
            "sort": "id:desc",
            "filters[Type][$eq]": "Tendance",
            "filters[category][$eq]": "High Tech",
            "pagination[pageSize]": 3,
            "pagination[page]": request.args.get("page", 1),
            "pagination[withCount]": 1,
        },
        headers=STRAPI_API_AUTH_TOKEN,
    )
    data = {
        "magazines": result.json()["data"],
        "people": people.json()["data"],
        "hightech": hightech.json()["data"],
    }
    return {"result": data, "page": request.args.get("page", 1)}


@app.route("/<category>")
@use_template("category.html")
def category_magazines(category):
    result = requests.get(
        url=f"{STRAPI_API_URL}/actualites",
        params={
            "populate": "images",
            "sort": "id:desc",
            "filters[Type][$eq]": "Tendance",
            "filters[category][$eq]": get_category[category]["cms"],
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
        "type": "Tendances",
    }
