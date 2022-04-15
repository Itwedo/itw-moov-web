from datetime import datetime, date
from flask import (
    Flask,
    redirect,
    request,
    render_template,
    send_from_directory,
)
from logging.config import dictConfig
from pathlib import Path
from .config import *

from .utils import use_template
from .contact import app as contact
from .life import app as life
from .home import app as home
from .magazine import app as magazine
from .news import app as news
from .preview import app as preview
from .search import app as search
from .article import app as article
from .redirection import app as redirection

import requests
import markdown2


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
@use_template()
def mention():
    return


@app.route("/coming_soon.html")
@use_template()
def coming_soon():
    return


@app.errorhandler(404)
@use_template("404.html")
def not_found(error):
    return


@app.route("/assets/<path:filename>")
def serve_assets(filename):
    return send_from_directory(Path() / "assets/", filename)


@app.route("/tmp/<path:filename>")
def serve_tmp(filename):
    return send_from_directory(Path() / "/tmp/", filename)
