from datetime import datetime, date
from flask import (
    Blueprint,
    redirect,
    request,
    render_template,
    send_from_directory,
)
from .config import *

import requests


app = Blueprint("search", __name__, url_prefix="/recherche")


@app.route("/")
def recherche():
    ads = requests.get(
        url=f"{STRAPI_API_URL}/ads",
        params={"populate": "image"},
        headers=STRAPI_API_AUTH_TOKEN,
    )
    ads = {
        ad["attributes"]["location"]: ad["attributes"]["image"]["data"]["attributes"][
            "url"
        ]
        for ad in ads.json()["data"]
    }
    result = requests.get(
        url=f"{STRAPI_API_URL}/actualites",
        params={
            "populate": "images",
            "sort": "id:desc",
            "filters[title][$containsi]": request.args.get("query", ""),
            "pagination[pageSize]": 8,
            "pagination[page]": request.args.get("page", 1),
            "pagination[withCount]": 1,
        },
        headers=STRAPI_API_AUTH_TOKEN,
    )

    regular = requests.get(
        url=f"{STRAPI_API_URL}/actualites",
        params={"populate": "images", "sort": "id:desc", "pagination[limit]": 100},
        headers=STRAPI_API_AUTH_TOKEN,
    )

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
        CMS_URL=STRAPI_PUBLIC_URL,
        ads=ads,
    )
