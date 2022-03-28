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

