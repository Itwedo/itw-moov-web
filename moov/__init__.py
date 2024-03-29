from datetime import datetime, date, timedelta
from flask import (
    Flask,
    send_from_directory,
)
from logging.config import dictConfig
from pathlib import Path
from moov.config import *

from moov.utils import use_template
from moov.contact import app as contact
from moov.life import app as life
from moov.home import app as home
from moov.magazine import app as magazine
from moov.news import app as news
from moov.preview import app as preview
from moov.search import app as search
from moov.article import app as article
from moov.redirection import app as redirection

from apscheduler.schedulers.background import BackgroundScheduler
from moov.etl import afp

import requests
import markdown2
from tqdm import tqdm

dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            },
            "access": {
                "format": "%(message)s",
            },
        },
        "handlers": {
            "console": {
                "level": "INFO",
                "class": "logging.StreamHandler",
                "formatter": "default",
                "stream": "ext://sys.stdout",
            },
            "error_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "default",
                "filename": LOG_FILE,
                "maxBytes": 10000,
                "backupCount": 10,
                "delay": True,
            },
            "access_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "access",
                "filename": LOG_FILE,
                "maxBytes": 10000,
                "backupCount": 10,
                "delay": True,
            },
        },
        "loggers": {
            "gunicorn.error": {
                "handlers": ["console"] if DEBUG else ["error_file"],
                "level": "INFO",
                "propagate": False,
            },
            "gunicorn.access": {
                "handlers": ["console"] if DEBUG else ["access_file"],
                "level": "INFO",
                "propagate": False,
            },
        },
        "root": {
            "level": "DEBUG",
            "handlers": ["console"] if DEBUG else ["error_file"],
        },
    }
)

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY=b"\xd6\x04\xbdj\xfe\xed$c\x1e@\xad\x0f\x13,@G"
)

app.register_blueprint(redirection)
app.register_blueprint(contact)
app.register_blueprint(life)
app.register_blueprint(home)
app.register_blueprint(magazine)
app.register_blueprint(news)
app.register_blueprint(preview)
app.register_blueprint(search)
app.register_blueprint(article)


def my_scheduled_job():
    for url in AFP_URLS:
        obj = afp.Connector(url, "type")
        feed = obj.get_feed()
        for info in tqdm(obj.feed):
            obj.insert_element(info)


scheduler = BackgroundScheduler()
scheduler.add_job(func=my_scheduled_job, trigger="interval", seconds=300)
scheduler.start()


@app.template_filter("date")
def _date(s):
    if isinstance(s, str):
        return (datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%fZ") + timedelta(hours=3)).strftime(
            "%d/%m/%Y"
        )
    return ""


@app.template_filter("time")
def _time(s):
    if isinstance(s, str):
        return (datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%fZ")+timedelta(hours=3)).strftime("%H:%M")
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


@app.template_filter("title")
def _title(s):
    if isinstance(s, str):
        return s.title()
    return "Moov"


@app.route("/mention.html")
@use_template()
def mention():
    return


@app.route("/coming_soon.html")
@use_template()
def coming_soon():
    return


@app.errorhandler(404)
@app.errorhandler(500)
@use_template("404.html")
def not_found(error):
    return


@app.route("/assets/<path:filename>")
def serve_assets(filename):
    return send_from_directory(Path() / "assets/", filename)


@app.route("/tmp/<path:filename>")
def serve_tmp(filename):
    return send_from_directory(Path() / "/tmp/", filename)
