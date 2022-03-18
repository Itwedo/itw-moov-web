from flask import (
    Blueprint,
    redirect,
    request,
    render_template,
    send_from_directory,
)
from datetime import datetime, date
from .config import *

import requests


app = Blueprint("drugstores", __name__, url_prefix="/pharmacies")


@app.route("/")
def drugstores():
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
    today = date.today().strftime("%Y-%m-%d")
    todays_month = today.split("-")[1]
    response = requests.get(
        url=f"{STRAPI_API_URL}/allnighters",
        headers=STRAPI_API_AUTH_TOKEN,
        params={
            "filters[$and][0][start][$lte]": today,
            "filters[$and][1][stop][$gte]": today,
            "sort": "start:desc",
            "populate": "drugstore",
        },
    )
    result = response.json()["data"]
    start = datetime.strptime(result[0]["attributes"]["start"], "%Y-%m-%d").strftime(
        "%d/%m/%Y"
    )
    stop = datetime.strptime(result[0]["attributes"]["stop"], "%Y-%m-%d").strftime(
        "%d/%m/%Y"
    )
    return render_template(
        "pharmacie.html",
        start=start,
        stop=stop,
        result=result,
        CMS_URL=STRAPI_PUBLIC_URL,
        ads=ads,
    )
