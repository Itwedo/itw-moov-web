#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import (
    Blueprint,
    redirect,
    request,
    render_template,
    send_from_directory,
)
from .config import *
from .utils import cut_body

import requests


app = Blueprint(
    "preview",
    __name__,
    url_prefix="/preview"
)


@app.route("/actualites/<string:slug>", methods=["GET", "POST"])
def preview_page(slug):
    """Given a slug, fetch and display page"""
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
    response = requests.get(
        url=f"{STRAPI_API_URL}/actualites",
        params={
            "populate": "images",
            "publicationState": "preview",
            "filter[slug][$eq]": slug
        },
        headers=STRAPI_API_AUTH_TOKEN,
    )
    news = response.json()
    if not news['data']:
        return redirect(
            f"{STRAPI_PUBLIC_URL}not-found.html"
        )
    article = news['data'][0]
    images = article['attributes']['images']['data']
    if images:
        number_of_images = len(images)
    else:
        number_of_images = 0

    body = cut_body(article["attributes"]["body"])

    same_category = requests.get(
        url=f"{STRAPI_API_URL}/actualites",
        params={
            "populate": "images",
            "sort": "id:desc",
            "pagination[limit]": 100,
            "filter[category][$eq]": article['attributes']['category']
        },
        headers=STRAPI_API_AUTH_TOKEN,
    )
    same_category = same_category.json()['data']
    if same_category:
        same_category = [
            i for i in same_category
            if i['id'] != id and i['attributes']['images']['data']
        ][:4]

    regular = requests.get(
        url=f"{STRAPI_API_URL}/actualites",
        params={
            "populate": "images",
            "sort": "id:desc",
            "pagination[limit]": 100
        },
        headers=STRAPI_API_AUTH_TOKEN,
    )
    regular = regular.json()['data']
    if regular:
        regular = [
            element for element in regular
            if element['id'] != id and element['attributes']['images']['data']
        ][:20]

    return render_template(
        "actualite.html",
        news={'data': article},
        images=images,
        number_of_images=number_of_images,
        body=body,
        same_category=same_category,
        regular=regular,
        CMS_URL=STRAPI_PUBLIC_URL,
        ads=ads,
    )    
