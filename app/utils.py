from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta
from .config import *

import requests


def get_ads_by_location(location):
    ads = requests.get(
        url=f"{STRAPI_API_URL}/ads",
        params={"populate": "image", "filters[location][$eq]": location},
        headers=STRAPI_API_AUTH_TOKEN,
    )

    list_ads = list()
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

    response_ads = dict()
    response_ads["top_bar"] = get_ads_by_location("TopBar")
    response_ads["side_bar"] = get_ads_by_location("SideBar")
    response_ads["banner"] = get_ads_by_location("Banner")
    response_ads["with_article"] = get_ads_by_location("WithArticle")
    return response_ads


def get_currency():
    today = date.today().strftime("%Y-%m-%d")
    response = requests.get(
        url=f"{STRAPI_API_URL}/exchangerates",
        headers=STRAPI_API_AUTH_TOKEN,
        params={
            "filters[date][$eq]": today,
            "filters[currency][$in]": [
                "USD",
                "EUR",
            ],
        },
    )
    result = {
        i["attributes"]["currency"]: round(i["attributes"]["value"], 2)
        for i in response.json()["data"]
    }

    return result


def cut_body(text):
    """Divides an article in two parts if length exceeds 1750 chars"""
    FIRST_LIMIT_CHAR = 1750

    first_part = []
    second_part = []
    for child in BeautifulSoup(text, "html.parser"):
        if len("".join([str(tag) for tag in first_part])) >= FIRST_LIMIT_CHAR:
            second_part.append(child)
        else:
            first_part.append(child)

    return (
        "".join([str(tag) for tag in first_part]),
        "".join([str(tag) for tag in second_part]),
    )
