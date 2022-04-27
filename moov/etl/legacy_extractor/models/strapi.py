from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel as Model


class BaseModel(Model):
    id: int


class User(BaseModel):
    name: str
    email: str
    password: str


class BaseNode(BaseModel):
    title: str
    created_by: int
    created_at: datetime


class Forum(BaseNode):
    body: str
    category: str
    # ! field_categorie_forum


class Article(BaseNode):
    body: str
    # ! field_tags
    # field_image
    # ! field_rubrique_categorie


class Actualites(BaseNode):
    head: Optional[str]
    body: str
    images: List[str]
    # field_images_actus
    # * field_copyright_image_actus
    # ! field_type_actualite
    # field_slider_page_accueil
    # field_slider_page_categorie
    # field_compteur_accueil
    # field_compteur_categorie
    # field_slider_page_categorie_in
    # ! field_copyright_contenu
    # field_lien_sponsoris_actus


class SmallAds(BaseNode):
    price: Optional[str]
    description: str
    phone: Optional[str]
    email: Optional[str]
    mvola_ref: Optional[str]
    # ! field_type_small_ads
    # ! field_cat_gorie_small_ads
    # ! field_lieu_small_ads
    # field_image_small_ads
    # field_date_small_ads
    # ! field_contact_me
    # field_emplacement
    # ! field_sous_categorie_small_ads
    # field_nombre_de_jour_small_ads
    # field_montant_payer_small_ads
    # field_transaction_id
    # field_token_id
    # field_status_de_la_transaction


class Comment(BaseModel):
    title: str
    body: str
    created_by: Optional[int]
    created_for_id: int
    created_at: datetime
