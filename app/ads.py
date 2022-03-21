from .config import *
import requests


def get_ads():
    ads = requests.get(
        url=f"{STRAPI_API_URL}/ads",
        params={"populate": "image"},
        headers=STRAPI_API_AUTH_TOKEN,
    )
    ads = {
        ad["attributes"]["location"]: ad["attributes"]["image"]["data"][
            "attributes"
        ]["url"]
        for ad in ads.json()["data"]
    }
    return ads
