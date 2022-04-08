import json
from functools import wraps
from datetime import datetime, date

from tqdm import tqdm
from rich import print
from rich.traceback import install
from pathlib import Path
from .const import EXPORT_DIR
from .models.drupal import (
    Comment as DrupalComment,
    FieldDataBody,
    FieldDataFieldChapeau,
    FieldDataFieldContenuArticle,
    FieldDataFieldCourriel,
    FieldDataFieldDescriptionActualite,
    FieldDataFieldDescriptionSmallAds,
    FieldDataFieldImageActus,
    FieldDataFieldImagesActus,
    FieldDataFieldPhoneNumber,
    FieldDataFieldPrice,
    FieldDataFieldReferenceMvola,
    Node,
    Users,
)
from .models.strapi import (
    Comment as StrapiComment,
    Actualites,
    Article,
    Forum,
    SmallAds,
    User,
)

install(show_locals=False)


def json_serial(obj):
    """
    JSON serializer for objects not serializable by default json code
    """

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()

    raise TypeError("Type %s not serializable" % type(obj))


class Export:
    def __init__(self, name, item_per_page=10) -> None:
        self.item_per_page = item_per_page
        self.name = name
        self.page = 0
        self.row = []

    def dump(self):
        if len(self.row) == 0:
            return

        _file = EXPORT_DIR / self.name / f"{self.name}.{self.page}.json"

        _file.touch()

        with _file.open("w") as fp:
            json.dump(self.row, fp, indent=2, default=json_serial)

        self.row.clear()
        self.page += 1

    def __call__(self, func):
        @wraps(func)
        def wraped(source_row):
            model = func(source_row)

            if model is None:
                return

            self.row.append(model.dict())

            if len(self.row) >= self.item_per_page:
                self.dump()

        return wraped


export_forum = Export("forum")
export_article = Export("article")
export_actualites = Export("actualites")
export_small_ads = Export("smallads")
export_user = Export("user", item_per_page=100)
export_comment = Export("comment", item_per_page=50)


@export_forum
def process_forum(node: Node):
    user = node.get_user()

    return Forum(
        id=node.nid,
        title=node.title,
        body=node.get_field(FieldDataBody),
        created_by=user.uid,
        created_at=datetime.fromtimestamp(node.created),
    )


@export_article
def process_article(node):
    user = node.get_user()

    return Article(
        id=node.nid,
        title=node.title,
        body=node.get_field(FieldDataFieldContenuArticle),
        created_by=user.uid,
        created_at=datetime.fromtimestamp(node.created),
    )


@export_actualites
def process_actualites(node):
    user = node.get_user()

    return Actualites(
        id=node.nid,
        title=node.title,
        head=node.get_field(FieldDataFieldChapeau),
        body=node.get_field(FieldDataFieldDescriptionActualite),
        images=node.get_media(
            FieldDataFieldImagesActus,
            FieldDataFieldImageActus,
            "field_image_actus_fid",
        ),
        created_by=user.uid,
        created_at=datetime.fromtimestamp(node.created),
    )


@export_small_ads
def process_small_ads(node):
    user = node.get_user()

    return SmallAds(
        id=node.nid,
        title=node.title,
        price=node.get_field(FieldDataFieldPrice),
        description=node.get_field(FieldDataFieldDescriptionSmallAds),
        phone=node.get_field(FieldDataFieldPhoneNumber),
        email=node.get_field(FieldDataFieldCourriel),
        mvola_ref=node.get_field(FieldDataFieldReferenceMvola),
        created_by=user.uid,
        created_at=datetime.fromtimestamp(node.created),
    )


@export_user
def create_user(user):
    return User(
        id=user.uid,
        name=user.name,
        email=user.mail,
        password=user.pass_,
    )


@export_comment
def create_comment(comment):
    node = comment.get_node()
    body = comment.get_body()
    user = comment.get_user()

    if node is None:
        return

    return StrapiComment(
        id=comment.cid,
        title=comment.subject,
        body=getattr(body, "comment_body_value", None),
        created_by=getattr(user, "uid", None),
        created_for_id=node.nid,
        created_at=datetime.fromtimestamp(comment.created),
    )


def run():
    # Create user
    for user in tqdm(Users, desc="User"):
        create_user(user)

    export_user.dump()

    unhandled_type = []

    def process_unhandled(node):
        if node.type not in unhandled_type:
            unhandled_type.append(node.type)

    # Create Node
    for node in tqdm(Node, desc="Node"):
        processor_func = {
            "forum": process_forum,
            "article": process_article,
            "actualites": process_actualites,
            "small_ads": process_small_ads,
        }.get(node.type, process_unhandled)

        processor_func(node)

    export_forum.dump()
    export_article.dump()
    export_actualites.dump()
    export_small_ads.dump()

    # create comment
    for comment in tqdm(DrupalComment, desc="Comment"):
        create_comment(comment)

    export_comment.dump()

    unhandled_type.sort()
    print(unhandled_type)
