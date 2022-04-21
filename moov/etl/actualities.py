#!/usr/bin/env python
# -*- coding: utf-8 -*-

from calendar import firstweekday
import requests
import json
from pathlib import Path

from PIL import Image

# from requests_html import HTML, HTMLSession
from ..config import *
from .legacy_extractor.mapping import map_category


class Connector(object):
    def __init__(self, filepath, node_type):
        self.article_dir = filepath
        self.images_dir = "/Users/mampionona/projects/telma/moov/MOOV.MG/moov/sites/default/files"
        self.files = self.loop_dir()
        self.count = 0
        self.type = node_type

    def post_article(self, actuality, image_id):
        actuality_item = dict()
        del actuality["id"]
        if image_id:
            actuality["images"] = image_id

        if not actuality.get("category"):
            actuality["category"] = "Vaovao"
        else:
            actuality["category"] = map_category(actuality.get("category"))

        if not actuality.get("Type"):
            actuality["Type"] = self.type

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
        if result.json()["data"] and result.json()["data"].get("id"):
            self.count += 1

    def filter_article(self, article):
        id = None
        if len(article["body"]) < 2000:
            return None
        elif article["images"]:
            try:
                with open(
                    f'{self.images_dir}/{article["images"][0]}', "rb"
                ) as f:
                    _size = Image.open(
                        f'{self.images_dir}/{article["images"][0]}'
                    ).size
                    if _size[1] < 500:

                        return None
                    else:
                        print(_size)
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
                        # print(response.json())
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
                    # self.count += 1

    def loop_dir(self):
        list_files = list()
        files = Path(self.article_dir).glob("*")
        for file in files:
            list_files.append(file)
        list_files.sort()
        return list_files
