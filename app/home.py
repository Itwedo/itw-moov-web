from datetime import datetime, date
from flask import (
    Blueprint,
    redirect,
    request,
    render_template,
    send_from_directory,
)
from .config import *
from .base import get_ads, get_currency

import requests


app = Blueprint("home", __name__, url_prefix="/")


@app.route("/")
def home():
    ads = get_ads()
    currency = get_currency()
    spotlights = requests.get(
        url=f"{STRAPI_API_URL}/actualites",
        params={
            "populate": "images",
            "sort": "id:desc",
            "filters[spotlight][$eq]": "true",
            "filters[Type][$eq]": "Actualite",
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
            "populate": "images",
            "sort": "id:desc",
            "filters[spotlight][$eq]": "true",
            "filters[Type][$eq]": "Tendance",
            "pagination[limit]": 1,
        },
        headers=STRAPI_API_AUTH_TOKEN,
    )
    news = requests.get(
        url=f"{STRAPI_API_URL}/actualites",
        params={
            "populate": "images",
            "sort": "id:desc",
            "filters[source][$eq]": "moov",
            "pagination[limit]": 100,
        },
        headers=STRAPI_API_AUTH_TOKEN,
    )

    data = {
        "today": datetime.now().strftime("%A, %d %B %Y"),
        "spotlights": [
            # each spotligh needs an image, an id, a title, createdAt, head
            {
                "id": item["id"],
                "title": item["attributes"]["title"],
                "createdAt": item["attributes"]["createdAt"],
                "head": item["attributes"]["head"],
                "images": item["attributes"]["images"]["data"],
            }
            for item in spotlights.json()["data"]
        ],
        "flashes": [
            {
                "head": item["attributes"]["head"],
                "createdAt": item["attributes"]["createdAt"],
                "id": item["id"],
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
            if item["attributes"]["images"]["data"]
        ],
    }
    return render_template(
        "index.html",
        data=data,
        ads=ads,
        CMS_URL=STRAPI_PUBLIC_URL,
        currency=currency,
    )
