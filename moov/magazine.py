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
        headers=STRAPI_API_AUTH_TOKEN_BEARER,
    )

    rubriques = requests.get(
        url=f"{STRAPI_API_URL}/magazine",
        params={
            'populate':'categorie.rubrique'
        },
        headers=STRAPI_API_AUTH_TOKEN_BEARER,
    )
    categories_news =[]
    for rubrique in rubriques.json()['data']['attributes']['categorie']:
        rubrique=rubrique['rubrique']['data']['attributes']
        categories_news.append({"rubrique" : rubrique,"articles" : get_news_by_rubrique(rubrique,4,1,request)})

    data = {
        "magazines": result.json()["data"],
        "category_1": categories_news[0],
        "category_2": categories_news[1],
        "category_3": categories_news[2],
        "category_4": categories_news[3]
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
        headers=STRAPI_API_AUTH_TOKEN_BEARER,
    )
    return {
        "category": get_category_display(category),
        "result": result.json(),
        "page": request.args.get("page", 1),
        "type": {"name": "Tendances", "slug":"tendance"},
    }


def get_news_by_rubrique(rubrique,article_per_page,page_count,request):
    return requests.get(
        url=f"{STRAPI_API_URL}/actualites",
        params={
            "populate": ["images","rubrique"],
            "sort": "id:desc",
            "filters[rubrique][type][$eq]": rubrique['type'],
            "filters[rubrique][slug][$eq]": rubrique['slug'],
            "pagination[pageSize]": article_per_page,
            "pagination[page]": request.args.get("page", 1),
            "pagination[withCount]": page_count,
        },
        headers=STRAPI_API_AUTH_TOKEN_BEARER,
    ).json()["data"]

