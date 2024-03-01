from datetime import datetime, date
from flask import (
    Blueprint,
    redirect,
    request,
    render_template,
    send_from_directory,
)
from .config import *
from .utils import use_template

import requests


app = Blueprint("search", __name__, url_prefix="/recherche")


@app.route("/")
@use_template("search.html")
def search():
    result = requests.get(
        url=f"{STRAPI_API_URL}/actualites",
        params={
            "populate": ["images","rubrique"],
            "sort": "id:desc",
            "filters[title][$containsi]": request.args.get("query", ""),
            "pagination[pageSize]": 8,
            "pagination[page]": request.args.get("page", 1),
            "pagination[withCount]": 1,
        },
        headers=STRAPI_API_AUTH_TOKEN_BEARER,
    )
    regular = requests.get(
        url=f"{STRAPI_API_URL}/actualites",
        params={
            "populate": ["images","rubrique"],
            "sort": "id:desc",
            "pagination[limit]": 100,
        },
        headers=STRAPI_API_AUTH_TOKEN_BEARER,
    )

    actualites = {"data": []}

    for data in regular.json()["data"]:
        if data["attributes"]["images"]["data"] is not None:
            actualites["data"].append(data)

    return {
        'result': result.json(),
        'actualites': actualites,
        'query': request.args.get("query", ""),
        'page': request.args.get("page", 1),
    }
