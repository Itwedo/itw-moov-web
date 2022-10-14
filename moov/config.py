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
        "Authorization": "Bearer a054f3cd7166597996223ca3ea11bfba225e6641aff4c258ffdb7a104eec12137d339f25407c097700c5bc9282fe32c3c2f2a96db00007f80f2b02f8eda2605aac0f3711fcce4b5067eaece186aa96a861fdcb33664d69bf62df691b23c3d8fc33733da0baab3a87aa6795eaa7734d1d27206e203eac7b18a954508c7cbf5f5d"
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
