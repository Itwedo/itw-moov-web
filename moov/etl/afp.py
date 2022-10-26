#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from requests_html import HTML, HTMLSession
import PIL
from .. import config
from ..utils import get_rubrique_id


class Connector(object):
    def __init__(self, url, type):
        self.url = url
        self.source = None
        self.feed = []
        self.type = type

    def __get_source__(self):
        try:
            session = HTMLSession()
            response = session.get(self.url)
            return response
        except requests.exceptions.RequestException as e:
            return None

    def mapping_category(self, category):
        categories = {
            "Monde": "Internationale",
            "Sante": "Médecine & Santé",
            "People": "People",
            "Tech-Media": "HighTech",
            "Sport": "Sport",
        }
        return categories[category]

    def get_feed(self):
        self.source = self.__get_source__()
        with self.source as source:
            category = source.html.find("description", first=True).text
            category = category.title().replace("é", "e")
            items = source.html.find("item", first=False)
            for item in items:
                title = item.find("title", first=True).text
                pubDate = item.find("pubDate", first=True).text
                guid = item.find("guid", first=True).text
                description = item.find("description", first=True).text
                media = item.find("content", first=True).attrs.get("url")
                media_copyright = item.find("copyright", first=True).text
                row = {
                    "title": title,
                    "pubDate": pubDate,
                    "guid": guid,
                    "category": self.mapping_category(category),
                    "description": description,
                    "media": media,
                    "media_copyright": media_copyright
                }
                self.feed.append(row)
        return self.feed

    def insert_element(self, element):
        image_url = element["media"]
        image_caption=element["media_copyright"]
        image_name = image_url.split("/")[-1]
        image = requests.get(image_url, stream=True)
        with open(f"/tmp/{image_name}", "wb") as f:
            for chunk in image:
                f.write(chunk)
        try:
            if PIL.Image.open(f"/tmp/{image_name}").width >= 600:
                with open(f"/tmp/{image_name}", "rb") as f:
                    response = requests.post(
                        url=f"{config.STRAPI_API_URL}/upload",
                        headers=config.STRAPI_API_AUTH_TOKEN,
                        files={
                            "files": (image_name, f, "image/jpeg"),
                            "Content-Disposition": f'form-data; name="file"; filename={image_name}',
                            "fileInfo": '{"caption": "image_caption"}',
                            "Content-Type": "image/jpeg",
                        },

                    )
                try:
                    obj = response.json()[0]
                except Exception:
                    obj = None

                head, body = element["description"].split("\n", 1)
                body = (
                    body.replace("- ", "### ")
                    .replace(" -", "")
                    .replace("\n", "\n\n")
                    .replace("]]>", "")
                )
                article_data = {
                    "title": element["title"],
                    "head": head,
                    "body": body,
                    "copyright": "afp",
                    "rubrique": [get_rubrique_id(element["category"])],
                    "metaTitle": element["title"][:79],
                    "metaDescription": head[:119]
                }
                if obj:
                    article_data["images"] = obj["id"]

                response = requests.post(
                    url=f"{config.STRAPI_API_URL}/actualites",
                    headers=config.STRAPI_API_AUTH_TOKEN,
                    json={"data": article_data},
                )
        except PIL.UnidentifiedImageError:
            pass

    def insert(self):
        for element in self.feed:
            self.insert_element(element)
