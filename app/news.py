from flask import (
    Blueprint,
    redirect,
    request,
    render_template,
    send_from_directory,
)
from .config import *
from .utils import cut_body
from .ads import get_ads

import requests


app = Blueprint("news", __name__, url_prefix="/actualites")


@app.route("/")
def news():
    ads = get_ads()
    result = requests.get(
        url=f"{STRAPI_API_URL}/actualites",
        params={
            "populate": "images",
            "sort": "id:desc",
            "pagination[pageSize]": 10,
            "pagination[page]": request.args.get("page", 1),
            "pagination[withCount]": 1,
        },
        headers=STRAPI_API_AUTH_TOKEN,
    )

    return render_template(
        "actualites.html",
        result=result.json(),
        page=request.args.get("page", 1),
        CMS_URL=STRAPI_PUBLIC_URL,
        ads=ads,
    )


@app.route("/<id>")
def news_article(id):
    ads = get_ads()
    response = requests.get(
        url=f"{STRAPI_API_URL}/actualites/{id}",
        params={"populate": "images"},
        headers=STRAPI_API_AUTH_TOKEN,
    )
    news = response.json()
    images = news["data"]["attributes"]["images"]["data"]
    if images:
        number_of_images = len(images)
    else:
        number_of_images = 0
    body = news["data"]["attributes"]["body"]
    body = body.replace("- ", "# ").replace(" -", "")
    body = cut_body(response.json()["data"]["attributes"]["body"])

    same_category = requests.get(
        url=f"{STRAPI_API_URL}/actualites",
        params={
            "populate": "images",
            "sort": "id:desc",
            "pagination[limit]": 100,
            "filter[category][$eq]": news["data"]["attributes"]["category"],
        },
        headers=STRAPI_API_AUTH_TOKEN,
    )
    same_category = same_category.json()["data"]
    if same_category:
        same_category = [
            i
            for i in same_category
            if i["id"] != id and i["attributes"]["images"]["data"]
        ][:4]

    regular = requests.get(
        url=f"{STRAPI_API_URL}/actualites",
        params={
            "populate": "images",
            "sort": "id:desc",
            "pagination[limit]": 100,
        },
        headers=STRAPI_API_AUTH_TOKEN,
    )
    regular = regular.json()["data"]
    if regular:
        regular = [
            element
            for element in regular
            if element["id"] != id and element["attributes"]["images"]["data"]
        ][:20]

    return render_template(
        "actualite.html",
        news=news,
        images=images,
        number_of_images=number_of_images,
        body=body,
        same_category=same_category,
        regular=regular,
        CMS_URL=STRAPI_PUBLIC_URL,
        ads=ads,
    )
