#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
from pathlib import Path

from PIL import Image

# from requests_html import HTML, HTMLSession
from ..config import *


class Connector(object):
    def __init__(
        self,
    ):
        self.article_dir = "/tmp/export/actualites"
        self.images_dir = "/Users/mampionona/projects/telma/moov/MOOV.MG/moov/sites/default/files"
        self.files = self.loop_dir()
        self.count = 0

    def post_article(self, actuality, image_id):
        actuality_item = dict()
        del actuality["id"]
        if image_id:
            actuality["images"] = image_id
        if not actuality.get("category"):
            actuality["category"] = "Vaovao"
        if not actuality.get("Type"):
            actuality["Type"] = "Actualite"
        if not actuality.get("source"):
            actuality["source"] = "moov"
        for item, value in actuality.items():

            if value:
                actuality_item[item] = value
        result = requests.post(
            url=f"{STRAPI_API_URL}/actualites",
            headers=STRAPI_API_AUTH_TOKEN,
            json={"data": actuality_item},
        )

    def filter_article(self, article):
        id = None
        if len(article["body"]) < 2000:
            return None
        elif article["images"]:
            try:
                with open(
                    f'{self.images_dir}/{article["images"][0]}', "rb"
                ) as f:
                    if (
                        Image.open(
                            f'{self.images_dir}/{article["images"][0]}'
                        ).size[0]
                        < 500
                    ):
                        return None
                    else:
                        response = requests.post(
                            url=f"{STRAPI_API_URL}/upload",
                            headers=STRAPI_API_AUTH_TOKEN,
                            files={
                                "files": (
                                    article["images"][0],
                                    f,
                                    "image/jpeg",
                                ),
                                "Content-Disposition": f'form-data; name="file"; filename={article["images"][0]}',
                                "Content-Type": "image/jpeg",
                            },
                        )
                    try:
                        id = response.json()[0]["id"]
                    except Exception:
                        return None
            except FileNotFoundError:
                return None
        return id

    def post_articles_file(self, filepath):
        with open(filepath) as json_file:
            data = json.load(json_file)
            for actuality in data:
                id = self.filter_article(actuality)
                if id:
                    self.post_article(actuality, id)
                self.count += 1

    def loop_dir(self):
        list_files = list()
        files = Path(self.article_dir).glob("*")
        for file in files:
            list_files.append(file)
        list_files.sort()
        return list_files

    def delecte_actus(self):
        result = requests.get(
            url=f"{STRAPI_API_URL}/actualites",
            params={
                "filters[category][$eq]": "Vaovao",
            },
            headers=STRAPI_API_AUTH_TOKEN,
        )
        print(result.json()["data"][-1])
