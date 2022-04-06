from flask import (
    Blueprint,
    redirect,
    url_for,
)
from .config import *


app = Blueprint("redirection", __name__, url_prefix="/")


@app.route("/actualites/<category>/detail/")
def redirect_category(category):
    if category == "médecine-et-santé":
        category = "sante-medecine"
    return redirect(url_for("news.category_actuality", category=category))
