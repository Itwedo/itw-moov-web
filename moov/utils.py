from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta
from flask import render_template, request
from functools import wraps
from captcha.image import ImageCaptcha
import string
import random
from .config import *

import requests


def generate_dates_interval(ref_date=None, days=7, forward=False):
    """Generates all dates, between `ref_date`
    and `days` days backward. Flag allows to go forward
    if needed.
    Results in a sorted array of `days` days"""
    result = []
    if not ref_date:
        ref_date = date.today()
    result.append(ref_date)
    count = 1
    while count < days:
        if forward:
            result.append(ref_date + timedelta(count))
        else:
            result = [ref_date - timedelta(count)] + result
        count += 1
    return result


def get_ads_by_location(location):
    ads = requests.get(
        url=f"{STRAPI_API_URL}/ads",
        params={"populate": "image", "filters[location][$eq]": location},
        headers=STRAPI_API_AUTH_TOKEN,
    )

    list_ads = []
    for ad in ads.json()["data"]:

        list_ads.append(
            {
                "image": ad["attributes"]["image"]["data"][0]["attributes"][
                    "url"
                ],
                "url": ad["attributes"]["destinationUrl"],
            }
        )

    return list_ads


def get_ads():
    response_ads = {}
    response_ads["top_bar"] = get_ads_by_location("TopBar")
    response_ads["side_bar"] = get_ads_by_location("SideBar")
    response_ads["banner"] = get_ads_by_location("Banner")
    response_ads["with_article"] = get_ads_by_location("WithArticle")
    return response_ads


def get_currency():
    """Actually, this should be renamed as get_latest_currency"""
    dates = generate_dates_interval()
    currencies = ["USD", "EUR"]
    result = {currency: 0 for currency in currencies}
    response = requests.get(
        url=f"{STRAPI_API_URL}/exchangerates",
        headers=STRAPI_API_AUTH_TOKEN,
        params={
            "sort": "date:asc",
            "filters[date][$in]": map(lambda x: x.strftime("%Y-%m-%d"), dates),
            "filters[currency][$in]": currencies,
        },
    )
    data = response.json()["data"]
    if data:
        for currency in currencies:
            infos = list(
                filter(lambda x: x["attributes"]["currency"] == currency, data)
            )
            if infos:
                result[currency] = round(infos[-1]["attributes"]["value"], 2)
    return result


def cut_body(title, head, text, images_number):
    """Divides an article in two parts if length exceeds 700 chars"""
    if images_number <= 1:
        FIRST_LIMIT_CHAR = 500
    else:
        FIRST_LIMIT_CHAR = 350

    if BeautifulSoup(text, "html.parser").find():
        text = BeautifulSoup(text, "html.parser")
        separator = ""
    else:
        text = text.split("\n")
        separator = "\n"
    first_part = []
    second_part = []
    medium = ""
    for child in text:
        if str(child) != "\n" and child != "":
            if (
                len(title)
                + len(head)
                + len("".join([str(tag) for tag in first_part]))
                >= FIRST_LIMIT_CHAR
            ):
                second_part.append(child)
            else:
                first_part.append(child)
    if second_part:
        medium = second_part[0] + second_part[1]

    return (
        separator.join([str(tag) for tag in first_part]),
        separator.join([str(tag) for tag in second_part]),
        str(medium),
    )


def get_paginated_curency(date_list, page, result_list, existant_dates):
    paginated_response = requests.get(
        url=f"{STRAPI_API_URL}/exchangerates",
        headers=STRAPI_API_AUTH_TOKEN,
        params={
            "filters[date][$in]": date_list,
            "filters[currency][$in]": [
                "USD",
                "EUR",
                "CAD",
                "CHF",
                "GBP",
                "ZAR",
            ],
            "pagination[page]": page,
        },
    )

    for i in paginated_response.json()["data"]:
        result_list.append(
            {
                "date": i["attributes"]["date"],
                "currency": i["attributes"]["currency"],
                "value": round(i["attributes"]["value"], 2),
            }
        )
        if i["attributes"]["date"] not in existant_dates:
            existant_dates.append(i["attributes"]["date"])
    return (
        paginated_response.json()["meta"]["pagination"]["pageCount"],
        result_list,
        existant_dates,
    )


def use_template(template=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            template_name = template
            if template_name is None:
                endpoint = request.endpoint
                if not endpoint.endswith(".html"):
                    endpoint = f"{endpoint}.html"
                template_name = endpoint
            ctx = f(*args, **kwargs)
            if not ctx:
                ctx = {}
            ctx["ads"] = get_ads()
            ctx["currency"] = get_currency()
            ctx["CMS_URL"] = STRAPI_PUBLIC_URL
            ctx["actualities"] = [
                {"display": "Vaovao", "slug": "vaovao"},
                {"display": "Internationale", "slug": "internationale"},
                {"display": "Medecine & Santé", "slug": "sante-medecine"},
                {"display": "People", "slug": "people"},
            ]
            ctx["magazines"] = []
            return render_template(template_name, **ctx)

        return decorated_function

    return decorator


def create_captcha():
    captcha_text = "".join(
        random.choices(string.ascii_uppercase + string.digits, k=5)
    )
    # Create an image instance of the given size
    image = ImageCaptcha(width=280, height=45)

    # Image captcha text
    # captcha_text = 'GeeksforGeeks'

    # generate the image of the given text
    data = image.generate(captcha_text)

    # write the image on the given file and save it
    image.write(captcha_text, "moov/assets/images/captcha/CAPTCHA.png")
    return captcha_text
