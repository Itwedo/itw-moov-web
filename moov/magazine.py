from flask import (
    Blueprint,
    request,
)

from .utils import use_template,get_category_display
from .config import *

import requests

app = Blueprint("magazine", __name__, url_prefix="/magazines")


@app.route("/")
@use_template("tendance.html")
def magazine():
    # 18/page
    result = requests.get(
        url=f"{STRAPI_API_URL}/actualites",
        params={
            "populate":["images","rubrique"],
            "sort": "id:desc",
            "filters[rubrique][type][$eq]": "Tendance",
            "pagination[pageSize]": 18,
            "pagination[page]": request.args.get("page", 1),
            "pagination[withCount]": 1,
        },
        headers=STRAPI_API_AUTH_TOKEN,
    )

    people = requests.get(
        url=f"{STRAPI_API_URL}/actualites",
        params={
            "populate": ["images","rubrique"],
            "sort": "id:desc",
            "filters[rubrique][type][$eq]": "Tendance",
            "filters[rubrique][slug][$eq]": "people",
            "pagination[pageSize]": 4,
            "pagination[page]": request.args.get("page", 1),
            "pagination[withCount]": 1,
        },
        headers=STRAPI_API_AUTH_TOKEN,
    )

    hightech = requests.get(
        url=f"{STRAPI_API_URL}/actualites",
        params={
            "populate": ["images","rubrique"],
            "sort": "id:desc",
            "filters[rubrique][type][$eq]": "Tendance",
            "filters[rubrique][slug][$eq]": "connected-life",
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
            "populate": ["images","rubrique"],
            "sort": "id:desc",
            "filters[rubrique][type][$eq]": "Tendance",
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
        "type": "Tendances",
    }
