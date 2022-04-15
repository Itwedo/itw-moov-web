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
from .utils import use_template, create_captcha


import smtplib
import requests

app = Blueprint("contact", __name__, url_prefix="/")


class ContactForm(FlaskForm):
    name = StringField("Nom")
    phonenumber = StringField("Numéro de téléphone")
    email = StringField("E-mail")
    message = TextAreaField("Message")
    submit = SubmitField("Envoyer")


@app.route("/contact", methods=["GET", "POST"])
@use_template("contact.html")
def contact():
    form = ContactForm()
    captcha = create_captcha()
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
        return {
            "form": form,
            "captcha": captcha["text"],
            "image": captcha["image"],
        }
    return {
        "form": form,
        "captcha": captcha["text"],
        "image": captcha["image"],
    }
