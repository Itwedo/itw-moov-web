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
import locale

app = Blueprint("home", __name__, url_prefix="/")


@app.route("/")
@use_template("index.html")
def home():
    spotlights = requests.get(
        url=f"{STRAPI_API_URL}/actualites",
        params={
            "populate": ["images","rubrique"],
            "sort": "id:desc",
            "filters[spotlight][$eq]": "true",
            "filters[rubrique][type][$eq]" : "Actualite",
        },
        headers=STRAPI_API_AUTH_TOKEN,
    )
    flashes_0 = requests.get(
        url=f"{STRAPI_API_URL}/flash-news",
        params={"populate": "images", "sort": "id:desc"},
        headers=STRAPI_API_AUTH_TOKEN,
    )
    flashes_1 = requests.get(
        url=f"{STRAPI_API_URL}/actualites",
        params={
            "populate": "images",
            "sort": "id:desc",
            "filters[flash][$eq]": "true",
        },
        headers=STRAPI_API_AUTH_TOKEN,
    )
    flashes = flashes_0.json()["data"] + flashes_1.json()["data"]
    flashes = sorted(
        flashes, key=lambda x: x["attributes"]["publishedAt"], reverse=True
    )
    magazine = requests.get(
        url=f"{STRAPI_API_URL}/actualites",
        params={
            "populate": ["images","rubrique"],
            "sort": "id:desc",
            "filters[spotlight][$eq]": "true",
            "filters[rubrique][type][$eq]": "Tendance",
            "pagination[limit]": 5,
        },
        headers=STRAPI_API_AUTH_TOKEN,
    )
    news = requests.get(
        url=f"{STRAPI_API_URL}/actualites",
        params={
            "populate": ["images","rubrique"],
            "sort": "id:desc",
            "filters[rubrique][type][$eq]": "Actualite",
            "pagination[limit]": 10,
        },
        headers=STRAPI_API_AUTH_TOKEN,
    )
    magazines = requests.get(
        url=f"{STRAPI_API_URL}/actualites",
        params={
            "populate": ["images","rubrique"],
            "sort": "id:desc",
            "filters[rubrique][type][$eq]": "Tendance",
            "pagination[limit]": 20,
        },
        headers=STRAPI_API_AUTH_TOKEN,
    )

    locale.setlocale(locale.LC_TIME,'fr_FR.UTF-8')
    data = {
        "today": datetime.now().strftime("%A, %d %B %Y").title(),
        "spotlights": [
            # each spotligh needs an image, an id, a title, createdAt, head
            {
                "id": item["id"],
                "title": item["attributes"]["title"],
                "createdAt": item["attributes"]["date"],
                "head": item["attributes"]["head"],
                "images": item["attributes"]["images"]["data"],
                "category": item["attributes"]["rubrique"]["data"]["attributes"]["name"],
                "slugId": item["attributes"]["slugId"],
                "copyright": item["attributes"]["copyright"]
            }
            for item in spotlights.json()["data"]
        ],
        "flashes": [
            {
                "head": item["attributes"]["head"],
                "createdAt": item["attributes"]["date"],
                "id": item["id"],
                "article": True if item["attributes"].__contains__('slugId') else False,
                "slugId": item["attributes"]["slugId"] if item["attributes"].__contains__('slugId') else ""
            }
            for item in flashes[:20]
        ],
        "news": [
            item
            for item in news.json()["data"]
            if item["attributes"]["images"]["data"]
        ],
        "magazine": [
            item
            for item in magazine.json()["data"]
            if item["attributes"]["images"]["data"][0]["attributes"]["width"]
        ],
        "magazines": [
            item
            for item in magazines.json()["data"]
            if item["attributes"]["images"]["data"]
        ],
    }
    return {"data": data}
