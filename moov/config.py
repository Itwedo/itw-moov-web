import configparser
from flask import request
import os

__all__ = [
    "DEBUG",
    "LOG_FILE",
    "CONTACT_EMAIL_USER",
    "CONTACT_EMAIL_PASSWORD",
    "CONTACT_SMTP_SERVER",
    "CONTACT_SMTP_PORT",
    "CONTACT_EMAIL_ACCOUNT",
    "STRAPI_API_URL",
    "STRAPI_API_AUTH_TOKEN",
    "STRAPI_PUBLIC_URL",
    "AFP_URLS",
    "PREVIEW_BASE_URL",
    "ETL_DATABASE_NAME",
    "ETL_DATABASE_HOST",
    "ETL_DATABASE_PORT",
    "ETL_DATABASE_USER",
    "ETL_DATABASE_PASSWORD",
    "EXPORT_DIR"
]

config = configparser.ConfigParser()
# config.read("/opt/moov/moov-web.conf")
config.read("G:\ITWEDO\Projet\Telma\moov-web-setup\moov-web.conf") 

try:
    misc_config = config["MISC"]
except KeyError:
    DEBUG = False
    # LOG_FILE = "/opt/moov/log/moov-web/moov-web.log"
    LOG_FILE = "G:\ITWEDO\Projet\Telma\moov-web-setup\moov-web.log"
else:
    DEBUG = eval(misc_config["DEBUG"])
    LOG_FILE = misc_config["WEBSITE_LOG_FILE"]


try:
    contact_config = config["CONTACT"]
except KeyError:
    CONTACT_EMAIL_USER = os.environ.get("EMAIL_USER", "")
    CONTACT_EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD", "")
    CONTACT_SMTP_SERVER = os.environ.get("SMTP_SERVER", "")
    CONTACT_SMTP_PORT = 465
    CONTACT_EMAIL_ACCOUNT = os.environ.get("CONTACT_EMAIL_ACCOUNT","")
else:
    CONTACT_EMAIL_USER = contact_config["CONTACT_EMAIL_USER"]
    CONTACT_EMAIL_PASSWORD = contact_config["CONTACT_EMAIL_PASSWORD"]
    CONTACT_SMTP_SERVER = contact_config["CONTACT_SMTP_SERVER"]
    CONTACT_SMTP_PORT = contact_config["CONTACT_SMTP_PORT"]
    CONTACT_EMAIL_ACCOUNT = contact_config["CONTACT_EMAIL_ACCOUNT"]

try:
    cms_config = config["CMS"]
except KeyError:
    STRAPI_API_URL = os.environ.get(
        "STRAPI_API_URL", "http://localhost:1337/"
    )
    STRAPI_API_AUTH_TOKEN = {
        "Authorization": "Bearer 1ac43231c24bc07a3d0b476f15234c1348a3bb37af00f4d4da40181e28602b2352334882ffe5b045aa434b0ef6faaa3b19f911dcefa7794e9d266b86d8194a442bd3f044f5320bb14465a2cce35dcc210f46bc687cbc9f8b1c8d3b2e924e13d7f4717c2304a83ed382e610aa48eed717bca659999206e90ea977a37beaab20ab"
    }
    STRAPI_PUBLIC_URL = os.environ.get(
        "STRAPI_PUBLIC_URL",
        STRAPI_API_URL.replace(f'/{STRAPI_API_URL.split("/")[-1]}', ""),
    )
    PREVIEW_BASE_URL = os.environ.get(
        "PREVIEW_BASE_URL", request.base_url
    )
else:
    STRAPI_PUBLIC_URL = cms_config["STRAPI_PUBLIC_URL"]
    STRAPI_API_URL = cms_config["STRAPI_API_URL"]
    STRAPI_API_AUTH_TOKEN = {
        "Authorization": f"Bearer {cms_config['STRAPI_API_AUTH_TOKEN']}"
    }
    PREVIEW_BASE_URL = cms_config["PREVIEW_BASE_URL"]

    
try:
    afp_config = config["AFP"]
except KeyError:
    AFP_URLS = os.environ.get(
        "AFP_URLS", ["https://hosting.afp.com/clients/dts-host/francais/journal/mon/actu.xml",
                    "https://hosting.afp.com/clients/dts-host/francais/journal/medecine/actu.xml",
                    "https://hosting.afp.com/clients/dts-host/francais/journal/gen/actu.xml",
                    "https://hosting.afp.com/clients/dts-host/francais/journal/hightech/actu.xml",
                    "https://hosting.afp.com/clients/dts-host/francais/journal/spo/actu.xml"]
    )
else:
    AFP_URLS = afp_config["AFP_URLS"].split(',')

try:
    migration = config["MIGRATION"]
except KeyError:
    ETL_DATABASE_HOST = os.environ.get("ETL_DATABASE_HOST",'localhost')
    ETL_DATABASE_PORT = os.environ.get("ETL_DATABASE_PORT",3306)
    ETL_DATABASE_NAME = os.environ.get("ETL_DATABASE_NAME",'c1moov')
    ETL_DATABASE_USER = os.environ.get("ETL_DATABASE_USER",'moov')
    ETL_DATABASE_PASSWORD = os.environ.get("ETL_DATABASE_PASSWORD",'moov1234')
    EXPORT_DIR = os.environ.get("EXPORT_DIR",'/tmp/export')
else:
    ETL_DATABASE_HOST = migration["ETL_DATABASE_HOST"]
    ETL_DATABASE_PORT = int(migration["ETL_DATABASE_PORT"])
    ETL_DATABASE_NAME = migration["ETL_DATABASE_NAME"]
    ETL_DATABASE_USER = migration["ETL_DATABASE_USER"]
    ETL_DATABASE_PASSWORD = migration["ETL_DATABASE_PASSWORD"]
    EXPORT_DIR = migration["EXPORT_DIR"]
