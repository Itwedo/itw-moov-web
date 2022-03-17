from datetime import datetime, date
from flask import (
    Blueprint,
    redirect,
    request,
    render_template,
    send_from_directory,
)
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .config import *

import smtplib
import requests

app = Blueprint("contact", __name__, url_prefix="/")


class ContactForm(FlaskForm):
    name = StringField("Nom")
    phonenumber = StringField("Numéro de téléphone")
    email = StringField("E-mail")
    message = TextAreaField("Message")
    submit = SubmitField("Envoyer")


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
    return render_template("contact.html", form=form, CMS_URL=STRAPI_PUBLIC_URL, ads=ads)
