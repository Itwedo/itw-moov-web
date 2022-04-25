#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..etl import drugstores
from ..etl import forex
from ..etl import afp
from ..etl.legacy_extractor import resolve
from ..etl import actualities
from ..config import *
from .. import app

import click
import configparser
import csv
import os
import requests
import shlex
import subprocess as sub
import sys


__app__ = ["cmd"]


@click.group()
def cmd():
    pass


@cmd.command()
@click.option("--hostname", default="127.0.0.1", help="Hostname or Address.")
@click.option("--port", default="8000", help="Port used to serve app.")
def run(hostname, port):
    app.run(host=hostname, port=port, debug=True)


@cmd.command()
def export_drupal():
    resolve.run()


@cmd.command()
@click.argument("action", type=click.Choice(["create", "show"]))
def config(action):
    config = configparser.ConfigParser()
    config.optionxform = lambda option: option.upper()
    if action == "create":
        if not os.path.isfile("/opt/moov/moov-web.conf"):
            sub.call(shlex.split("sudo mkdir /opt/moov"))
        click.echo(
            (
                "Copy the following configuration "
                "in /opt/moov/moov-web.conf "
                "and customize it\n"
            )
        )
        config.add_section("CONTACT")
        config.add_section("CMS")
        config.set("CONTACT", "CONTACT_EMAIL_USER", "someone@some.domain")
        config.set("CONTACT", "CONTACT_EMAIL_PASSWORD", "xxxxxxxxxxxx")
        config.set("CONTACT", "CONTACT_SMTP_SERVER", "example.mail.server")
        config.set("CONTACT", "CONTACT_SMTP_PORT", "465")
        config.set("CMS", "STRAPI_PUBLIC_URL", "http://localhost:2337")
        config.set("CMS", "STRAPI_API_URL", "http://localhost:2337/api")
        config.set("CMS", "STRAPI_API_AUTH_TOKEN", "cms_generated_token")
        config.write(sys.stdout)
    elif action == "show":
        config.read("/opt/moov/moov-web.conf")
        click.echo(config)


@cmd.command()
@click.option(
    "--minchars", default=2000, help="Minimum number of characters to have"
)
def filter_articles(minchars):
    count = 0
    infos = []
    click.echo(
        f"Filtering article that have less than {minchars} characters\n"
    )
    while True:
        response = requests.get(
            url=f"{STRAPI_API_URL}/actualites",
            headers=STRAPI_API_AUTH_TOKEN,
            params={
                "populate": "images",
                "pagination[start]": count,
                "pagination[limit]": 100,
            },
        )
        data = response.json()["data"]
        if not data:
            break
        with click.progressbar(data, length=len(data)) as bar:
            for info in bar:
                if len(info["attributes"]["body"]) < 2000:
                    infos.append(
                        (
                            f"{info['id']}|"
                            f"{info['attributes']['title']}|"
                            f"{info['attributes']['createdAt']}|"
                            f"{info['attributes']['updatedAt']}|"
                            f"{info['attributes']['publishedAt']}"
                        )
                    )
                    result = requests.delete(
                        url=f"{STRAPI_API_URL}/actualites/{info['id']}",
                        headers=STRAPI_API_AUTH_TOKEN,
                    )
                elif (
                    info["attributes"]["images"]["data"]
                    and info["attributes"]["images"]["data"][0]["attributes"][
                        "width"
                    ]
                ):
                    if (
                        info["attributes"]["images"]["data"][0]["attributes"][
                            "width"
                        ]
                        < 600
                    ):
                        infos.append(
                            (
                                f"{info['id']}|"
                                f"{info['attributes']['title']}|"
                                f"{info['attributes']['createdAt']}|"
                                f"{info['attributes']['updatedAt']}|"
                                f"{info['attributes']['publishedAt']}"
                            )
                        )
                        result = requests.delete(
                            url=f"{STRAPI_API_URL}/actualites/{info['id']}",
                            headers=STRAPI_API_AUTH_TOKEN,
                        )
        count += 100
        click.echo(f"{len(infos)}/{count}")
    with open("/tmp/articles.csv", "w") as f:
        writer = csv.writer(f, delimiter=",", quotechar='"')
        for info in infos:
            row = info.split("|")
            writer.writerow(row)


@cmd.command()
@click.argument("url")
def get_afp_feed(url):
    obj = afp.Connector(url)
    feed = obj.get_feed()
    with click.progressbar(obj.feed, length=len(obj.feed)) as bar:
        for info in bar:
            obj.insert_element(info)


@cmd.command()
def update_currency_exchange():
    obj = forex.RecordChanges()
    obj.save()


@cmd.command()
@click.argument("filepath", type=click.Path(exists=True))
def parse_drugstores_list(filepath):
    obj = drugstore.Connector(filepath)
    obj.parse_file()
    with click.progressbar(obj.data, length=len(obj.data)) as bar:
        for info in bar:
            obj.insert_allnighters(info["start"], info["stop"], info["infos"])


@cmd.command()
def get_category():
    csv_file = csv.reader(
        open("moov/api/data/category.csv", "r"), delimiter=","
    )
    actualities = list()
    magazines = list()
    for row in csv_file:
        result = requests.get(
            url=f"{STRAPI_API_URL}/actualites",
            params={
                "populate": "images",
                "sort": "id:desc",
                "filters[Type][$eq]": "Actualite",
                "filters[category][$eq]": row[1],
                "pagination[pageSize]": 9,
                "pagination[withCount]": 1,
            },
            headers=STRAPI_API_AUTH_TOKEN,
        )
        if result.json()["data"] and not row[2] in actualities:
            actualities.append({"display": row[2], "slug": row[0]})

        result = requests.get(
            url=f"{STRAPI_API_URL}/actualites",
            params={
                "populate": "images",
                "sort": "id:desc",
                "filters[Type][$eq]": "Tendance",
                "filters[category][$eq]": row[1],
                "pagination[pageSize]": 9,
                "pagination[withCount]": 1,
            },
            headers=STRAPI_API_AUTH_TOKEN,
        )
        if result.json()["data"] and not row[2] in magazines:
            # magazines.append({row[2]: row[0]})
            magazines.append({"display": row[2], "slug": row[0]})
    print({"actuality": actualities, "magazine": magazines})


@cmd.command()
def import_actus():
    obj = actualities.Connector("/tmp/export/actualites", "Actualite")
    article_path = obj.article_dir
    with click.progressbar(range(5767), length=5767) as bar:
        for info in bar:
            obj.post_articles_file(f"{article_path}/actualites.{info}.json")
            print(f"{article_path}/actualites.{info}.json")
            print(f"  {str(obj.count)} actualities inserted")


@cmd.command()
def import_tendance():
    obj = actualities.Connector("/tmp/export/tendance_moov", "Tendance")
    article_path = obj.article_dir
    with click.progressbar(range(2132), length=2132) as bar:
        for info in bar:
            obj.post_articles_file(f"{article_path}/tendance_moov.{info}.json")
            print(f"{article_path}/tendance_moov.{info}.json")
            print(f"  {str(obj.count)} actualities inserted")


@cmd.command()
def delete_actus():
    for i in range(10):

        result = requests.get(
            url=f"{STRAPI_API_URL}/actualites",
            params={
                "pagination[pageSize]": 100,
                "sort": "id:asc",
            },
            headers=STRAPI_API_AUTH_TOKEN,
        )

        with click.progressbar(
            result.json()["data"], length=len(result.json()["data"])
        ) as bar:
            for actu in bar:

                result = requests.delete(
                    url=f"{STRAPI_API_URL}/actualites/{actu['id']}",
                    headers=STRAPI_API_AUTH_TOKEN,
                )
        print(i)
