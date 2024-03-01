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
    "STRAPI_API_AUTH_TOKEN_BEARER",
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
    STRAPI_API_AUTH_TOKEN_BEARER = {
        "Authorization": "Bearer " + os.environ.get("STRAPI_API_AUTH_TOKEN")
    }
    STRAPI_PUBLIC_URL = os.environ.get("STRAPI_PUBLIC_URL")
    PREVIEW_BASE_URL = os.environ.get("PREVIEW_BASE_URL")
    print("STRAPI_API_AUTH_TOKEN try")
    print(STRAPI_API_AUTH_TOKEN_BEARER)
except KeyError:
    STRAPI_API_URL = os.environ.get(
        "STRAPI_API_URL", "http://localhost:1337/"
    )
    STRAPI_API_AUTH_TOKEN_BEARER = {
        "Authorization": "Bearer " + os.environ.get("STRAPI_API_AUTH_TOKEN")
    }
    STRAPI_PUBLIC_URL = os.environ.get(
        "STRAPI_PUBLIC_URL",
        STRAPI_API_URL.replace(f'/{STRAPI_API_URL.split("/")[-1]}', ""),
    )
    PREVIEW_BASE_URL = os.environ.get(
        "PREVIEW_BASE_URL", "http://localhost:8000"
    )
    print("STRAPI_API_AUTH_TOKEN except")
    print(STRAPI_API_AUTH_TOKEN)
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
    STRAPI_API_AUTH_TOKEN_BEARER = {
        "Authorization": "Bearer 2efc0d1f3a2ef356dd50deeaf46b0ed0be41518370e0036067fc160f943559c9334c3ea0b602010bc665310cc9459b164e92c8f866af8a2dcc4e09ed7129621fb0d2809b2b00e2903820c4ab03b4118c65cd7b7da4774f6f81e0c96bec94f947e4e129e7a98bce84ae8330ffdc6ba3a04e746b54bfe086f5c569125f304785a3"
    }
    STRAPI_PUBLIC_URL = os.environ.get(
        "STRAPI_PUBLIC_URL",
        STRAPI_API_URL.replace(f'/{STRAPI_API_URL.split("/")[-1]}', ""),
    )
    PREVIEW_BASE_URL = os.environ.get(
        "PREVIEW_BASE_URL", "http://localhost:8000"
    )
    print("STRAPI_API_AUTH_TOKEN else")
    print(STRAPI_API_AUTH_TOKEN_BEARER)
    
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
