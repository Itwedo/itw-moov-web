#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint

import uuid


app = Blueprint(
    "preview",
    __name__,
    url_prefix="/preview"
)


@app.route("/actualites/<string:unique_id>", methods=["GET", "POST"])
def preview_page(unique_id):
    """Given an ID, fetch and display page"""
    pass
