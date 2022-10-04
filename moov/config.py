import configparser
import os

__all__ = [
    "DEBUG",
    "LOG_FILE",
    "CONTACT_EMAIL_USER",
    "CONTACT_EMAIL_PASSWORD",
    "CONTACT_SMTP_SERVER",
    "CONTACT_SMTP_PORT",
    "STRAPI_API_URL",
    "STRAPI_API_AUTH_TOKEN",
    "STRAPI_PUBLIC_URL",
]

config = configparser.ConfigParser()
config.read("/opt/moov/moov-web.conf")


try:
    misc_config = config["MISC"]
except KeyError:
    DEBUG = False
    LOG_FILE = "/opt/moov/log/moov-web/moov-web.log"
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
else:
    CONTACT_EMAIL_USER = contact_config["CONTACT_EMAIL_USER"]
    CONTACT_EMAIL_PASSWORD = contact_config["CONTACT_EMAIL_PASSWORD"]
    CONTACT_SMTP_SERVER = contact_config["CONTACT_SMTP_SERVER"]
    CONTACT_SMTP_PORT = contact_config["CONTACT_SMTP_PORT"]


try:
    cms_config = config["CMS"]
except KeyError:
    STRAPI_API_URL = os.environ.get(
        "STRAPI_API_URL", "https://moov-cms.sudo.mg/api"
    )
    STRAPI_API_AUTH_TOKEN = {
        "Authorization": "Bearer 1c901303b81202af57d48292eb65174d560dc19675976fb383c0b5891cfeed25d08fcb6410614126f7ee2c474c8be300f2c726fd9441918f50ba29909602d01e21635132aaf2841948eee9c09c3ec616e9c9e8ecd1f0f8dd75492da9830a2ff58f5e54d79ac2188b2dc70ab4d87ee1704b70627ed5c9fb9c4f391be350906ab1"
    }
    STRAPI_PUBLIC_URL = os.environ.get(
        "STRAPI_PUBLIC_URL",
        STRAPI_API_URL.replace(f'/{STRAPI_API_URL.split("/")[-1]}', ""),
    )
else:
    STRAPI_PUBLIC_URL = cms_config["STRAPI_PUBLIC_URL"]
    STRAPI_API_URL = cms_config["STRAPI_API_URL"]
    STRAPI_API_AUTH_TOKEN = {
        "Authorization": f"Bearer {cms_config['STRAPI_API_AUTH_TOKEN']}"
    }
