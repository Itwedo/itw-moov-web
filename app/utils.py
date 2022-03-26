from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta
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
