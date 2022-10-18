#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import requests
import json
from pathlib import Path
import cv2

import PIL


# from requests_html import HTML, HTMLSession
from ..config import *
from ..utils import get_rubrique_id


class Connector(object):
    def __init__(self, filepath, node_type):
        self.article_dir = filepath
        self.images_dir = "/Users/mampionona/projects/telma/moov/drupal/moov/sites/default/files"
        self.files = self.loop_dir()
        self.count = 0
        self.type = node_type

    def post_article(self, actuality, image_id):
        actuality_item = dict()
        del actuality["id"]
        if image_id:
            actuality["images"] = image_id

        if not actuality.get("category"):
            actuality["rubrique"] = get_rubrique_id("Vaovao")
        else:
            actuality["rubrique"] = get_rubrique_id(actuality.get("category"))

        if not actuality.get("Type"):
            actuality["Type"] = self.type

        if not actuality.get("copyright"):
            actuality["copyright"] = "moov"
        if actuality["created_at"]:
            actuality["date"] = actuality["created_at"]
            del actuality["created_at"]

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
        doublons = requests.get(
            url=f"{STRAPI_API_URL}/actualites",
            headers=STRAPI_API_AUTH_TOKEN,
            params={
                "populate": "images",
                "filters[title][$eq]": article["title"],
            },
        )
        if len(doublons.json()["data"]) > 1:
            return {
                "id": article["id"],
                "reason": "doublons",
                "value": article["body"],
            }
        elif len(article["body"]) < 2000:
            return {
                "id": article["id"],
                "reason": "body low charactere",
                "value": article["body"],
            }
        elif article["images"] and not article["images"][0].endswith(".gif"):

            img_original = cv2.imread(
                f'{self.images_dir}/{article["images"][0]}',
            )

            try:
                with open(
                    f'{self.images_dir}/{article["images"][0]}', "rb"
                ) as f:
                    image = PIL.Image.open(
                        f'{self.images_dir}/{article["images"][0]}'
                    )

                    if not self.is_file_corrupted(image):

                        if image.width < 600:

                            return {
                                "id": article["id"],
                                "reason": article["images"][0],
                                "value": image.size,
                            }
                        else:
                            print(image.size)
                            id = self.post_upload(f, article["images"][0])

                        f.close()
                    else:
                        return None

            except (Exception) as e:
                print(e)
                print("error")
                return None
        return id

    def is_file_corrupted(self, image_object):
        try:

            if os.path.getsize(image_object.filename) == 0:
                return True
            image_object.getdata()[0]
            return False
        except Exception as e:
            print(e)
            print("file corrupted :" + image_object.filename)
            return True

    def post_upload(self, file_object, filename):
        """
        return the id of the upload node is success
        """
        response = requests.post(
            url=f"{STRAPI_API_URL}/upload",
            headers=STRAPI_API_AUTH_TOKEN,
            files={
                "files": (
                    filename,
                    file_object,
                    "image/jpeg",
                ),
                "Content-Disposition": f'form-data; name="file"; filename={filename}',
                "Content-Type": "image/jpeg",
            },
        )
        try:
            id = response.json()[0]["id"]
        except Exception:
            return None
        return id

    def post_articles_file(self, filepath):
        missing = list()
        with open(filepath) as json_file:
            data = json.load(json_file)
            for actuality in data:
                id = self.filter_article(actuality)
                if type(id) == int:
                    self.post_article(actuality, id)
                    # self.count += 1
                elif type(id) == dict:
                    missing.append(id)

        filename = filepath.split(".")[1]
        out_file = open(
            f"report/{self.type}/{self.type}{filename}.json",
            "w",
        )
        json.dump(missing, out_file, indent=4)

    def loop_dir(self):
        list_files = list()
        files = Path(self.article_dir).glob("*")
        for file in files:
            list_files.append(file)
        list_files.sort()
        return list_files
