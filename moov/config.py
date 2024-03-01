import configparser
from flask import request
from dotenv import load_dotenv
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

load_dotenv()

try:
    DEBUG = os.environ.get("DEBUG")
    LOG_FILE = os.environ.get("WEBSITE_LOG_FILE")
except KeyError:
    DEBUG = False
    LOG_FILE = "moov-web.log"
else:
    # DEBUG = eval(misc_config["DEBUG"])
    # LOG_FILE = misc_config["WEBSITE_LOG_FILE"]
    DEBUG = False
    LOG_FILE = "moov-web.log"

try:
    # contact_config = config["CONTACT"]
    CONTACT_EMAIL_USER = os.environ.get("CONTACT_EMAIL_USER")
    CONTACT_EMAIL_PASSWORD = os.environ.get("CONTACT_EMAIL_PASSWORD")
    CONTACT_SMTP_SERVER = os.environ.get("CONTACT_SMTP_SERVER")
    CONTACT_SMTP_PORT = os.environ.get("CONTACT_SMTP_PORT")
    CONTACT_EMAIL_ACCOUNT = os.environ.get("CONTACT_EMAIL_ACCOUNT")
except KeyError:
    CONTACT_EMAIL_USER = os.environ.get("EMAIL_USER", "")
    CONTACT_EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD", "")
    CONTACT_SMTP_SERVER = os.environ.get("SMTP_SERVER", "")
    CONTACT_SMTP_PORT = 465
    CONTACT_EMAIL_ACCOUNT = os.environ.get("CONTACT_EMAIL_ACCOUNT","")
else:
    # CONTACT_EMAIL_USER = contact_config["CONTACT_EMAIL_USER"]
    # CONTACT_EMAIL_PASSWORD = contact_config["CONTACT_EMAIL_PASSWORD"]
    # CONTACT_SMTP_SERVER = contact_config["CONTACT_SMTP_SERVER"]
    # CONTACT_SMTP_PORT = contact_config["CONTACT_SMTP_PORT"]
    # CONTACT_EMAIL_ACCOUNT = contact_config["CONTACT_EMAIL_ACCOUNT"]
    CONTACT_EMAIL_USER = os.environ.get("EMAIL_USER", "")
    CONTACT_EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD", "")
    CONTACT_SMTP_SERVER = os.environ.get("SMTP_SERVER", "")
    CONTACT_SMTP_PORT = 465
    CONTACT_EMAIL_ACCOUNT = os.environ.get("CONTACT_EMAIL_ACCOUNT","")

try:
    # cms_config = config["CMS"]
    STRAPI_API_URL = os.environ.get("STRAPI_API_URL")
    STRAPI_API_AUTH_TOKEN = {
        "Authorization": "Bearer " + os.environ.get("STRAPI_API_AUTH_TOKEN")
    }
    STRAPI_PUBLIC_URL = os.environ.get("STRAPI_PUBLIC_URL")
    PREVIEW_BASE_URL = os.environ.get("PREVIEW_BASE_URL")
    print(STRAPI_API_URL)
except KeyError:
    STRAPI_API_URL = os.environ.get(
        "STRAPI_API_URL", "http://localhost:1337/"
    )
    STRAPI_API_AUTH_TOKEN = {
        "Authorization": "Bearer " + os.environ.get("STRAPI_API_AUTH_TOKEN")
    }
    STRAPI_PUBLIC_URL = os.environ.get(
        "STRAPI_PUBLIC_URL",
        STRAPI_API_URL.replace(f'/{STRAPI_API_URL.split("/")[-1]}', ""),
    )
    PREVIEW_BASE_URL = os.environ.get(
        "PREVIEW_BASE_URL", "http://localhost:8000"
    )
else:
    # STRAPI_PUBLIC_URL = cms_config["STRAPI_PUBLIC_URL"]
    # STRAPI_API_URL = cms_config["STRAPI_API_URL"]
    # STRAPI_API_AUTH_TOKEN = {
    #     "Authorization": f"Bearer {cms_config['STRAPI_API_AUTH_TOKEN']}"
    # }
    # PREVIEW_BASE_URL = cms_config["PREVIEW_BASE_URL"]
    STRAPI_API_URL = os.environ.get(
        "STRAPI_API_URL", "http://localhost:1337/"
    )
    STRAPI_API_AUTH_TOKEN = {
        "Authorization": "Bearer f2ab0fe63de719bd17f5d321628a22a8d91cac37014afd980c6178f89ba755a8514560a7ec98987e73d7ebf948cf1cb730a4ac55956431560a12d3ef9b5746af5da8a8a7733a559fe3e997c9f8e1009de2d187b0147c01045fd8f38f1edadcdfb10be3a664610d6ee64ef033f515437208abe6546b1feb7fdb64ed14af3314a3"
    }
    STRAPI_PUBLIC_URL = os.environ.get(
        "STRAPI_PUBLIC_URL",
        STRAPI_API_URL.replace(f'/{STRAPI_API_URL.split("/")[-1]}', ""),
    )
    PREVIEW_BASE_URL = os.environ.get(
        "PREVIEW_BASE_URL", "http://localhost:8000"
    )

    
try:
    afp_config = config["AFP"]
    AFP_URLS = os.environ.get("AFP_URLS")
except KeyError:
    AFP_URLS = os.environ.get(
        "AFP_URLS", ["https://hosting.afp.com/clients/dts-host/francais/journal/mon/actu.xml",
                    "https://hosting.afp.com/clients/dts-host/francais/journal/medecine/actu.xml",
                    "https://hosting.afp.com/clients/dts-host/francais/journal/gen/actu.xml",
                    "https://hosting.afp.com/clients/dts-host/francais/journal/hightech/actu.xml",
                    "https://hosting.afp.com/clients/dts-host/francais/journal/spo/actu.xml"]
    )
else:
    # AFP_URLS = afp_config["AFP_URLS"].split(',')
    AFP_URLS = os.environ.get(
        "AFP_URLS", ["https://hosting.afp.com/clients/dts-host/francais/journal/mon/actu.xml",
                    "https://hosting.afp.com/clients/dts-host/francais/journal/medecine/actu.xml",
                    "https://hosting.afp.com/clients/dts-host/francais/journal/gen/actu.xml",
                    "https://hosting.afp.com/clients/dts-host/francais/journal/hightech/actu.xml",
                    "https://hosting.afp.com/clients/dts-host/francais/journal/spo/actu.xml"]
    )

try:
    # migration = config["MIGRATION"]
    ETL_DATABASE_HOST = os.environ.get("ETL_DATABASE_HOST")
    ETL_DATABASE_PORT = os.environ.get("ETL_DATABASE_PORT")
    ETL_DATABASE_NAME = os.environ.get("ETL_DATABASE_NAME")
    ETL_DATABASE_USER = os.environ.get("ETL_DATABASE_USER")
    ETL_DATABASE_PASSWORD = os.environ.get("ETL_DATABASE_PASSWORD")
    EXPORT_DIR = os.environ.get("EXPORT_DIR")
except KeyError:
    ETL_DATABASE_HOST = os.environ.get("ETL_DATABASE_HOST",'localhost')
    ETL_DATABASE_PORT = os.environ.get("ETL_DATABASE_PORT",3306)
    ETL_DATABASE_NAME = os.environ.get("ETL_DATABASE_NAME",'c1moov')
    ETL_DATABASE_USER = os.environ.get("ETL_DATABASE_USER",'moov')
    ETL_DATABASE_PASSWORD = os.environ.get("ETL_DATABASE_PASSWORD",'moov1234')
    EXPORT_DIR = os.environ.get("EXPORT_DIR",'/tmp/export')
else:
    # ETL_DATABASE_HOST = migration["ETL_DATABASE_HOST"]
    # ETL_DATABASE_PORT = int(migration["ETL_DATABASE_PORT"])
    # ETL_DATABASE_NAME = migration["ETL_DATABASE_NAME"]
    # ETL_DATABASE_USER = migration["ETL_DATABASE_USER"]
    # ETL_DATABASE_PASSWORD = migration["ETL_DATABASE_PASSWORD"]
    # EXPORT_DIR = migration["EXPORT_DIR"]
    ETL_DATABASE_HOST = os.environ.get("ETL_DATABASE_HOST",'localhost')
    ETL_DATABASE_PORT = os.environ.get("ETL_DATABASE_PORT",3306)
    ETL_DATABASE_NAME = os.environ.get("ETL_DATABASE_NAME",'c1moov')
    ETL_DATABASE_USER = os.environ.get("ETL_DATABASE_USER",'moov')
    ETL_DATABASE_PASSWORD = os.environ.get("ETL_DATABASE_PASSWORD",'moov1234')
    EXPORT_DIR = os.environ.get("EXPORT_DIR",'/tmp/export')
