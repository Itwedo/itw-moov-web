from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta
from flask import render_template, request
from functools import wraps
from captcha.image import ImageCaptcha
import string
import random
from pathlib import Path
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
    response_ads["banner"] = get_ads_by_location("Banner")
    response_ads["with_article"] = get_ads_by_location("WithArticle")

    side_bar = get_ads_by_location("SideBar")
    first_len = round(len(side_bar) / 2)
    response_ads["side_bar"] = [side_bar[:first_len], side_bar[first_len:]]

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


def get_heigh(text_type, text):
    """
    type : 'title' or 'head' or 'body'
    """
    types = {
        "title": {"line": 18, "heigh": 60},
        "head": {"line": 77, "heigh": 22},
        "body": {"line": 110, "heigh": 25},
    }
    heigh = len(text) * types[text_type]["heigh"] / types[text_type]["line"]
    if "<h2>" or "<h3>" in text:
        heigh += types[text_type]["heigh"]
    if "https://moov-cms.sudo.mg" in text:
        heigh += 500
    return heigh


def image_body(text):
    if "/uploads/" in text:
        text = text.replace("/uploads", f"https://moov-cms.sudo.mg/uploads")
    return text


def cut_body(title, head, text, images_number):
    """Divides an article in two parts if length exceeds 700 chars"""
    if images_number <= 1:
        FIRST_LIMIT_CHAR = 200
        FIRST_LIMIT_HEIGH = 540
    else:
        FIRST_LIMIT_CHAR = 150
        FIRST_LIMIT_HEIGH = 250

    if BeautifulSoup(text, "html.parser").find():
        text = BeautifulSoup(text, "html.parser")
        separator = ""
        text_backup = list()
        if len(text) <= 2:
            for part in text:
                if len(part) > 1:
                    text_backup.append(part)

            if len(text_backup) == 1:
                text = (text_backup[0].text).split("\n")
                separator = "\n"

    else:
        text = text.split("\n")
        text[-1] = text[-1].replace("]]>", "")
        separator = "\n"
    first_part = []
    second_part = []
    medium = ""

    for child in text:
        child = image_body(child)
        if str(child) != "\n" and child != "":
            if second_part:
                second_part.append(child)
            elif (
                    get_heigh("title", title)
                    + get_heigh("head", head)
                    + get_heigh("body", "".join([str(tag) for tag in first_part]))
                    + get_heigh("body", str(child))
                    >= FIRST_LIMIT_HEIGH
            ):
                second_part.append(child)
            else:
                first_part.append(child)

    if second_part:
        if f"https://moov-cms.sudo.mg/uploads" in second_part[0]:
            medium = second_part[1] if len(second_part) >= 2 else ""
        else:
            medium = (
                separator.join([str(second_part[0]), str(second_part[1])])
                if len(second_part) >= 2
                else str(second_part[0])
            )
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


def get_menus(type):
    actualities = requests.get(
        url=f"{STRAPI_API_URL}/rubriques",
        headers=STRAPI_API_AUTH_TOKEN,
        params={
            "filters[actualites][id][$notNull]": True,
            "filters[type][$eq]": type,
        },
    )
    return actualities.json()["data"]


def get_category_display(category):
    return requests.get(
        url=f"{STRAPI_API_URL}/rubriques",
        params={
            "filters[slug][$eq]": category,
            "sort": "order:asc"
        },
        headers=STRAPI_API_AUTH_TOKEN,
    ).json()["data"][0]["attributes"]


def get_rubriques():
    menus = requests.get(
        url=f"{STRAPI_API_URL}/rubriques",
        headers=STRAPI_API_AUTH_TOKEN,
    ).json()["data"]
    menu_list = []
    for menu in menus:
        menu_list.append({"id": menu["id"], "name": menu["attributes"]["name"], "slug": menu["attributes"]["slug"]})
    return menu_list


def get_rubrique_id(article_category):
    for m in get_rubriques():
        if m["name"] == article_category:
            return m["id"]
        else:
            return 0


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
            ctx["actualities"] = [{"display": menu["attributes"]["name"], "slug": menu["attributes"]["slug"]} for menu
                                  in get_menus("Actualite")]
            ctx["magazines"] = [{"display": menu["attributes"]["name"], "slug": menu["attributes"]["slug"]} for menu in
                                get_menus("Tendance")]
            return render_template(template_name, **ctx)

        return decorated_function

    return decorator


def create_captcha():
    captcha_path = "/tmp/captcha"
    Path(captcha_path).mkdir(exist_ok=True)
    captcha_name = f"captcha{random.randint(0, 100)}"
    captcha_text = "".join(
        random.choices(string.ascii_uppercase + string.digits, k=5)
    )
    # Create an image instance of the given size
    image = ImageCaptcha(width=280, height=45)
    data = image.generate(captcha_text)

    # write the image on the given file and save it
    image.write(captcha_text, f"{captcha_path}/{captcha_name}.png")
    return {
        "image": f"{captcha_path}/{captcha_name}.png",
        "text": captcha_text,
    }
