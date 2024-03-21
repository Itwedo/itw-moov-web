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
from datetime import date
import calendar

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
def drugstores(city="Antananarivo"):
    today = date.today().strftime("%Y-%m-%d")
    todays_month = today.split("-")[1]
    response = requests.get(
        url=f"{STRAPI_API_URL}/allnighters",
        headers=STRAPI_API_AUTH_TOKEN_BEARER,
        params={
            "filters[$and][0][start][$lte]": today,
            "filters[$and][1][stop][$gte]": today,
            "sort": "start:desc",
            "populate": "drugstore",
        },
    )
    result = response.json()["data"]
    print(f"result: ${result}")
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
    hour = request.args.get("hour", 6)  
    api_key = "f44c786dff794da38fd73052231209"
    response = requests.get(
        url="http://api.weatherapi.com/v1/forecast.json",
        params={"key": api_key, "q": city, "days": 7, lang: lang, "hour": hour}  # Récupérer les prévisions pour 7 jours
    )
    weather_data = response.json()
    day = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
    month = ['Janvier', 'Fevrier', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Aout', 'Septembre', 'Octobre', 'Novembre', 'Décembre']

    for forecast in weather_data["forecast"]["forecastday"]:
        date_string = forecast["date"]
        date_object = datetime.strptime(date_string, "%Y-%m-%d")
        mois = month[date_object.month - 1]  # Adjusting month index to start from 0
        formatted_date = date_object.strftime("%d") + " " + mois
        day_of_week = calendar.weekday(date_object.year, date_object.month, date_object.day)
        formatted_day = day[day_of_week]
        forecast["formatted_date"] = formatted_date
        forecast["formatted_day"] = formatted_day

    #Get all data hour for the current day
    weather_hours_data = []
    
    for hour in range(1, 24):
        response = requests.get(
            url="http://api.weatherapi.com/v1/forecast.json",
            params={"key": api_key, "q": city, "days": 1, "lang": lang, "hour": hour}
        )
        wh_data = response.json()
        
        for forecast in wh_data["forecast"]["forecastday"]:
            if(len(forecast['hour']) > 0):
                hour_data = forecast['hour'][0]
                time_string = forecast['hour'][0]['time']
                time_object = datetime.strptime(time_string, "%Y-%m-%d %H:%M")
                formatted_hour = time_object.strftime("%H")
                hour_data["target_hour"] = int(formatted_hour)
                hour_data["target_temp_c"] = int(hour_data['temp_c'])
                weather_hours_data.append(hour_data)
    
    return {"city": city, "weather_data": weather_data, "now": date.today().strftime('%d/%m/%Y'), "weather_hours_data": weather_hours_data }
