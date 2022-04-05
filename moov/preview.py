#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import (
    abort,
    Blueprint,
    redirect,
    request,
    render_template,
    send_from_directory,
)

from .config import *
from .utils import cut_body, use_template

import requests


app = Blueprint("preview", __name__, url_prefix="/preview")


@app.route("/actualites/<string:slug>", methods=["GET", "POST"])
@use_template("actualite.html")
def preview_page(slug):
    """Given a slug, fetch and display page"""
    response = requests.get(
        url=f"{STRAPI_API_URL}/actualites",
        params={
            "populate": "images",
            "publicationState": "preview",
            "filters[slug][$eq]": slug,
        },
        headers=STRAPI_API_AUTH_TOKEN,
    )
    news = response.json()
    if not news["data"]:
        abort(404)
    article = news["data"][0]
    images = article["attributes"]["images"]["data"]
    if images:
        number_of_images = len(images)
    else:
        number_of_images = 0

    body = cut_body(
        article["attributes"]["title"],
        article["attributes"]["head"],
        article["attributes"]["body"],
    )

    same_category = requests.get(
        url=f"{STRAPI_API_URL}/actualites",
        params={
            "populate": "images",
            "sort": "id:desc",
            "pagination[limit]": 100,
            "filter[category][$eq]": article["attributes"]["category"],
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

    return {
        "news": {"data": article},
        "images": images,
        "number_of_images": number_of_images,
        "body": body,
        "same_category": same_category,
        "regular": regular,
    }
