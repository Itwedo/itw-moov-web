#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..etl import drugstores
from ..etl import forex
from ..etl import afp
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


__app__ = ['cmd']

@click.group()
def cmd():
    pass


@cmd.command()
@click.option("--hostname", default="127.0.0.1", help="Hostname or Address.")
@click.option("--port", default="8000", help="Port used to serve app.")
def run(hostname, port):
    app.run(host=hostname, port=port, debug=True)


@cmd.command()
@click.argument("action", type=click.Choice(["create", "show"]))
def config(action):
    config = configparser.ConfigParser()
    config.optionxform = lambda option: option.upper()
    if action == "create":
        if not os.path.isfile("/etc/moov/config.ini"):
            sub.call(shlex.split("sudo mkdir /etc/moov"))
        click.echo(
            (
                "Copy the following configuration "
                "in /etc/moov/config.ini "
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
        config.read("/etc/moov/config.ini")
        click.echo(config)


@cmd.command()
@click.option("--minchars", default=2000, help="Minimum number of characters to have")
def filter_articles(minchars):
    count = 0
    infos = []
    click.echo(f"Filtering article that have less than {minchars} characters\n")
    while True:
        response = requests.get(
            url=f"{STRAPI_API_URL}/actualites",
            headers=STRAPI_API_AUTH_TOKEN,
            params={
                'pagination[start]': count,
                'pagination[limit]': 100
            }
        )
        data = response.json()['data']
        if not data:
            break
        with click.progressbar(data, length=len(data)) as bar:
            for info in bar:
                if len(info['attributes']['body']) < 2000:
                    infos.append(
                        (
                            f"{info['id']}|"
                            f"{info['attributes']['title']}|"
                            f"{info['attributes']['createdAt']}|"
                            f"{info['attributes']['updatedAt']}|"
                            f"{info['attributes']['publishedAt']}"
                        )
                    )
        count += 100
        click.echo(f"{len(infos)}/{count}")
    with open("/tmp/articles.csv", "w") as f:
        writer = csv.writer(f, delimiter=',', quotechar='"')
        for info in infos:
            row = info.split('|')
            writer.writerow(row)


@cmd.command()
@click.argument('url')
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
@click.argument('filepath', type=click.Path(exists=True))
def parse_drugstores_list(filepath):
    obj = drugstore.Connector(filepath)
    obj.parse_file()
    with click.progressbar(obj.data, length=len(obj.data)) as bar:
        for info in bar:
            obj.insert_allnighters(info['start'], info['stop'], info['infos'])