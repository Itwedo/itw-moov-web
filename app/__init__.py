from pathlib import Path
from datetime import datetime, date

from flask import Flask, redirect, request, render_template, send_from_directory

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import os
import smtplib
import ssl
import requests
import markdown2
from bs4 import BeautifulSoup


app = Flask(__name__)
app.config.from_mapping(SECRET_KEY=b"\xd6\x04\xbdj\xfe\xed$c\x1e@\xad\x0f\x13,@G")

EMAIL_USER = os.environ.get("EMAIL_USER", "")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD", "")
SMTP_SERVER = os.environ.get("SMTP_SERVER", "")
SMTP_PORT = 465
EMAIL_ACCOUNT = os.environ.get("EMAIL_ACCOUNT", "rhino.rabe-harifetra@telma.mg")

STRAPI_API_URL = os.environ.get("STRAPI_API_URL", "http://localhost:2337/api")
STRAPI_API_AUTH_TOKEN = {
    "Authorization": f'Bearer {os.environ.get("STRAPI_API_AUTH_TOKEN", "")}'
}
CMS_URL = os.environ.get(
    "STRAPI_PUBLIC_URL", STRAPI_API_URL.replace(f'/{STRAPI_API_URL.split("/")[-1]}', "")
)


class ContactForm(FlaskForm):
    name = StringField("Nom")
    phonenumber = StringField("Numéro de téléphone")
    email = StringField("E-mail")
    message = TextAreaField("Message")
    submit = SubmitField("Envoyer")


@app.route("/")
def home():
    ads = requests.get(
        url=f"{STRAPI_API_URL}/ads",
        params={"populate": "image"},
        headers=STRAPI_API_AUTH_TOKEN,
    )
    spotlights = requests.get(
        url=f"{STRAPI_API_URL}/actualites",
        params={
            "populate": "images",
            "sort": "id:desc",
            "filters[spotlight][$eq]": "true",
        },
        headers=STRAPI_API_AUTH_TOKEN,
    )
    flashes_0 = requests.get(
        url=f"{STRAPI_API_URL}/flash-news",
        params={"populate": "images", "sort": "id:desc"},
        headers=STRAPI_API_AUTH_TOKEN,
    )
    flashes_1 = requests.get(
        url=f"{STRAPI_API_URL}/actualites",
        params={"populate": "images", "sort": "id:desc", "filters[flash][$eq]": "true"},
        headers=STRAPI_API_AUTH_TOKEN,
    )
    flashes  = flashes_0.json()['data'] + flashes_1.json()['data']
    flashes = sorted(flashes, key=lambda x: x['attributes']['publishedAt'], reverse=True)
    magazine = requests.get(
        url=f"{STRAPI_API_URL}/actualites",
        params={
            "populate": "images",
            "sort": "id:desc",
            "filters[Type][$eq]": "Tendance",
            "pagination[limit]": 1,
        },
        headers=STRAPI_API_AUTH_TOKEN,
    )
    news = requests.get(
        url=f"{STRAPI_API_URL}/actualites",
        params={
            "populate": "images",
            "sort": "id:desc",
            "filters[source][$eq]": "moov",
            "pagination[limit]": 100,
        },
        headers=STRAPI_API_AUTH_TOKEN,
    )

    data = {
        "today": datetime.now().strftime("%A, %d %B %Y"),
        "spotlights": [
            # each spotligh needs an image, an id, a title, createdAt, head
            {
                "id": item["id"],
                "title": item["attributes"]["title"],
                "createdAt": item["attributes"]["createdAt"],
                "head": item["attributes"]["head"],
                "images": item["attributes"]["images"]["data"],
            }
            for item in spotlights.json()["data"]
        ],
        "flashes": [
            {
                "head": item["attributes"]["head"],
                "createdAt": item["attributes"]["createdAt"],
                "id": item["id"],
            }
            for item in flashes[:20]
        ],
        "news": [
            item for item in news.json()["data"] if item["attributes"]["images"]["data"]
        ],
        "magazine": [
            item for item in magazine.json()['data'] if item["attributes"]["images"]["data"]
        ]
    }
    ads = {
        ad["attributes"]["location"]: ad["attributes"]["image"]["data"]["attributes"][
            "url"
        ]
        for ad in ads.json()["data"]
    }

    return render_template(
        "index.html",
        data=data,
        ads=ads,
        CMS_URL=CMS_URL,
    )


@app.route("/actualites/<id>")
def actualite(id):
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
    response = requests.get(
        url=f"{STRAPI_API_URL}/actualites/{id}",
        params={"populate": "images"},
        headers=STRAPI_API_AUTH_TOKEN,
    )

    body = response.json()["data"]["attributes"]["body"]
    body = body.replace('- ', '# ').replace(' -', '')

    # body = cut_body(response.json()["data"]["attributes"]["body"])

    regular = requests.get(
        url=f"{STRAPI_API_URL}/actualites",
        params={"populate": "images", "sort": "id:desc", "pagination[limit]": 100},
        headers=STRAPI_API_AUTH_TOKEN,
    )

    actualites = {"data": []}

    for data in regular.json()["data"]:
        if data["attributes"]["images"]["data"] is not None:
            actualites["data"].append(data)

    return render_template(
        "actualite.html",
        actualites=actualites,
        news=response.json(),
        body=body,
        CMS_URL=CMS_URL,
        ads=ads,
    )


@app.route("/actualites")
def news():
    # 10/page
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
    result = requests.get(
        url=f"{STRAPI_API_URL}/actualites",
        params={
            "populate": "images",
            "sort": "id:desc",
            "pagination[pageSize]": 10,
            "pagination[page]": request.args.get("page", 1),
            "pagination[withCount]": 1,
        },
        headers=STRAPI_API_AUTH_TOKEN,
    )

    return render_template(
        "actualites.html",
        result=result.json(),
        page=request.args.get("page", 1),
        CMS_URL=CMS_URL,
        ads=ads,
    )


@app.route("/magazine")
def tendance():
    # 18/page
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
    result = requests.get(
        url=f"{STRAPI_API_URL}/actualites",
        params={
            "populate": "images",
            "sort": "id:desc",
            "pagination[pageSize]": 18,
            "pagination[page]": request.args.get("page", 1),
            "pagination[withCount]": 1,
        },
        headers=STRAPI_API_AUTH_TOKEN,
    )

    return render_template(
        "tendance.html",
        result=result.json(),
        page=request.args.get("page", 1),
        CMS_URL=CMS_URL,
        ads=ads,
    )


@app.route("/recherche")
def recherche():
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
    result = requests.get(
        url=f"{STRAPI_API_URL}/actualites",
        params={
            "populate": "images",
            "sort": "id:desc",
            "filters[title][$containsi]": request.args.get("query", ""),
            "pagination[pageSize]": 8,
            "pagination[page]": request.args.get("page", 1),
            "pagination[withCount]": 1,
        },
        headers=STRAPI_API_AUTH_TOKEN,
    )

    regular = requests.get(
        url=f"{STRAPI_API_URL}/actualites",
        params={"populate": "images", "sort": "id:desc", "pagination[limit]": 100},
        headers=STRAPI_API_AUTH_TOKEN,
    )

    actualites = {"data": []}

    for data in regular.json()["data"]:
        if data["attributes"]["images"]["data"] is not None:
            actualites["data"].append(data)

    return render_template(
        "recherche.html",
        result=result.json(),
        actualites=actualites,
        query=request.args.get("query", ""),
        page=request.args.get("page", 1),
        CMS_URL=CMS_URL,
        ads=ads,
    )


@app.route("/mention.html")
def mention():
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
    return render_template("mention.html", CMS_URL=CMS_URL, ads=ads)


@app.route("/contact.html", methods=["GET", "POST"])
def contact():
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
    form = ContactForm()
    if request.method == "POST":
        data = form.data
        moment = datetime.now()
        response = requests.post(
            url=f"{STRAPI_API_URL}/contacts",
            headers=STRAPI_API_AUTH_TOKEN,
            json={
                "data": {
                    "date": moment.isoformat(),
                    "name": data["name"],
                    "phonenumber": data["phonenumber"],
                    "email": data["email"],
                    "message": data["message"],
                }
            },
        )
        # message = MIMEMultipart('alternative')
        # message['Subject'] = 'Contact'
        # message['From'] = data['email']
        # message['To'] = EMAIL_ACCOUNT
        # text = [
        #     f'Date et heure: {moment.isoformat()}',
        #     f'Nom: {data["name"]}',
        #     f'Telephone: {data["phonenumber"]}',
        #     f'Email: {data["email"]}',
        #     f'Message: {data["message"]}'
        # ]
        # text = '\n'.join(text)
        # message.attach(MIMEText(text, 'plain'))
        # context = ssl.create_default_context()
        # with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
        #     server.login(EMAIL_USER, EMAIL_PASSWORD)
        #     server.sendmail(data['email'], EMAIL_ACCOUNT, message.as_string())
        return redirect("/contact.html")
    return render_template("contact.html", form=form, CMS_URL=CMS_URL, ads=ads)


@app.route("/taux-de-change")
def exchange_rates():
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
    response = requests.get(
        url=f"{STRAPI_API_URL}/exchangerates",
        headers=STRAPI_API_AUTH_TOKEN,
        params={"filters[date][$eq]": today, "filters[currency][$in]": ["USD", "EUR"]},
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
        CMS_URL=CMS_URL,
        ads=ads,
    )


@app.route("/pharmacies")
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
        CMS_URL=CMS_URL,
        ads=ads,
    )


@app.route("/coming_soon.html")
def coming_soon():
    return render_template("coming_soon.html")


@app.route("/assets/<path:filename>")
def serve_assets(filename):
    return send_from_directory(Path() / "assets/", filename)


@app.template_filter("date")
def _date(s):
    if isinstance(s, str):
        return datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%d/%m/%Y")
    return ""


@app.template_filter("time")
def _time(s):
    if isinstance(s, str):
        return datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%H:%M")
    return ""


@app.template_filter("markdown")
def _markdown(s):
    if isinstance(s, str):
        return markdown2.markdown(
            s,
            extras=[
                "break-on-newline",
                "cuddled-lists",
                "markdown-in-html",
                "header-ids",
                "strike",
                "target-blank-links",
                "task_list",
            ],
        )
    return ""


def cut_body(text):
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
