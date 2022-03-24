from datetime import datetime, date
from flask import (
    Flask,
    redirect,
    request,
    render_template,
    send_from_directory,
)
from pathlib import Path
from .config import *
from .utils import get_ads, get_currency
from .contact import app as contact
from .drugstores import app as drugstores
from .forex import app as forex
from .home import app as home
from .magazine import app as magazine
from .news import app as news
from .preview import app as preview
from .search import app as search

import requests
import markdown2


app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY=b"\xd6\x04\xbdj\xfe\xed$c\x1e@\xad\x0f\x13,@G"
)
app.register_blueprint(contact)
app.register_blueprint(drugstores)
app.register_blueprint(forex)
app.register_blueprint(home)
app.register_blueprint(magazine)
app.register_blueprint(news)
app.register_blueprint(preview)
app.register_blueprint(search)


@app.template_filter("date")
def _date(s):
    if isinstance(s, str):
        return datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%fZ").strftime(
            "%d/%m/%Y"
        )
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


@app.route("/mention.html")
def mention():
    ads = get_ads()
    currency = get_currency()
    return render_template(
        "mention.html", CMS_URL=STRAPI_PUBLIC_URL, ads=ads, currency=currency
    )


@app.route("/coming_soon.html")
def coming_soon():
    ads = get_ads()
    currency = get_currency()
    return render_template(
        "coming_soon.html",
        CMS_URL=STRAPI_PUBLIC_URL,
        ads=ads,
        currency=currency(),
    )


@app.errorhandler(404)
def not_found(error):
    ads = get_ads()
    currency = get_currency()
    return (
        render_template(
            "404.html", CMS_URL=STRAPI_PUBLIC_URL, ads=ads, currency=currency
        ),
        404,
    )


@app.route("/assets/<path:filename>")
def serve_assets(filename):
    return send_from_directory(Path() / "assets/", filename)
