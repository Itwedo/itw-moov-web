from flask import (
    Blueprint,
    redirect,
    request,
    render_template,
    send_from_directory,
)
from datetime import datetime, date
from .config import *
from .ads import get_ads

import requests


app = Blueprint("forex", __name__, url_prefix="/taux-de-change")


@app.route("/")
def exchange_rates():
    ads = get_ads()
    today = date.today().strftime("%Y-%m-%d")
    response = requests.get(
        url=f"{STRAPI_API_URL}/exchangerates",
        headers=STRAPI_API_AUTH_TOKEN,
        params={
            "filters[date][$eq]": today,
            "filters[currency][$in]": ["USD", "EUR"],
        },
    )
    result = [
        {
            "currency": i["attributes"]["currency"],
            "value": round(1 / i["attributes"]["rate"]),
        }
        for i in response.json()["data"]
    ]
    print(result)
    return render_template(
        "exchange.html",
        result=result,
        date=date.today().strftime("%d/%m/%Y"),
        CMS_URL=STRAPI_PUBLIC_URL,
        ads=ads,
    )
