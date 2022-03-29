from flask import (
    Blueprint,
    redirect,
    request,
    render_template,
    send_from_directory,
)
from datetime import datetime, date, timedelta
from .config import *
from .utils import get_ads, get_currency

import requests


app = Blueprint("forex", __name__, url_prefix="/taux-de-change")


@app.route("/")
def exchange_rates():
    ads = get_ads()
    currency = get_currency()
    seven_date = [
        (date.today() - timedelta(i)).strftime("%Y-%m-%d") for i in range(8)
    ]
    page_count, result, existant_dates = get_paginated_curency(
        seven_date, 0, list(), list()
    )
    if page_count > 1:
        for page in range(1, page_count):
            (
                page_count,
                paginated_result,
                existant_dates,
            ) = get_paginated_curency(
                seven_date, page + 1, result, existant_dates
            )
    return render_template(
        "exchange_rate.html",
        seven_date=existant_dates,
        result=result,
        date=date.today().strftime("%d/%m/%Y"),
        CMS_URL=STRAPI_PUBLIC_URL,
        ads=ads,
        currency=currency,
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
