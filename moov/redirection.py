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


@app.route("/découvrir-madagascar/nature-découverte-circuits/")
def redirect2():
    return redirect(
        url_for("magazine.category_magazines", category="tourisme-voyage")
    )


@app.route("/découvrir-madagascar/testé-pour-vous-nouveauté")
def redirect3():
    return redirect(
        url_for("magazine.category_magazines", category="tourisme-voyage")
    )


@app.route("/education-emploi/education")
def redirect4():
    return redirect(
        url_for("magazine.category_magazines", category="education-emploi")
    )


@app.route("/education-emploi/education/detail/")
def redirect5():
    return redirect(
        url_for("magazine.category_magazines", category="education-emploi")
    )


@app.route("/education-emploi/emploi")
def redirect6():
    return redirect(
        url_for("magazine.category_magazines", category="education-emploi")
    )


@app.route("/tendance-moov/<category>")
def redirect7(category):
    if category == "maison-deco":
        category = "maison-jardin"
    if category == "santé-bien-être":
        category = "sante-bien-etre"
    return redirect(url_for("magazine.category_magazines", category=category))


@app.route("/tendance-moov/<category>/detail/")
def redirect8(category):
    if category == "maison-deco":
        category = "maison-jardin"
    if category == "santé-bien-être":
        category = "sante-bien-etre"
    return redirect(url_for("magazine.category_magazines", category=category))
