from flask import (
    Blueprint,
    redirect,
    request,
    render_template,
    send_from_directory,
)
from datetime import datetime, date, timedelta
from .config import *
from .utils import use_template, get_paginated_curency

import requests


app = Blueprint("life", __name__, url_prefix="/vie-pratique")


@app.route("/cours-de-change")
@use_template("exchange_rate.html")
def exchange_rates():
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
    return {
        "seven_date": existant_dates,
        "result": result,
        "date": date.today().strftime("%d/%m/%Y"),
    }


@app.route("/pharmacie")
@use_template("pharmacie.html")
def drugstores():
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
    start = datetime.strptime(
        result[0]["attributes"]["start"], "%Y-%m-%d"
    ).strftime("%d/%m/%Y")
    stop = datetime.strptime(
        result[0]["attributes"]["stop"], "%Y-%m-%d"
    ).strftime("%d/%m/%Y")
    return {"start": start, "stop": stop, "result": result}

@app.route("/meteo")
@app.route("/meteo/<string:city>")
@use_template("meteo.html")
def weather_report(city="Antananarivo"):
    city = request.args.get("city", city)  
    lang = request.args.get("lang", "fr")  
    api_key = "f44c786dff794da38fd73052231209"
    response = requests.get(
        url="http://api.weatherapi.com/v1/forecast.json",
        params={"key": api_key, "q": city, "days": 7, lang: lang}  # Récupérer les prévisions pour 7 jours
    )
    weather_data = response.json()
    return {"city": city, "weather_data": weather_data}
