from logging.handlers import TimedRotatingFileHandler
import configparser
import logging
import os

__all__ = [
    'CONTACT_EMAIL_USER',
    'CONTACT_EMAIL_PASSWORD',
    'CONTACT_SMTP_SERVER',
    'CONTACT_SMTP_PORT',
    'STRAPI_API_URL',
    'STRAPI_API_AUTH_TOKEN',
    'STRAPI_PUBLIC_URL'
]

config = configparser.ConfigParser()
config.read('/etc/moov-website/config.ini')


try:
    contact_config = config['CONTACT']
except KeyError:
    CONTACT_EMAIL_USER = os.environ.get("EMAIL_USER", "")
    CONTACT_EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD", "")
    CONTACT_SMTP_SERVER = os.environ.get("SMTP_SERVER", "")
    CONTACT_SMTP_PORT = 465
else:
    CONTACT_EMAIL_USER = contact_config['CONTACT_EMAIL_USER']
    CONTACT_EMAIL_PASSWORD = contact_config['CONTACT_EMAIL_PASSWORD']
    CONTACT_SMTP_SERVER = contact_config['CONTACT_SMTP_SERVER']
    CONTACT_SMTP_PORT = contact_config['CONTACT_SMTP_PORT']


try:
    cms_config = config['CMS']
except KeyError:
    STRAPI_API_URL = os.environ.get("STRAPI_API_URL", "http://localhost:2337/api")
    STRAPI_API_AUTH_TOKEN = {
        "Authorization": f'Bearer {os.environ.get("STRAPI_API_AUTH_TOKEN", "")}'
    }
    STRAPI_PUBLIC_URL = os.environ.get(
        "STRAPI_PUBLIC_URL", STRAPI_API_URL.replace(f'/{STRAPI_API_URL.split("/")[-1]}', "")
    )
else:    
    STRAPI_PUBLIC_URL = cms_config['STRAPI_PUBLIC_URL']
    STRAPI_API_URL = cms_config['STRAPI_API_URL']
    STRAPI_API_AUTH_TOKEN = {
        "Authorization": f"Bearer {cms_config['STRAPI_API_AUTH_TOKEN']}"
    }