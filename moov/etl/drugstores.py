#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This connector ingests an Excel file listing
all-night drugstores, and inserts them in the strapi database
using the former's REST API
"""

from datetime import datetime

from .. import config

import pandas  # a bit overkill maybe ?
import requests


class Connector(object):
    def __init__(self, filepath):
        self.filepath = filepath
        dfs = pandas.ExcelFile(self.filepath)
        self.sheet_names = dfs.sheet_names
        self.data = []

    @property
    def drugstores(self):
        seen = set()
        for info in self.data:
            for name, address, phonenumbers in info['infos']:
                seen.add(name)
        return seen

    def parse_file(self):
        """Populates self.data with mappings representing
        drugstores available during a given time slot
        """
        for sheet_name in self.sheet_names:
            df = pandas.read_excel(self.filepath, sheet_name=sheet_name)
            infos = None
            valid_lines = filter(
                lambda x: isinstance(x[1], str) and not pandas.isnull(x[1]),
                df.values,
            )
            for line in valid_lines:
                if line[1].startswith("DATE"):
                    if infos:
                        self.data.append(infos)
                    splits = line[1].split()
                    start = datetime.strptime(splits[2], "%d/%m/%y")
                    stop = datetime.strptime(splits[4], "%d/%m/%y")
                    infos = {"start": start, "stop": stop, "infos": []}
                else:
                    infos["infos"].append(list(line[1:]))
            self.data.append(infos)  # don't miss the last block
        self.data = sorted(self.data, key=lambda x: x["start"])
        for info in self.data:
            info["start"] = info["start"].strftime("%Y-%m-%d")
            info["stop"] = info["stop"].strftime("%Y-%m-%d")
        return

    def insert_allnighters(self, start, stop, infos):
        """Using strapi's REST API, insert data.
        It requires the existence of following components:
          - 'drugstore' with fields (name, address, phonenumbers)
          - 'allnighter' with fields (start, stop, drugstore<fk>)
        For the time slot, if drugstore does not exist, create it
        then if current availability is not set, set it
        otherwise, in any case, do nothing
        """
        drugstores_url = f"{config.STRAPI_API_URL}/drugstores"
        allnighters_url = f"{config.STRAPI_API_URL}/allnighters"
        for name, address, phonenumbers in infos:
            if phonenumbers.lower() != "telephone":
                name = name.rstrip().lstrip()  # sanitize! lol
                response = requests.get(
                    drugstores_url,
                    headers=config.STRAPI_API_AUTH_TOKEN,
                    params={"filters[name][$eq]": name},
                )
                if not response.json()["data"]:
                    response = requests.post(
                        drugstores_url,
                        headers=config.STRAPI_API_AUTH_TOKEN,
                        json={
                            "data": {
                                "name": name,
                                "address": address,
                                "phonenumbers": phonenumbers,
                            }
                        },
                    )
                    drugstore_id = response.json()["data"]["id"]
                else:
                    drugstore_id = response.json()["data"][0]["id"]
                response = requests.get(
                    allnighters_url,
                    headers=config.STRAPI_API_AUTH_TOKEN,
                    params={
                        "filters[drugstore_id][$eq]": drugstore_id,
                        "filters[start][$eq]": start,
                        "filters[stop][$eq]": stop,
                    },
                )
                if not response.json()["data"]:
                    response = requests.post(
                        allnighters_url,
                        headers=config.STRAPI_API_AUTH_TOKEN,
                        json={
                            "data": {
                                "start": start,
                                "stop": stop,
                            }
                        },
                    )
                    event_id = response.json()['data']['id']
                    response = requests.put(
                        f'{allnighters_url}/{event_id}',
                        headers=config.STRAPI_API_AUTH_TOKEN,
                        json={
                            "data": {
                                "drugstore": [drugstore_id]
                            }
                        },
                    )
        return
