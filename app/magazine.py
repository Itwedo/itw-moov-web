from flask import (
    Blueprint,
    redirect,
    request,
    render_template,
    send_from_directory,
)

from .ads import get_ads
from .config import *

import requests


app = Blueprint("magazine", __name__, url_prefix="/magazine")


@app.route("/")
def magazine():
    # 18/page
    ads = get_ads()
    result = requests.get(
        url=f"{STRAPI_API_URL}/actualites",
        params={
            "populate": "images",
            "sort": "id:desc",
            "pagination[pageSize]": 18,
            "pagination[page]": request.args.get("page", 1),
            "pagination[withCount]": 1,
        },
        headers=STRAPI_API_AUTH_TOKEN,
    )

    return render_template(
        "tendance.html",
        result=result.json(),
        page=request.args.get("page", 1),
        CMS_URL=STRAPI_PUBLIC_URL,
        ads=ads,
    )
