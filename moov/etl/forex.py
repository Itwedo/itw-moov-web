#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Currency exchange utility for MGA
Original Author: https://github.com/Piooon

Originally commited in
https://github.com/codeandscale/moov-proto/tree/feature/exchange
"""

import requests
import json

from datetime import date, timedelta
from .. import config


class RecordChanges:
    def __init__(self) -> None:
        self.url_api = "https://api.exchangerate.host"

    def fetch_data(self, query):
        data = requests.get(query)
        return data.json()

    def save(self):
        """
        save the data into strapi
        :params :
        data: data to save
        type : (string) type of the data ['exchange_rate','historical','fluctuation']
        """
        exchangerates_url = f"{config.STRAPI_API_URL}/exchangerates"
        data = self.fetch_exchange_rate()
        for element in data:
            response = requests.post(
                exchangerates_url,
                headers=config.STRAPI_API_AUTH_TOKEN,
                json={
                    "data": element  # date, currency, rate
                },
            )

    def fetch_exchange_rate(self):
        query = f"{self.url_api}/latest?base=MGA"
        data = self.fetch_data(query)
        result = [
            {"date": data["date"], "currency": currency, "rate": value}
            for currency, value in data["rates"].items()
        ]
        return result

    def fetch_historical(self, delta):
        query = f"{self.url_api}/timeseries?base=USD"
        end_date = date.today()
        start_date = end_date - timedelta(days=delta)
        query += f"&start_date={str(start_date)}&end_date={str(end_date)}"
        data = self.fetch_data(query)
        del data["motd"]
        return data


class ChangesController:
    def __init__(self, delta=30) -> None:
        self.delta = delta
        self.check()

    def check(self):
        """
        check if today's rate already exists and load it if not
        """
        RecordChanges().save(self.delta)

    def curr_in_mga(self, flag=False):
        """
        return the value of each currency in ariary
        """
        exchangerates_url = f"{config.STRAPI_API_URL}/exchangerates"
        response = requests.get(
            exchangerates_url,
            headers=config.STRAPI_API_AUTH_TOKEN,
            params={"filters[date][$eq]": date.today()},
        )
        records = response.json()["data"][0]
        if flag:
            return records
        rates = dict()
        for curr, value in records.get("rates").items():
            if value != 0:
                rates[curr] = round(1 / value, 3)
            else:
                rates[curr] = value
        records.update(rates=rates)
        return records

    def historical(self):
        pass

    def convert(self, base, target, value):
        records = self.curr_in_mga(flag=True)
        response = (
            records["rates"][target] * int(value) / records["rates"][base]
        )

        return {
            "date": records["date"],
            "base": base,
            "target": target,
            "value": value,
            "result": response,
        }
