from .config import *
from datetime import datetime, date, timedelta
import requests


def get_ads():
    ads = requests.get(
        url=f"{STRAPI_API_URL}/ads",
        params={"populate": "image"},
        headers=STRAPI_API_AUTH_TOKEN,
    )
    # response_ads = dict()
    # for ad in ads.json()["data"]:
    #     images = list()
    #     for image in ad["attributes"]["image"]["data"]:
    #         images.append(image["attributes"]["url"])
    #     response_ads[ad["attributes"]["location"]] = images
    ads = {
        ad["attributes"]["location"]: ad["attributes"]["image"]["data"][
            "attributes"
        ]["url"]
        for ad in ads.json()["data"]
    }
    return ads


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
        i["attributes"]["currency"]: round(1 / i["attributes"]["rate"])
        for i in response.json()["data"]
    }

    return result
