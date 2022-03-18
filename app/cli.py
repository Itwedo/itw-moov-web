#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import app

import click
import configparser
import os
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
@click.argument("action", type=click.Choice(["generate", "show"]))
def config(action):
    config = configparser.ConfigParser()
    config.optionxform = lambda option: option.upper()
    if action == "generate":
        sub.call(shlex.split("sudo mkdir /etc/moov-website"))
        if not os.path.isfile("/etc/moov-website/config.ini"):
            sub.call(shlex.split("sudo mkdir /etc/moov-website"))
        click.echo(
            (
                "Copy the following configuration "
                "in /etc/moov-website/config.ini "
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
        config.read("/etc/moov-website/config.ini")
        click.echo(config)
