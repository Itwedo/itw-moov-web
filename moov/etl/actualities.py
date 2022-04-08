#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
from pathlib import Path

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

    def post_articles_file(self, filepath):
        with open(filepath) as json_file:
            data = json.load(json_file)
            for actuality in data:
                if actuality["images"]:
                    try:
                        with open(
                            f'{self.images_dir}/{actuality["images"][0]}', "rb"
                        ) as f:
                            response = requests.post(
                                url=f"{STRAPI_API_URL}/upload",
                                headers=STRAPI_API_AUTH_TOKEN,
                                files={
                                    "files": (
                                        actuality["images"][0],
                                        f,
                                        "image/jpeg",
                                    ),
                                    "Content-Disposition": f'form-data; name="file"; filename={actuality["images"][0]}',
                                    "Content-Type": "image/jpeg",
                                },
                            )
                        try:
                            obj = response.json()[0]
                        except Exception:
                            obj = None
                    except FileNotFoundError:
                        actuality["images"] = []
                        obj = None
                else:
                    obj = None

                actuality_item = dict()
                del actuality["id"]
                if obj:
                    actuality["images"] = [obj["id"]]
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
