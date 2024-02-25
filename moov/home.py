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
    spotlights_response = requests.get(
        url=f"{STRAPI_API_URL}/actualites",
        params={
            "populate": ["images","category"],
            "sort": "id:desc",
            "filters[spotlight][$eq]": "true",
            "filters[category][type][$eq]" : "Actualite",
        },
        headers=STRAPI_API_AUTH_TOKEN,
    )
    spotlights = []
    if spotlights_response.ok:
        spotlights_data = spotlights_response.json()["data"]
        spotlights = [
            {
                "id": item["id"],
                "title": item["attributes"]["title"],
                "createdAt": item["attributes"]["date"],
                "head": item["attributes"]["head"],
                "images": item["attributes"]["images"]["data"],
                "category": item["attributes"]["category"]["data"]["attributes"]["name"],
                "slugId": item["attributes"]["slugId"] if item["attributes"]["slugId"] else "article",
                "copyright": item["attributes"]["copyright"]
            }
            for item in spotlights_data
        ]
    flashes_0_response = requests.get(
        url=f"{STRAPI_API_URL}/flash-news",
        params={"populate": "images", "sort": "id:desc"},
        headers=STRAPI_API_AUTH_TOKEN,
    )
    flashes_0 = []
    if flashes_0_response.ok:
        flashes_0 = flashes_0_response.json()["data"]
    flashes_1_response = requests.get(
        url=f"{STRAPI_API_URL}/actualites",
        params={
            "populate": "images",
            "sort": "id:desc",
            "filters[flash][$eq]": "true",
        },
        headers=STRAPI_API_AUTH_TOKEN,
    )
    flashes_1 = []
    if flashes_0_response.ok:
        flashes_0 = flashes_1_response.json()["data"]
    flashes_all = flashes_0 + flashes_1
    if(len(flashes_all) > 0):
        flashes_all = sorted(
            flashes_all, key=lambda x: x["attributes"]["publishedAt"], reverse=True
        )
    flashes = []
    flashes = [
        {
            "head": item["attributes"]["head"],
            "createdAt": item["attributes"]["date"],
            "id": item["id"],
            "article": True if item["attributes"].__contains__('slugId') else False,
            "slugId": item["attributes"]["slugId"] if item["attributes"].__contains__('slugId') else ""
        }
        for item in flashes_all[:20]
    ]
    magazine_response = requests.get(
        url=f"{STRAPI_API_URL}/actualites",
        params={
            "populate": ["images","category"],
            "sort": "id:desc",
            "filters[spotlight][$eq]": "true",
            "filters[category][type][$eq]": "Tendance",
            "pagination[limit]": 5,
        },
        headers=STRAPI_API_AUTH_TOKEN,
    )
    magazine = []
    if magazine_response.ok:
        magazine_data = magazine_response.json()["data"]
        magazine = [
            item
            for item in magazine_data
            if item["attributes"]["images"]["data"][0]["attributes"]["width"]
        ]
    news_response = requests.get(
        url=f"{STRAPI_API_URL}/actualites",
        params={
            "populate": ["images","category"],
            "sort": "id:desc",
            "filters[category][type][$eq]": "Actualite",
            "pagination[limit]": 10,
        },
        headers=STRAPI_API_AUTH_TOKEN,
    )
    news = []
    if news_response.ok:
        news_data = news_response.json()["data"]
        news = [
            item
            for item in news_data
            if item["attributes"]["images"]["data"]
        ]
    magazines_response = requests.get(
        url=f"{STRAPI_API_URL}/actualites",
        params={
            "populate": ["images","category"],
            "sort": "id:desc",
            "filters[category][type][$eq]": "Actualite",
            "filters[category][name][$in]": ["International", "Médecine & Santé"],
            "pagination[limit]": 20,
        },
        headers=STRAPI_API_AUTH_TOKEN,
    )
    magazines = []
    if magazines_response.ok:
        magazines_data = magazines_response.json()["data"]
        magazines = [
            item
            for item in magazines_data
            if item["attributes"]["images"]["data"]
        ]

    locale.setlocale(locale.LC_TIME,'fr_FR.UTF-8')
    data = {
        "today": datetime.now().strftime("%A, %d %B %Y").title(),
        "spotlights": spotlights,
        "flashes": flashes,
        "news": news,
        "magazine": magazine,
        "magazines": magazines,
    }
    return {"data": data}
